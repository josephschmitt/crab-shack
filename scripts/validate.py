#!/usr/bin/env python3
"""Validate the plugin tree against every format this repo targets.

Per plugin (plugins/<name>/):
- plugin.json is a valid Agent Plugins 1.0.0 manifest: `$schema`, name matching
  the directory, semantic version, non-empty description, permitted keys only.
  Also checked against the vendored JSON Schema when `jsonschema` is installed.
- mcp.json, if present, declares the 1.0.0 `$schema` and an `mcpServers` object.
- At least one skills/<skill>/SKILL.md.

Per skill (SKILL.md):
- YAML frontmatter with only the Agent Skills fields.
- `name` matches the directory; `description` 1-1024 chars.
- `license` and `metadata.version` match the owning plugin.json.

Repo-wide:
- Plugin and skill names follow ^[a-z0-9]+(-[a-z0-9]+)*$ and are unique.
- marketplace.yaml parses and carries the fields the generator needs.
- Every generated manifest matches what scripts/sync_manifests.py would write.
- LICENSE exists when any manifest declares a license.

Exits non-zero and prints a report on any error. Warnings never fail the run.
"""
from __future__ import annotations

import json
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))

from crabshack import (  # noqa: E402
    CLAUDE_MARKETPLACE,
    CODEX_MARKETPLACE,
    COMPATIBILITY_MAX,
    CONFIG_PATH,
    CURSOR_MARKETPLACE,
    DESCRIPTION_MAX,
    MCP_SCHEMA_PATH,
    MCP_SCHEMA_URL,
    NAME_MAX,
    NAME_RE,
    PLUGIN_SCHEMA_PATH,
    PLUGIN_SCHEMA_URL,
    REPO_ROOT,
    SEMVER_RE,
    Plugin,
    Skill,
    load_config,
    load_plugins,
    rel,
)
from sync_manifests import check as check_generated, render_all  # noqa: E402

try:
    import jsonschema
except ImportError:
    jsonschema = None

SKILL_FIELDS = {"name", "description", "license", "compatibility", "metadata", "allowed-tools"}
MANIFEST_FIELDS = {"$schema", "name", "version", "description", "author", "homepage", "repository", "license", "keywords", "extensions"}
AUTHOR_FIELDS = {"name", "email", "url"}
RESERVED_NAME_TOKENS = {"claude", "anthropic"}
SKILL_BODY_MAX_LINES = 500
CONFIG_FIELDS = ("name", "displayName", "description", "owner", "codex")


class Report:
    def __init__(self) -> None:
        self.errors: list[str] = []
        self.warnings: list[str] = []

    def error(self, scope: str, msg: str) -> None:
        self.errors.append(f"{scope}: {msg}")

    def warn(self, scope: str, msg: str) -> None:
        self.warnings.append(f"{scope}: {msg}")

    def ok(self) -> bool:
        return not self.errors


def validate_name(name: object, scope: str, report: Report, expected: str | None = None) -> bool:
    if not isinstance(name, str) or not name:
        report.error(scope, "`name` is required and must be a non-empty string")
        return False
    if len(name) > NAME_MAX:
        report.error(scope, f"`name` is {len(name)} chars, max is {NAME_MAX}")
    if not NAME_RE.match(name):
        report.error(scope, "`name` must be lowercase letters and digits separated by single hyphens (no leading, trailing, or doubled hyphens)")
    if expected and name != expected:
        report.error(scope, f"`name` is '{name}' but the directory is '{expected}' — they must match")
    if RESERVED_NAME_TOKENS & set(name.split("-")):
        report.warn(scope, "`name` contains a reserved word (claude/anthropic)")
    return True


def schema_validate(instance: dict, schema_path: Path, scope: str, report: Report) -> None:
    if jsonschema is None:
        return
    schema = json.loads(schema_path.read_text(encoding="utf-8"))
    validator = jsonschema.Draft202012Validator(schema)
    for err in sorted(validator.iter_errors(instance), key=lambda e: list(e.path)):
        where = "/".join(str(p) for p in err.path) or "<root>"
        report.error(scope, f"schema: {where}: {err.message}")


def validate_manifest(plugin: Plugin, report: Report) -> None:
    scope = rel(plugin.manifest_path)
    if plugin.manifest is None:
        report.error(scope, plugin.manifest_error or "unreadable")
        return
    manifest = plugin.manifest

    if manifest.get("$schema") != PLUGIN_SCHEMA_URL:
        report.error(scope, f"`$schema` must be {PLUGIN_SCHEMA_URL}")
    validate_name(manifest.get("name"), scope, report, expected=plugin.name)

    version = manifest.get("version")
    if not isinstance(version, str) or not SEMVER_RE.match(version):
        report.error(scope, "`version` is required and must be a semantic version like 1.2.3")

    description = manifest.get("description")
    if not isinstance(description, str) or not description.strip():
        report.error(scope, "`description` is required and must be a non-empty string")

    for key in sorted(set(manifest) - MANIFEST_FIELDS):
        report.error(scope, f"unknown top-level field `{key}` (Agent Plugins permits only {', '.join(sorted(MANIFEST_FIELDS))})")

    author = manifest.get("author")
    if author is not None:
        if not isinstance(author, dict):
            report.error(scope, "`author` must be an object")
        else:
            for key in sorted(set(author) - AUTHOR_FIELDS):
                report.error(scope, f"`author.{key}` is not permitted (only name, email, url)")

    keywords = manifest.get("keywords")
    if keywords is not None and (not isinstance(keywords, list) or not all(isinstance(k, str) for k in keywords)):
        report.error(scope, "`keywords` must be an array of strings")

    schema_validate(manifest, PLUGIN_SCHEMA_PATH, scope, report)


def validate_mcp(plugin: Plugin, report: Report) -> None:
    mcp_path = plugin.dir / "mcp.json"
    if not mcp_path.exists():
        return
    scope = rel(mcp_path)
    try:
        mcp = json.loads(mcp_path.read_text(encoding="utf-8"))
    except json.JSONDecodeError as exc:
        report.error(scope, f"invalid JSON: {exc}")
        return
    if not isinstance(mcp, dict):
        report.error(scope, "must be a JSON object")
        return
    if mcp.get("$schema") != MCP_SCHEMA_URL:
        report.error(scope, f"`$schema` must be {MCP_SCHEMA_URL}")
    if not isinstance(mcp.get("mcpServers"), dict):
        report.error(scope, "`mcpServers` must be an object")
    schema_validate(mcp, MCP_SCHEMA_PATH, scope, report)


def validate_skill(skill: Skill, plugin: Plugin, report: Report) -> None:
    scope = rel(skill.path)
    if skill.error:
        report.error(scope, skill.error)
        return
    fm = skill.frontmatter
    if fm is None:
        report.error(scope, "missing YAML frontmatter (must start with `---`)")
        return

    validate_name(fm.get("name"), scope, report, expected=skill.name)

    description = fm.get("description")
    if not isinstance(description, str) or not description.strip():
        report.error(scope, "`description` is required and must be a non-empty string")
    elif len(description) > DESCRIPTION_MAX:
        report.error(scope, f"`description` is {len(description)} chars, max is {DESCRIPTION_MAX}")

    for key in sorted(set(fm) - SKILL_FIELDS):
        report.error(scope, f"unknown frontmatter field `{key}` (Agent Skills permits only {', '.join(sorted(SKILL_FIELDS))})")

    compatibility = fm.get("compatibility")
    if compatibility is not None:
        if not isinstance(compatibility, str) or not compatibility.strip():
            report.error(scope, "`compatibility` must be a non-empty string")
        elif len(compatibility) > COMPATIBILITY_MAX:
            report.error(scope, f"`compatibility` is {len(compatibility)} chars, max is {COMPATIBILITY_MAX}")

    allowed_tools = fm.get("allowed-tools")
    if allowed_tools is not None and not isinstance(allowed_tools, str):
        report.error(scope, "`allowed-tools` must be a space-separated string")

    license_ = fm.get("license")
    if not isinstance(license_, str) or not license_.strip():
        report.error(scope, "`license` is required in this repo and must be a string")
    elif plugin.manifest and license_ != plugin.manifest.get("license"):
        report.error(scope, f"`license` is '{license_}' but plugin.json says '{plugin.manifest.get('license')}'")

    metadata = fm.get("metadata")
    if not isinstance(metadata, dict):
        report.error(scope, "`metadata` is required in this repo and must be a mapping with at least `version`")
    else:
        for key, value in metadata.items():
            if not isinstance(key, str) or not isinstance(value, str):
                report.error(scope, f"`metadata.{key}` must be a string (quote numbers like version: \"1.0.0\")")
        version = metadata.get("version")
        if not isinstance(version, str):
            report.error(scope, "`metadata.version` is required and must be a quoted string")
        elif plugin.manifest and version != plugin.manifest.get("version"):
            report.error(scope, f"`metadata.version` is '{version}' but plugin.json says '{plugin.manifest.get('version')}'")

    line_count = skill.path.read_text(encoding="utf-8").count("\n")
    if line_count > SKILL_BODY_MAX_LINES:
        report.warn(scope, f"{line_count} lines; keep SKILL.md under {SKILL_BODY_MAX_LINES} and move detail into sibling files")


def load_json(path: Path, report: Report) -> dict | None:
    scope = path.as_posix()
    full = REPO_ROOT / path
    if not full.exists():
        report.error(scope, "file not found — run `python3 scripts/sync_manifests.py`")
        return None
    try:
        data = json.loads(full.read_text(encoding="utf-8"))
    except json.JSONDecodeError as exc:
        report.error(scope, f"invalid JSON: {exc}")
        return None
    if not isinstance(data, dict) or not isinstance(data.get("plugins"), list):
        report.error(scope, "`plugins` must be an array")
        return None
    return data


def validate_marketplaces(plugins: list[Plugin], report: Report) -> None:
    on_disk = {p.name for p in plugins}

    for path in (CLAUDE_MARKETPLACE, CURSOR_MARKETPLACE):
        data = load_json(path, report)
        if data is None:
            continue
        listed: set[str] = set()
        for idx, entry in enumerate(data["plugins"]):
            scope = f"{path.as_posix()}[{idx}]"
            source = entry.get("source") if isinstance(entry, dict) else None
            if not isinstance(source, str) or not source.startswith("./"):
                report.error(scope, "`source` must be a relative path starting with `./` (bare paths break `/plugin marketplace add`)")
                continue
            if not (REPO_ROOT / source).is_dir():
                report.error(scope, f"source directory `{source}` does not exist")
                continue
            listed.add(Path(source).name)
        for name in sorted(on_disk - listed):
            report.error(path.as_posix(), f"plugins/{name} is not listed")
        for name in sorted(listed - on_disk):
            report.error(path.as_posix(), f"lists '{name}' which has no plugins/{name} directory")

    data = load_json(CODEX_MARKETPLACE, report)
    if data is not None:
        listed = set()
        for idx, entry in enumerate(data["plugins"]):
            scope = f"{CODEX_MARKETPLACE.as_posix()}[{idx}]"
            source = entry.get("source") if isinstance(entry, dict) else None
            path_value = source.get("path") if isinstance(source, dict) else None
            if not isinstance(path_value, str) or not (REPO_ROOT / path_value).is_dir():
                report.error(scope, "`source.path` must point at an existing plugin directory")
                continue
            listed.add(Path(path_value).name)
        for name in sorted(on_disk ^ listed):
            report.error(CODEX_MARKETPLACE.as_posix(), f"plugin set differs from plugins/ (offending: {name})")


def validate_config(report: Report) -> dict | None:
    scope = rel(CONFIG_PATH)
    if not CONFIG_PATH.exists():
        report.error(scope, "file not found")
        return None
    try:
        cfg = load_config()
    except ValueError as exc:
        report.error(scope, str(exc))
        return None
    for key in CONFIG_FIELDS:
        if not cfg.get(key):
            report.error(scope, f"`{key}` is required")
    owner = cfg.get("owner")
    if owner is not None and (not isinstance(owner, dict) or not owner.get("name")):
        report.error(scope, "`owner` must be a mapping with at least `name`")
    return cfg if all(cfg.get(key) for key in CONFIG_FIELDS) else None


def validate_drift(cfg: dict | None, plugins: list[Plugin], report: Report) -> None:
    if cfg is None:
        return
    for problem in check_generated(render_all(cfg, plugins), plugins):
        first_line = problem.splitlines()[0]
        report.error("generated", f"{first_line} — run `python3 scripts/sync_manifests.py`")


def main() -> int:
    report = Report()

    cfg = validate_config(report)
    plugins = load_plugins()
    if not plugins:
        report.error("plugins/", "no plugin directories found")

    seen_skill_names: set[str] = set()
    for plugin in plugins:
        validate_name(plugin.name, f"plugins/{plugin.name}", report)
        validate_manifest(plugin, report)
        validate_mcp(plugin, report)
        if not plugin.skills:
            report.error(f"plugins/{plugin.name}", "no skills/*/SKILL.md found")
        for skill in plugin.skills:
            validate_skill(skill, plugin, report)
            if skill.name in seen_skill_names:
                report.error(rel(skill.path), f"duplicate skill name '{skill.name}'")
            seen_skill_names.add(skill.name)

    validate_marketplaces(plugins, report)
    validate_drift(cfg, plugins, report)

    if any(p.manifest and p.manifest.get("license") for p in plugins) and not (REPO_ROOT / "LICENSE").exists():
        report.error("LICENSE", "manifests declare a license but no LICENSE file exists at the repo root")

    if jsonschema is None:
        report.warn("scripts/validate.py", "`jsonschema` not installed; skipped JSON Schema validation of plugin.json (pip install jsonschema)")

    for warning in report.warnings:
        print(f"warning: {warning}", file=sys.stderr)

    if report.ok():
        skill_count = sum(len(p.skills) for p in plugins)
        print(f"ok — validated {len(plugins)} plugin(s), {skill_count} skill(s)")
        return 0

    print("Validation failed:\n", file=sys.stderr)
    for err in report.errors:
        print(f"  - {err}", file=sys.stderr)
    print(f"\n{len(report.errors)} error(s)", file=sys.stderr)
    return 1


if __name__ == "__main__":
    sys.exit(main())

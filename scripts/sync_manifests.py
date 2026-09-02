#!/usr/bin/env python3
"""Generate the per-client marketplace and plugin manifests.

Sources: marketplace.yaml and plugins/<name>/plugin.json.

Generated:
  .claude-plugin/marketplace.json        Claude Code marketplace
  .cursor-plugin/marketplace.json        Cursor marketplace (same shape as Claude's)
  .agents/plugins/marketplace.json       Codex marketplace
  plugins/<name>/.claude-plugin/plugin.json
  plugins/<name>/.codex-plugin/plugin.json

Usage:
  sync_manifests.py            write every generated file
  sync_manifests.py --check    exit 1 if any generated file is stale or missing
  sync_manifests.py bump <plugin> <version>
                               set the version in plugin.json and SKILL.md, then sync
"""
from __future__ import annotations

import difflib
import json
import re
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))

from crabshack import (  # noqa: E402
    CLAUDE_MARKETPLACE,
    CODEX_MARKETPLACE,
    CURSOR_MARKETPLACE,
    FRONTMATTER_RE,
    PLUGIN_GENERATED_FILES,
    REPO_ROOT,
    SEMVER_RE,
    Plugin,
    display_name,
    load_config,
    load_plugins,
    rel,
    render_json,
)

SHORT_DESCRIPTION_MAX = 100
PASSTHROUGH_FIELDS = ("version", "description", "author", "homepage", "repository", "license", "keywords")


def pick(manifest: dict, *keys: str) -> dict:
    return {key: manifest[key] for key in keys if key in manifest}


def plugin_override(cfg: dict, plugin: Plugin, *path: str):
    node = (cfg.get("overrides") or {}).get(plugin.name) or {}
    for key in path:
        if not isinstance(node, dict) or key not in node:
            return None
        node = node[key]
    return node


def plugin_display_name(cfg: dict, plugin: Plugin) -> str:
    return plugin_override(cfg, plugin, "displayName") or display_name(plugin.name)


def short_description(description: str) -> str:
    if len(description) <= SHORT_DESCRIPTION_MAX:
        return description
    return description[: SHORT_DESCRIPTION_MAX - 1].rstrip() + "…"


def render_claude_marketplace(cfg: dict, plugins: list[Plugin]) -> dict:
    entries = []
    for plugin in plugins:
        entry = {"name": plugin.name, "source": plugin.source}
        entry.update(pick(plugin.manifest, "description", "version", "author", "homepage", "repository", "license", "keywords"))
        entries.append(entry)
    return {
        "name": cfg["name"],
        "owner": cfg["owner"],
        "metadata": {"description": cfg["description"]},
        "plugins": entries,
    }


def render_codex_marketplace(cfg: dict, plugins: list[Plugin]) -> dict:
    codex_defaults = cfg.get("codex") or {}
    entries = []
    for plugin in plugins:
        entry = {
            "name": plugin.name,
            **pick(plugin.manifest, "description"),
            "source": {"source": "local", "path": plugin.source},
        }
        policy = plugin_override(cfg, plugin, "codex", "policy") or codex_defaults.get("policy")
        category = plugin_override(cfg, plugin, "codex", "category") or codex_defaults.get("category")
        if policy:
            entry["policy"] = policy
        if category:
            entry["category"] = category
        entries.append(entry)
    return {
        "name": cfg["name"],
        "interface": {"displayName": cfg["displayName"]},
        "plugins": entries,
    }


def render_claude_plugin(plugin: Plugin) -> dict:
    return {"name": plugin.name, **pick(plugin.manifest, *PASSTHROUGH_FIELDS)}


def render_codex_plugin(cfg: dict, plugin: Plugin) -> dict:
    manifest = plugin.manifest
    interface = {"displayName": plugin_display_name(cfg, plugin)}
    if "description" in manifest:
        interface["shortDescription"] = short_description(manifest["description"])
    category = plugin_override(cfg, plugin, "codex", "category") or (cfg.get("codex") or {}).get("category")
    if category:
        interface["category"] = category
    return {
        "name": plugin.name,
        **pick(manifest, "version", "description"),
        "skills": "./skills/",
        **pick(manifest, "author", "homepage", "repository", "license", "keywords"),
        "interface": interface,
    }


def render_all(cfg: dict, plugins: list[Plugin]) -> dict[Path, str]:
    """Return {path relative to repo root: file text} for every generated file."""
    plugins = sorted((p for p in plugins if p.manifest is not None), key=lambda p: p.name)
    claude = render_json(render_claude_marketplace(cfg, plugins))
    outputs = {
        CLAUDE_MARKETPLACE: claude,
        CURSOR_MARKETPLACE: claude,
        CODEX_MARKETPLACE: render_json(render_codex_marketplace(cfg, plugins)),
    }
    for plugin in plugins:
        plugin_rel = plugin.dir.relative_to(REPO_ROOT)
        outputs[plugin_rel / ".claude-plugin" / "plugin.json"] = render_json(render_claude_plugin(plugin))
        outputs[plugin_rel / ".codex-plugin" / "plugin.json"] = render_json(render_codex_plugin(cfg, plugin))
    return outputs


def orphaned_generated_files(plugins: list[Plugin]) -> list[Path]:
    """Generated files under plugin dirs that no longer have a plugin.json."""
    orphans = []
    for plugin in plugins:
        if plugin.manifest is not None:
            continue
        for generated in PLUGIN_GENERATED_FILES:
            if (plugin.dir / generated).exists():
                orphans.append((plugin.dir / generated).relative_to(REPO_ROOT))
    return orphans


def check(outputs: dict[Path, str], plugins: list[Plugin]) -> list[str]:
    problems = []
    for path, expected in outputs.items():
        full = REPO_ROOT / path
        if not full.exists():
            problems.append(f"missing: {path.as_posix()}")
            continue
        actual = full.read_text(encoding="utf-8")
        if actual != expected:
            diff = difflib.unified_diff(
                actual.splitlines(keepends=True),
                expected.splitlines(keepends=True),
                fromfile=f"{path.as_posix()} (on disk)",
                tofile=f"{path.as_posix()} (expected)",
            )
            problems.append(f"stale: {path.as_posix()}\n" + "".join(diff))
    for orphan in orphaned_generated_files(plugins):
        problems.append(f"orphaned: {orphan.as_posix()} (no plugin.json alongside it)")
    return problems


def write(outputs: dict[Path, str]) -> None:
    for path, text in outputs.items():
        full = REPO_ROOT / path
        full.parent.mkdir(parents=True, exist_ok=True)
        if full.exists() and full.read_text(encoding="utf-8") == text:
            print(f"unchanged  {path.as_posix()}")
            continue
        full.write_text(text, encoding="utf-8")
        print(f"wrote      {path.as_posix()}")


def bump(plugin_name: str, version: str) -> int:
    if not SEMVER_RE.match(version):
        print(f"error: '{version}' is not a semantic version", file=sys.stderr)
        return 2
    plugin = next((p for p in load_plugins() if p.name == plugin_name), None)
    if plugin is None or plugin.manifest is None:
        print(f"error: no plugin.json for plugins/{plugin_name}", file=sys.stderr)
        return 2

    plugin.manifest["version"] = version
    plugin.manifest_path.write_text(render_json(plugin.manifest), encoding="utf-8")
    print(f"bumped     {rel(plugin.manifest_path)} -> {version}")

    for skill in plugin.skills:
        text = skill.path.read_text(encoding="utf-8")
        match = FRONTMATTER_RE.match(text)
        if not match:
            print(f"warning: {rel(skill.path)} has no frontmatter; not updated", file=sys.stderr)
            continue
        frontmatter, count = re.subn(
            r"^(\s+version:\s*).*$",
            lambda m: f'{m.group(1)}"{version}"',
            match.group(1),
            count=1,
            flags=re.MULTILINE,
        )
        if count == 0:
            print(f"warning: {rel(skill.path)} has no metadata.version; not updated", file=sys.stderr)
            continue
        skill.path.write_text(text[: match.start(1)] + frontmatter + text[match.end(1) :], encoding="utf-8")
        print(f"bumped     {rel(skill.path)} -> {version}")
    return 0


def main(argv: list[str]) -> int:
    if argv[:1] == ["bump"]:
        if len(argv) != 3:
            print(__doc__, file=sys.stderr)
            return 2
        status = bump(argv[1], argv[2])
        if status:
            return status
        argv = []

    if argv not in ([], ["--check"]):
        print(__doc__, file=sys.stderr)
        return 2

    try:
        cfg = load_config()
    except (OSError, ValueError) as exc:
        print(f"error: {exc}", file=sys.stderr)
        return 1
    plugins = load_plugins()
    for plugin in plugins:
        if plugin.manifest is None:
            print(f"warning: skipping plugins/{plugin.name}: {plugin.manifest_error}", file=sys.stderr)
    outputs = render_all(cfg, plugins)

    if argv == ["--check"]:
        problems = check(outputs, plugins)
        if not problems:
            print(f"ok — {len(outputs)} generated file(s) are up to date")
            return 0
        print("Generated manifests are out of date:\n", file=sys.stderr)
        for problem in problems:
            print(f"  - {problem}", file=sys.stderr)
        print("\nhint: run `python3 scripts/sync_manifests.py`", file=sys.stderr)
        return 1

    write(outputs)
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))

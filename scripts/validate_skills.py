#!/usr/bin/env python3
"""Validate SKILL.md files and the marketplace manifest.

Checks, for every plugin directory referenced in `.claude-plugin/marketplace.json`
and every `plugins/*/SKILL.md` on disk:

- SKILL.md exists at the expected path.
- YAML frontmatter parses.
- `name`: present, 1-64 chars, lowercase [a-z0-9-], matches the directory name.
- `description`: present, 1-1024 chars.
- Marketplace entries point at directories that exist, and their declared
  `name` matches the SKILL.md `name`.

Exits non-zero and prints a human-readable report on any failure.
"""
from __future__ import annotations

import json
import re
import sys
from pathlib import Path

try:
    import yaml
except ImportError:
    sys.exit("error: pyyaml is required. Install with `pip install pyyaml`.")


REPO_ROOT = Path(__file__).resolve().parent.parent
PLUGINS_DIR = REPO_ROOT / "plugins"
MARKETPLACE_PATH = REPO_ROOT / ".claude-plugin" / "marketplace.json"

NAME_RE = re.compile(r"^[a-z0-9][a-z0-9-]{0,63}$")
NAME_MAX = 64
DESCRIPTION_MAX = 1024
FRONTMATTER_RE = re.compile(r"\A---\r?\n(.*?)\r?\n---\r?\n", re.DOTALL)


class Report:
    def __init__(self) -> None:
        self.errors: list[str] = []

    def error(self, scope: str, msg: str) -> None:
        self.errors.append(f"{scope}: {msg}")

    def ok(self) -> bool:
        return not self.errors


def parse_frontmatter(path: Path) -> dict | None:
    text = path.read_text(encoding="utf-8")
    match = FRONTMATTER_RE.match(text)
    if not match:
        return None
    try:
        data = yaml.safe_load(match.group(1))
    except yaml.YAMLError as exc:
        raise ValueError(f"invalid YAML: {exc}") from exc
    if not isinstance(data, dict):
        raise ValueError("frontmatter must be a YAML mapping")
    return data


def validate_skill(skill_md: Path, report: Report, expected_name: str | None = None) -> str | None:
    scope = str(skill_md.relative_to(REPO_ROOT))

    try:
        frontmatter = parse_frontmatter(skill_md)
    except ValueError as exc:
        report.error(scope, str(exc))
        return None

    if frontmatter is None:
        report.error(scope, "missing YAML frontmatter (must start with `---`)")
        return None

    name = frontmatter.get("name")
    description = frontmatter.get("description")

    if not isinstance(name, str) or not name:
        report.error(scope, "`name` is required and must be a non-empty string")
    else:
        if len(name) > NAME_MAX:
            report.error(scope, f"`name` is {len(name)} chars, max is {NAME_MAX}")
        if not NAME_RE.match(name):
            report.error(
                scope,
                "`name` must be lowercase letters, digits, and hyphens "
                "(starting with a letter or digit)",
            )
        if expected_name and name != expected_name:
            report.error(
                scope,
                f"`name` is '{name}' but parent directory is '{expected_name}' — they must match",
            )

    if not isinstance(description, str) or not description.strip():
        report.error(scope, "`description` is required and must be a non-empty string")
    elif len(description) > DESCRIPTION_MAX:
        report.error(
            scope,
            f"`description` is {len(description)} chars, max is {DESCRIPTION_MAX}",
        )

    return name if isinstance(name, str) else None


def validate_marketplace(report: Report) -> dict[str, str]:
    """Validate marketplace.json and return a map of plugin name -> source dir."""
    scope = str(MARKETPLACE_PATH.relative_to(REPO_ROOT))
    if not MARKETPLACE_PATH.exists():
        report.error(scope, "file not found")
        return {}

    try:
        manifest = json.loads(MARKETPLACE_PATH.read_text(encoding="utf-8"))
    except json.JSONDecodeError as exc:
        report.error(scope, f"invalid JSON: {exc}")
        return {}

    plugins = manifest.get("plugins")
    if not isinstance(plugins, list):
        report.error(scope, "`plugins` must be an array")
        return {}

    declared: dict[str, str] = {}
    for idx, entry in enumerate(plugins):
        entry_scope = f"{scope}[{idx}]"
        if not isinstance(entry, dict):
            report.error(entry_scope, "plugin entry must be an object")
            continue
        name = entry.get("name")
        source = entry.get("source")
        if not isinstance(name, str) or not name:
            report.error(entry_scope, "`name` is required")
            continue
        if not isinstance(source, str) or not source:
            report.error(entry_scope, "`source` is required")
            continue
        source_dir = (REPO_ROOT / source).resolve()
        if not source_dir.is_dir():
            report.error(entry_scope, f"source directory `{source}` does not exist")
            continue
        if not (source_dir / "SKILL.md").exists():
            report.error(entry_scope, f"source `{source}` has no SKILL.md")
            continue
        declared[name] = source

    return declared


def main() -> int:
    report = Report()

    declared = validate_marketplace(report)

    skill_files = sorted(PLUGINS_DIR.glob("*/SKILL.md")) if PLUGINS_DIR.is_dir() else []
    if not skill_files:
        report.error("plugins/", "no SKILL.md files found")

    seen_names: set[str] = set()
    for skill_md in skill_files:
        dir_name = skill_md.parent.name
        name = validate_skill(skill_md, report, expected_name=dir_name)
        if name:
            if name in seen_names:
                report.error(str(skill_md.relative_to(REPO_ROOT)), f"duplicate skill name '{name}'")
            seen_names.add(name)

    on_disk_names = {p.parent.name for p in skill_files}
    declared_dir_names: set[str] = set()
    for declared_name, source in declared.items():
        source_dir_name = Path(source).name
        declared_dir_names.add(source_dir_name)
        if declared_name != source_dir_name:
            report.error(
                "marketplace.json",
                f"plugin '{declared_name}' has source '{source}' — name must match directory",
            )

    for name in sorted(on_disk_names - declared_dir_names):
        report.error(
            "marketplace.json",
            f"plugin directory 'plugins/{name}' is not listed in marketplace.json",
        )

    if report.ok():
        print(f"ok — validated {len(skill_files)} skill(s)")
        return 0

    print("Skill validation failed:\n", file=sys.stderr)
    for err in report.errors:
        print(f"  - {err}", file=sys.stderr)
    print(f"\n{len(report.errors)} error(s)", file=sys.stderr)
    return 1


if __name__ == "__main__":
    sys.exit(main())

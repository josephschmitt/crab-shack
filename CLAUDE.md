# Repo layout for plugin authors

This repo is one tree that installs as a Claude Code marketplace, a Codex marketplace, a Cursor marketplace, a set of [Agent Plugins](https://agent-plugins.org) packages, and a set of [Agent Skills](https://agentskills.io) discoverable by `npx skills add`. Keep that in mind: every layout rule below exists because at least one of those consumers hard-codes it.

## Files you edit vs. files you generate

Hand-written (the only sources of truth):

- `plugins/<name>/plugin.json` — the Agent Plugins manifest. Holds the plugin's name, version, description, author, license, keywords, and homepage. Every other manifest is derived from it.
- `plugins/<name>/skills/<skill>/SKILL.md` — the skill itself. Tooling never rewrites this file.
- `plugins/<name>/README.md` — see `plugins/CLAUDE.md` for voice.
- `marketplace.yaml` — repo-level marketplace name, owner, and Codex defaults.

Generated (never hand-edit; run `python3 scripts/sync_manifests.py` after touching a source):

- `.claude-plugin/marketplace.json`, `.cursor-plugin/marketplace.json`, `.agents/plugins/marketplace.json`
- `plugins/<name>/.claude-plugin/plugin.json`, `plugins/<name>/.codex-plugin/plugin.json`

CI runs `scripts/sync_manifests.py --check` and fails on drift, so a forgotten regeneration shows up as a red PR rather than a broken install.

## Plugin directory layout

```
plugins/<plugin-name>/
├── plugin.json                       hand-written
├── README.md                         hand-written
├── skills/<skill-name>/SKILL.md      hand-written
├── .claude-plugin/plugin.json        generated
└── .codex-plugin/plugin.json         generated
```

`SKILL.md` must live at `plugins/<plugin-name>/skills/<skill-name>/SKILL.md`, **not** at the plugin root. Claude Code, Codex, Cursor, and the Agent Plugins spec all fix the skill location at `skills/<skill-name>/`; a root-level `SKILL.md` installs cleanly and registers nothing. This is also why a single skill still gets a plugin wrapper: Claude Code has no installer for bare skills from a repo, so the plugin is the packaging, and people who only want the skill folder use `npx skills add josephschmitt/crab-shack --skill <name>` or the release zip.

When the plugin contains a single skill, the skill name should match the plugin name (so `plugins/copy-editor/skills/copy-editor/SKILL.md`).

The release workflow (`.github/workflows/package-skills.yml`) zips each `skills/<skill-name>/` folder as `<skill-name>/...` at the archive root, which is the layout claude.ai expects for skill uploads. Manifests never end up in the zip.

## Names

Plugin and skill names must match `^[a-z0-9]+(-[a-z0-9]+)*$` and be at most 64 characters. That is the intersection of the four specs: lowercase alphanumerics separated by single hyphens, no leading or trailing hyphen, no `--`, no periods. Avoid the reserved words `anthropic` and `claude`.

## Adding a plugin

1. `mkdir -p plugins/<name>/skills/<name>` and write `SKILL.md` with the full frontmatter (see below).
2. Write `plugins/<name>/plugin.json` — copy an existing one and change `name`, `description`, `homepage`, and `keywords`. Keep `"version": "1.0.0"` and the `$schema` line as is.
3. Write `plugins/<name>/README.md`.
4. `python3 scripts/sync_manifests.py` to generate the client manifests.
5. `python3 scripts/validate.py` (needs `pip install pyyaml jsonschema`). Fix anything it reports, then open a PR.

## Bumping a version

Bump the plugin version whenever `SKILL.md` changes. Either edit `version` in `plugin.json` and `metadata.version` in `SKILL.md` by hand, or run:

```
python3 scripts/sync_manifests.py bump <plugin> <version>
```

which updates both files and regenerates the manifests. The validator fails if the two versions disagree.

## SKILL.md frontmatter

```yaml
---
name: distill
description: What the skill does and when to use it, in third person.
license: MIT
metadata:
  author: Joe Schmitt
  version: "1.0.0"
---
```

Only the Agent Skills fields are allowed: `name`, `description`, `license`, `compatibility`, `metadata`, `allowed-tools`. `metadata` values must be strings, so quote the version. `license` and `metadata.version` are required here and must match `plugin.json`.

## Skill authoring best practices

When authoring or editing a skill in this repo, follow Anthropic's official guidance: https://platform.claude.com/docs/en/agents-and-tools/agent-skills/best-practices

Key points to keep in mind:

- **Be concise.** Don't explain things Claude already knows. Every token in `SKILL.md` competes with the rest of the context once loaded.
- **Write the description in third person** and include both *what* the skill does and *when* to use it — that field is what Claude uses to pick the skill.
- **Use gerund-form, hyphenated names** (`processing-pdfs`, `analyzing-spreadsheets`); avoid vague names like `helper` or `utils`, and never use the reserved words `anthropic` or `claude`.
  For a plugin skill, the frontmatter `name` is also the slash command (`name: distill` registers `/distill`) and the `@`/`$` mention token in ChatGPT and Codex, so a skill meant to be invoked by hand can use a short imperative name instead.
- **Keep `SKILL.md` under 500 lines.** Split larger material into sibling files and link to them from `SKILL.md` — references should be one level deep so Claude reads them fully.
- **Match degrees of freedom to the task:** prose for open-ended work, scripts/templates for fragile or must-be-consistent operations.
- **Prefer utility scripts over generated code** for deterministic operations, and make execution intent explicit ("run X" vs. "see X for the algorithm"). Use forward slashes in all paths.
- **Avoid time-sensitive phrasing** ("after August 2025…"); put deprecated guidance under an "Old patterns" section instead.
- **Iterate against real usage.** Build a few evals before writing extensive docs, then refine based on how Claude actually navigates the skill.

## Marketplace manifest gotchas

`.claude-plugin/marketplace.json` is generated, but if you ever touch it by hand: the `source` field must be a relative path that starts with `./` (e.g. `./plugins/my-plugin`). A bare path like `plugins/my-plugin` fails schema validation with `plugins.N.source: Invalid input` and breaks `/plugin marketplace add` for the whole repo. The generator always emits the `./` form and the validator rejects anything else.

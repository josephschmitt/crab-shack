# Contributing

Thanks for poking around. Every plugin here is a portable [Agent Plugins](https://agent-plugins.org) package, meaning a `plugin.json` at the plugin root and a `skills/` directory beside it. Cursor, Codex, Copilot, VS Code, Kiro and the rest of the [compatible clients](https://agent-plugins.org/compatible-clients) read that layout directly, so there is nothing client-specific to write for them.

Claude Code is the one exception, since it reads its own manifests instead. Those are generated, which leads to the thing worth internalizing before you start: **you write four files, and a script writes Claude's.**

## Which files you edit, which are generated

| File | Who writes it |
|---|---|
| `plugins/<name>/plugin.json` | **You.** The per-plugin source of truth. |
| `plugins/<name>/skills/<skill>/SKILL.md` | **You.** The skill itself. No tool ever rewrites this. |
| `plugins/<name>/README.md` | **You.** See [`plugins/AGENTS.md`](./plugins/AGENTS.md) for the voice. |
| `marketplace.yaml` | **You**, but rarely. Repo-level marketplace name and owner for Claude Code. |
| `.claude-plugin/marketplace.json` | Generated |
| `plugins/<name>/.claude-plugin/plugin.json` | Generated |

Everything in the generated half comes from `plugins/*/plugin.json` plus `marketplace.yaml`, rendered by `scripts/sync_manifests.py`. Editing a generated file by hand does nothing useful, because the next sync overwrites it and CI fails on the difference in the meantime. If a generated file has the wrong contents, fix the source and re-run the sync.

## Setup

```
pip install pyyaml jsonschema
```

That is the whole toolchain. `jsonschema` is optional for a local run and only adds schema validation of `plugin.json`, but CI installs it, so you may as well match.

## Adding a plugin

Say you're adding a plugin called `meal-planner`.

**1. Create the skill.**

```
mkdir -p plugins/meal-planner/skills/meal-planner
```

Write `plugins/meal-planner/skills/meal-planner/SKILL.md` with this frontmatter:

```yaml
---
name: meal-planner
description: Builds a week of meals from what's in the fridge and a rough calorie target. Use when the user asks what to cook, wants a grocery list, or says "plan my meals".
license: MIT
metadata:
  author: Joe Schmitt
  version: "1.0.0"
---
```

The `description` is what an agent reads to decide whether to load the skill, so write it in third person and say both what it does and when to use it. Quote the version, since Agent Skills requires `metadata` values to be strings.

**2. Write the plugin manifest** at `plugins/meal-planner/plugin.json`. Copy one from a neighboring plugin and change the name, description, homepage, and keywords:

```json
{
  "$schema": "https://agent-plugins.org/schemas/1.0.0/plugin.schema.json",
  "name": "meal-planner",
  "version": "1.0.0",
  "description": "Builds a week of meals from what's on hand and turns it into a grocery list.",
  "author": { "name": "Joe Schmitt", "email": "ai@joe.sh", "url": "https://github.com/josephschmitt" },
  "homepage": "https://github.com/josephschmitt/crab-shack/tree/main/plugins/meal-planner",
  "repository": "https://github.com/josephschmitt/crab-shack",
  "license": "MIT",
  "keywords": ["cooking", "planning"]
}
```

The `description` here is the short marketplace blurb and can differ from the SKILL.md description, which is longer and trigger-heavy. Only the ten fields the Agent Plugins spec permits are allowed, so resist adding `displayName` or anything else. The spec sets `additionalProperties: false`, and the validator rejects extras.

**3. Write the README.** [`plugins/AGENTS.md`](./plugins/AGENTS.md) covers what belongs in it. For the install section, copy the block from any existing plugin README and substitute the name.

**4. Generate the manifests.**

```
python3 scripts/sync_manifests.py
```

You should see two paths touched: your new `.claude-plugin/plugin.json` and an updated marketplace.

**5. Validate.**

```
python3 scripts/validate.py
```

A clean run prints `ok — validated 7 plugin(s), 7 skill(s)`.

**6. Open a PR.** Commit the generated files along with your sources. They are checked in on purpose, so that installing from a clone or a tarball needs no build step.

## Rules the validator enforces

**Names** must match `^[a-z0-9]+(-[a-z0-9]+)*$` and be at most 64 characters. That is the intersection of four specs, so no capitals, no periods, no doubled hyphens, and no leading or trailing hyphen. The plugin directory name, the skill directory name, the `name` in `plugin.json`, and the `name` in SKILL.md frontmatter all have to agree. Avoid the reserved words `claude` and `anthropic`.

**Layout** is fixed at `plugins/<plugin>/skills/<skill>/SKILL.md`. A `SKILL.md` at the plugin root installs cleanly and registers nothing, because every consumer looks under `skills/`. When a plugin holds a single skill, name the skill after the plugin.

**Frontmatter** accepts only the Agent Skills fields: `name`, `description`, `license`, `compatibility`, `metadata`, and `allowed-tools`. This repo additionally requires `license` and `metadata.version`, and both must match `plugin.json`.

**Versions** start at `1.0.0` and use semver.

## Why a single skill still gets a plugin wrapper

It's a fair question, since five of the six plugins here are one skill each. Claude Code has no way to install a bare skill from a repository, and the Agent Plugins spec fixes the skill location at `<plugin>/skills/<name>/`. The wrapper is one extra directory level and it duplicates no content. Anyone who wants only the skill folder can still run `npx skills add josephschmitt/crab-shack --skill <name>` or download the release zip.

## Changing an existing plugin

Bump the version whenever `SKILL.md` changes, so installs and release zips stay traceable:

```
python3 scripts/sync_manifests.py bump meal-planner 1.1.0
```

That updates `version` in `plugin.json` and `metadata.version` in every SKILL.md under the plugin, then regenerates the manifests. Editing both by hand and running a plain sync works too; the validator fails if the two ever disagree.

## Before you open a PR

```
python3 scripts/validate.py
python3 scripts/sync_manifests.py --check
```

Both should exit clean. The second is the one people forget, and it fails whenever a source changed but the generated files didn't.

## What CI runs

On pull requests touching `plugins/`, the manifests, `marketplace.yaml`, or `scripts/`, [`.github/workflows/validate.yml`](./.github/workflows/validate.yml) runs three jobs. The first runs the validator and the drift check and must pass. The second runs `npx skills add . --list` and confirms every skill in `plugins/` is discoverable by the skills.sh CLI, and it must also pass. The third runs the Agent Skills reference validator, `skills-ref`, and is allowed to fail, since upstream labels it a demonstration tool.

Publishing a GitHub release triggers [`package-skills.yml`](./.github/workflows/package-skills.yml), which validates, zips each `skills/<skill>/` folder with the skill directory at the archive root, and uploads the zips as release assets. That archive layout is what claude.ai expects for skill uploads, and it excludes the manifests by design.

## Common errors

**`stale: .claude-plugin/marketplace.json`** and a diff. A source changed and the generated files didn't. Run `python3 scripts/sync_manifests.py`.

**`plugins/<name>/plugin.json: plugin.json not found`.** You created the plugin directory and skill but skipped step 2.

**`.claude-plugin/marketplace.json: plugins/<name> is not listed`.** Same cause. Without a `plugin.json`, the generator skips the plugin entirely and it never reaches the marketplaces.

**`` `metadata.version` is '1.0.1' but plugin.json says '1.0.0' ``.** The two version fields drifted. Use the `bump` subcommand instead of editing one by hand.

**`unknown top-level field `displayName``.** The Agent Plugins schema permits ten top-level fields and nothing else. Drop the extra key.

**`` `source` must be a relative path starting with `./` ``.** You hand-edited a marketplace file. Don't; the generator always emits the correct form. A bare path like `plugins/my-plugin` breaks `/plugin marketplace add` for the entire repo.

## Also worth reading

[`AGENTS.md`](./AGENTS.md) is short and points back here for the mechanics, but its skill authoring best practices are worth a skim before you write a `SKILL.md`. [`plugins/AGENTS.md`](./plugins/AGENTS.md) covers the voice for a plugin's `README.md`. Both are also reachable as `CLAUDE.md`, which is a symlink, so harnesses that look for either name find the same file.

<p align="center"><img width="340" src="https://github.com/user-attachments/assets/26f5176c-2303-4a46-a856-b8f20eacf07f" /></p>

# Joe's Crab Shack 🦀

Because crabs belong in shacks. A personal plugin marketplace for Claude Code, Codex, Cursor, and any agent that speaks Agent Skills.

## Install

Every plugin here is a single skill wrapped in an [Agent Plugins](https://agent-plugins.org) package, and each skill follows the [Agent Skills](https://agentskills.io) spec, so the same folder installs into most agents. Pick your flavor:

| Where | How |
|---|---|
| Just the skill, no plugin (Claude Code, Cursor, Codex, Copilot, and 50+ others) | `npx skills add josephschmitt/crab-shack --skill <name>` |
| Claude Code | `/plugin marketplace add josephschmitt/crab-shack` then `/plugin install <name>@joes-crab-shack` |
| Claude.ai (web or desktop) | Download `<name>.zip` from the [latest release](https://github.com/josephschmitt/crab-shack/releases/latest), then **+** → **Create skill** and upload it |
| Codex / ChatGPT | `codex plugin marketplace add josephschmitt/crab-shack` then install from the plugin directory |
| Cursor | Add this repo under **Customize → Plugins**, or clone it and copy `plugins/<name>` into `~/.cursor/plugins/local/` |
| Any other Agent Plugins client | Point it at `plugins/<name>/` |

Browse [skills.sh](https://skills.sh) to see what other people are installing, or run `npx skills add josephschmitt/crab-shack` with no `--skill` flag to pick from a menu.

## What's Inside

Browse the [`plugins/`](./plugins) directory to see what's cooking.

## Repo layout

```
plugins/<name>/
├── plugin.json              Agent Plugins manifest (hand-written, source of truth)
├── skills/<name>/SKILL.md   the skill itself (Agent Skills format)
├── README.md
├── .claude-plugin/          generated
└── .codex-plugin/           generated
```

The marketplace files for Claude Code, Cursor, and Codex are generated from `marketplace.yaml` plus each `plugin.json` by `scripts/sync_manifests.py`.

Adding a plugin? [`CONTRIBUTING.md`](./CONTRIBUTING.md) walks through it and spells out which files you write versus which ones the sync script generates.

# Repo guidance

Every plugin here is a portable [Agent Plugins](https://agent-plugins.org) package: `plugin.json` at the plugin root plus `skills/`. Most clients read that directly. Claude Code is the exception and gets generated manifests of its own.

**[`CONTRIBUTING.md`](./CONTRIBUTING.md) is the reference for all of it**: which files are hand-written and which are generated, how to add a plugin, the naming and frontmatter rules, version bumps, and what each validator error means. Read it before adding or restructuring a plugin rather than inferring the layout from neighboring files.

[`plugins/AGENTS.md`](./plugins/AGENTS.md) covers the voice for a plugin's `README.md`.

## Two rules worth having in context

**Never hand-edit a generated file.** `.claude-plugin/marketplace.json` and each plugin's `.claude-plugin/plugin.json` are rendered from `plugins/*/plugin.json` plus `marketplace.yaml`. Change the source, then run:

```
python3 scripts/sync_manifests.py
```

**Validate before you call the work done.** Both commands should exit clean, and the second is the one that catches a source edited without a re-sync:

```
python3 scripts/validate.py
python3 scripts/sync_manifests.py --check
```

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

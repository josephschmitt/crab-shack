# Repo layout for plugin authors

## Marketplace manifest

`.claude-plugin/marketplace.json` lists every plugin in this repo. When adding a new plugin entry, the `source` field must be a relative path that starts with `./` (e.g. `./plugins/my-plugin`). A bare path like `plugins/my-plugin` fails schema validation with `plugins.N.source: Invalid input` and breaks `/plugin add marketplace` for the whole repo.

## Plugin directory layout

Each plugin lives at `plugins/<plugin-name>/`. A plugin's `SKILL.md` must live at:

```
plugins/<plugin-name>/skills/<skill-name>/SKILL.md
```

**Not** `plugins/<plugin-name>/SKILL.md`. Claude Code only discovers skills under the nested `skills/<skill-name>/` directory. Putting `SKILL.md` at the plugin root means the plugin installs cleanly but no skills register and nothing shows up as a slash command.

When the plugin contains a single skill, the skill name should match the plugin name (so `plugins/copy-editor/skills/copy-editor/SKILL.md`). The validator in `scripts/validate_skills.py` enforces this layout — run it before opening a PR.

The release workflow (`.github/workflows/package-skills.yml`) zips each `skills/<skill-name>/` folder as `<skill-name>/...` at the archive root, which is the layout claude.ai expects for skill uploads.

## Skill authoring best practices

When authoring or editing a skill in this repo, follow Anthropic's official guidance: https://platform.claude.com/docs/en/agents-and-tools/agent-skills/best-practices

Key points to keep in mind:

- **Be concise.** Don't explain things Claude already knows. Every token in `SKILL.md` competes with the rest of the context once loaded.
- **Write the description in third person** and include both *what* the skill does and *when* to use it — that field is what Claude uses to pick the skill.
- **Use gerund-form, hyphenated names** (`processing-pdfs`, `analyzing-spreadsheets`); avoid vague names like `helper` or `utils`, and never use the reserved words `anthropic` or `claude`.
- **Keep `SKILL.md` under 500 lines.** Split larger material into sibling files and link to them from `SKILL.md` — references should be one level deep so Claude reads them fully.
- **Match degrees of freedom to the task:** prose for open-ended work, scripts/templates for fragile or must-be-consistent operations.
- **Prefer utility scripts over generated code** for deterministic operations, and make execution intent explicit ("run X" vs. "see X for the algorithm"). Use forward slashes in all paths.
- **Avoid time-sensitive phrasing** ("after August 2025…"); put deprecated guidance under an "Old patterns" section instead.
- **Iterate against real usage.** Build a few evals before writing extensive docs, then refine based on how Claude actually navigates the skill.

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

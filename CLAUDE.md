# Marketplace manifest

`.claude-plugin/marketplace.json` lists every plugin in this repo. When adding a new plugin entry, the `source` field must be a relative path that starts with `./` (e.g. `./plugins/my-plugin`). A bare path like `plugins/my-plugin` fails schema validation with `plugins.N.source: Invalid input` and breaks `/plugin add marketplace` for the whole repo.

# Working in this repository

This is the DocForge.live plugin for Claude. It is listed (or about to be
listed) in Anthropic's plugin directory, which tracks the `main` branch:
every push to `main` becomes a new version.

- **Until the first version is published,** all changes go to `main`.
- **After the first version is published,** never commit to `main`
  directly. Do each new version on its own branch (e.g. `release/1.1.0`),
  raise `version` in `.claude-plugin/plugin.json` there, and merge into
  `main` only when the owner says the version is ready.
- Edit `engine/`, never `skills/*/scripts/` (generated). Run
  `python tools/build.py` after engine changes.
- Before pushing, run the checks in DEVELOPMENT.md ("Setup and checks").

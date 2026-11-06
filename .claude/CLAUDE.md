# Working in this repository

This is the DocForge.live plugin for Claude. It is listed (or about to be
listed) in Anthropic's plugin directory, which tracks the `main` branch:
every push to `main` becomes a new version.

- **Until the first version is published,** all changes go to `main`.
- **After the first version is published,** never commit to `main`
  directly. Do each new version on its own branch (e.g. `release/1.1.0`),
  raise `version` in `.claude-plugin/plugin.json` there, and merge into
  `main` only when the owner says the version is ready.
- The engine lives once, in `skills/docforge/scripts/`. Never hand-edit the
  copied upstream modules there: change them in r9s9/docforge and re-sync
  with `tools/sync_upstream.py`. Plugin code lives in `toolkit/`.
- Keep the repository under 200 zip entries (files plus folders), the limit
  of Claude's plugin upload. `python tools/build.py` checks it.
- Before pushing, run the checks in DEVELOPMENT.md ("Setup and checks").

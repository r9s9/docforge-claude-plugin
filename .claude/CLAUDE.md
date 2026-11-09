# Working in this repository

This is the DocForge.live plugin for Claude. It is listed (or about to be
listed) in Anthropic's plugin directory, which tracks the `main` branch:
every push to `main` becomes a new version.

- **Until the first version is published,** all changes go to `main`.
- **After the first version is published,** never commit to `main`
  directly. Do each new version on its own branch (e.g. `release/1.1.0`),
  raise `version` in `.claude-plugin/plugin.json` there, and merge into
  `main` only when the owner says the version is ready.
- No code in this repository: only Markdown, JSON, YAML and the icon. The
  directory refuses scripts from organizations it hasn't verified. The code
  the skill runs is the `docforge-live` package, built in r9s9/docforge-toolkit
  and pinned in `skills/docforge/SKILL.md`. Raise the pin only after the new
  version is on PyPI.
- The plugin's checks live in r9s9/docforge-toolkit's `plugin_checks/`; this
  repository's CI runs them. Before pushing, run them locally (see
  DEVELOPMENT.md, "Checks") and `claude plugin validate --strict .`.

# Security

To report a security problem in the DocForge.live plugin, email
[support@docforge.live](mailto:support@docforge.live) with "Security" in the
subject line. Please don't open a public GitHub issue for it.

Include:

- the plugin version (`version` in `.claude-plugin/plugin.json`)
- where you used it: Claude chat, Cowork or Claude Code
- what you did, what happened, and a sample file if one is needed to show it

We confirm that we received the report, investigate it, and tell you what we
found and when a fix is released. Fixes reach everyone through a new plugin
version.

## Scope

The plugin's skill runs DocForge's toolkit, the `docforge-live` package,
locally, in Claude's code sandbox or on your computer. It reads and writes
Word files; its only network use is installing the pinned package from PyPI
(see "What it runs, and what it sends" in the [README](README.md)). Reports
about any of these are in scope:

- the skill and command instructions in `skills/` and `commands/`, including
  how they install the toolkit
- the toolkit, whose code is in
  [github.com/r9s9/docforge-toolkit](https://github.com/r9s9/docforge-toolkit)
- how it handles untrusted `.docx` and `.zip` files: zip bombs, path
  traversal, XML parsing and template rendering

Problems in the DocForge web app belong to
[github.com/r9s9/docforge](https://github.com/r9s9/docforge), and problems in
Claude itself to Anthropic.

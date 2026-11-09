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

The plugin runs a Python toolkit locally, in Claude's code sandbox or on your
computer. It reads and writes Word files and sends nothing over the network
(see "What it runs, and what it sends" in the [README](README.md)). Reports
about any of these are in scope:

- the toolkit in `skills/docforge/scripts/`, including the copied DocForge
  engine and the bundled docxtpl
- how it handles untrusted `.docx` and `.zip` files: zip bombs, path
  traversal, XML parsing and template rendering
- the skill and command instructions in `skills/` and `commands/`

Problems in the DocForge web app belong to
[github.com/r9s9/docforge](https://github.com/r9s9/docforge), and problems in
Claude itself to Anthropic.

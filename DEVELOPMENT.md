# Developing the DocForge plugin

## Layout

```
.claude-plugin/plugin.json       the plugin manifest (this repository is the plugin)
.claude-plugin/marketplace.json  lets Claude Code add this repo as a marketplace
skills/<skill>/SKILL.md          what Claude follows
skills/<skill>/references/       rules and formats the skill points to
skills/<skill>/scripts/          generated: a copy of engine/ (see below)
engine/docforge/                 DocForge's engine (copied) + toolkit/ (plugin code)
engine/docforge_cli.py           the CLI launcher every skill ships
engine/requirements.txt          pinned runtime packages
engine/UPSTREAM.md               which DocForge commit the engine came from
tools/sync_upstream.py           copies the engine from a DocForge checkout
tools/build.py                   copies engine/ into each skill; checks directory limits
tools/run_upstream_tests.py      runs DocForge's own engine tests against the copy
tests/                           tests for the toolkit and CLI
```

Each skill carries its own copy of the engine because claude.ai chat copies
only the loaded skill's folder into the code sandbox. **Edit `engine/`, never
`skills/*/scripts/`**, then run `python tools/build.py`. CI fails when the
copies are stale.

## The engine and upstream

`engine/docforge/` holds the deterministic modules of
[r9s9/docforge](https://github.com/r9s9/docforge):

- reading .docx files
- comparing examples
- classifying elements and deriving fields
- building templates
- rendering, validation and compliance

The web app's model client, prompts, database and storage are left out.
Claude does the AI work, guided by the skill references, which are distilled
from the app's `ai/prompts.py`.

- **Owned by the plugin, never overwritten by a sync:**
  - `toolkit/`
  - three package `__init__.py` files that export only the no-model path
- **Patched on copy:** `ai_router/document.py` gets anchored edits that remove
  model calls. The sync fails loudly if upstream changes shape there.

To pick up upstream changes:

```bash
python tools/sync_upstream.py --from ../docforge --status   # what changed since the last sync
python tools/sync_upstream.py --from ../docforge            # copy, patch, record the commit
python tools/build.py                                       # refresh the skill copies
python tools/run_upstream_tests.py --from ../docforge       # upstream's engine tests on the copy
pytest
```

`--status` also lists watched upstream files: the services and prompts that
toolkit modules and skill references are adapted from. Review the plugin side
when one changes.

## Setup and checks

```bash
python3 -m venv .venv && .venv/bin/pip install -r engine/requirements.txt pytest ruff
.venv/bin/python tools/build.py --check
.venv/bin/python tools/sync_upstream.py --verify
.venv/bin/pytest -q
.venv/bin/ruff check engine/docforge/toolkit tools tests
claude plugin validate --strict .
```

To try the CLI directly:

```bash
python engine/docforge_cli.py demo --out docforge-demo
python engine/docforge_cli.py analyze docforge-demo/invoice_1.docx docforge-demo/invoice_2.docx --work invoice-work
```

## Testing the plugin in Claude

- **Claude Code:** `claude --plugin-dir .`, then ask for something a skill
  covers, or run `/docforge:make-template`.
- **claude.ai and Cowork:**
  1. Zip the repository.
  2. Upload it under **Customize > Plugins > Add > Upload plugin**.
  3. Turn on code execution and file creation.

## Releasing

1. Raise `version` in `.claude-plugin/plugin.json`.
2. Make sure CI is green, and that `claude plugin validate --strict .`
   passes.
3. Submit or update the listing in the developer portal at
   [claude.ai/directory/manage](https://claude.ai/directory/manage). Choose
   **Plugin bundle**, enter this repository, then **Validate** and submit.

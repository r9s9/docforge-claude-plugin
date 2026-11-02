# Developing the DocForge.live plugin

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
engine/_vendor/                  bundled third-party code (docxtpl), hash-locked
tools/sync_upstream.py           copies the engine from a DocForge checkout
tools/build.py                   copies engine/ into each skill; checks directory limits
tools/run_upstream_tests.py      runs DocForge's own engine tests against the copy
tests/                           tests for the toolkit and CLI
evals/                           `claude plugin eval` cases (with and without the plugin)
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

## Bundled code

`engine/_vendor/docxtpl/` is docxtpl 0.20.2, unmodified and licensed
LGPL-2.1-only, with its license text next to it. Claude's sandboxes rarely
have docxtpl, and bundling it means filling templates needs no download.

- `vendor.lock.json` records each file's SHA-256, and `tools/build.py --check`
  fails if a file differs, so the copy stays unmodified as the license expects.
- The launcher appends `_vendor` to the end of `sys.path`, so an installed
  docxtpl wins.
- To upgrade:
  1. Copy the new release's `docxtpl/*.py` files from its wheel.
  2. Update `version` and `files` in `vendor.lock.json`.
  3. Update `BUNDLED` in `toolkit/deps.py` and the pin in `requirements.txt`.

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

## Evals

`evals/` holds five cases in the
[`claude plugin eval`](https://code.claude.com/docs/en/plugin-evals) format:

- make a template
- fill from a brief
- check and fix
- batch
- one ordinary Word request that must not use the plugin

Each case asks Claude to generate the demo documents first, so no binary
fixtures are needed.

Run them from the repository root:

```bash
claude plugin eval . --allow-tools Bash Write Edit
```

- **Python prerequisites:** the runs use Claude Code's sandboxed Bash, so
  `python3` on your machine needs the packages in `engine/requirements.txt`
  (docxtpl is bundled, so it can be left out). The sandbox blocks network
  access, so install them beforehand.
- **Cost:** evals use your Claude plan. Each case runs once per arm (with and
  without the plugin). Use `--runs 3` before a release for steadier scores.
- **Results:** written to `evals/results/`, which is git-ignored.

## Testing the plugin in Claude

- **Claude Code:** `claude --plugin-dir .`, then ask for something a skill
  covers, or run `/docforge-live:make-template`.
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

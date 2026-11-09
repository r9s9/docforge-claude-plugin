# Developing the DocForge.live plugin

## Layout

```
.claude-plugin/plugin.json          the plugin manifest (this repository is the plugin)
.claude-plugin/marketplace.json     lets Claude Code add this repo as a marketplace
skills/docforge/SKILL.md            what Claude reads first: routing, running the toolkit
skills/docforge/references/         the three workflows, plus rules and formats
skills/docforge/scripts/docforge/   DocForge's engine (copied) + toolkit/ (plugin code)
skills/docforge/scripts/docforge_cli.py   the CLI launcher
skills/docforge/scripts/requirements.txt  pinned runtime packages
skills/docforge/scripts/_vendor/    bundled third-party code (docxtpl), hash-locked
commands/                           /docforge-live:make-template, fill-template, check-document
tools/sync_upstream.py              copies the engine from a local DocForge copy
tools/UPSTREAM.md, upstream.lock.json   which DocForge commit the engine came from
tools/build.py                      checks the upload and directory limits
tools/run_upstream_tests.py         runs DocForge's own engine tests against the copy
tests/                              tests for the toolkit and CLI
evals/                              `claude plugin eval` cases (with and without the plugin)
```

There is one skill with three workflows, and the engine lives exactly once,
in the skill's `scripts/` folder. Claude chat copies only the active skill's
folder into its sandbox, so a skill can't share code with another. The
plugin upload also accepts at most 200 zip entries (files plus folders), so
the engine can't be copied into several skills. `python tools/build.py` checks
that limit; keep new files few.

The three commands in `commands/` are entry points only. Each one names a
workflow and hands over to the docforge skill, which holds the toolkit and the
rules. They load as slash commands in Claude Code and Cowork, and as skills
in claude.ai chat, so they hold no paths or placeholders other than one
`$ARGUMENTS`. `tests/test_plugin.py` checks that.

## The engine and upstream

`skills/docforge/scripts/docforge/` holds the deterministic modules of
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

To pick up upstream changes, with a local copy of r9s9/docforge next to this
repository:

1. `tools/sync_upstream.py --from ../docforge --status` lists what changed
   since the last sync.
2. `tools/sync_upstream.py --from ../docforge` copies the engine, applies the
   patches and records the commit.
3. Run the checks below, plus `tools/run_upstream_tests.py --from ../docforge`
   for upstream's own engine tests on the copy.
4. Set `ref:` in `.github/workflows/ci.yml` to the new commit in
   `tools/upstream.lock.json`; a test fails until the two match.

`--status` also lists watched upstream files: the services and prompts that
toolkit modules and skill references are adapted from. Review the plugin side
when one changes.

## Bundled code

`skills/docforge/scripts/_vendor/docxtpl/` is docxtpl 0.20.2, unmodified and licensed
LGPL-2.1-only, with its license text next to it. Claude's sandboxes rarely
have docxtpl, and bundling it means filling templates works offline.

- `vendor.lock.json` records each file's SHA-256, and `tools/build.py --check`
  fails if a file differs, so the copy stays unmodified as the license expects.
- The launcher appends `_vendor` to the end of `sys.path`, so a docxtpl
  that Python already has wins.
- To upgrade:
  1. Copy the new release's `docxtpl/*.py` files into `_vendor/docxtpl/`.
  2. Update `version` and `files` in `vendor.lock.json`.
  3. Update `BUNDLED` in `toolkit/deps.py` and the pin in `requirements.txt`.

## Setup and checks

`.github/workflows/ci.yml` is the reference: its "test" job lists the
packages to have in a virtual environment and every check to run, and the
"upstream-parity" job runs upstream's engine tests. Run the same checks
before pushing:

- `tools/build.py`: the upload, directory and bundled-code checks
- `tools/sync_upstream.py --verify`: the engine still matches its upstream
  lock
- `pytest`: the tests in `tests/`
- `ruff check`, with the settings in the workflow's Lint step
- `claude plugin validate --strict .`

To try the CLI directly, run `skills/docforge/scripts/docforge_cli.py demo`
with `--out` and a folder name, then `analyze` on two of the demo invoices.

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

Run them from the repository root with
`claude plugin eval . --allow-tools Bash Write Edit`.

- **Python prerequisites:** the runs use Claude Code's sandboxed Bash, so
  `python3` on your machine needs the packages in `skills/docforge/scripts/requirements.txt`
  (docxtpl is bundled, so it can be left out). The sandbox is offline, so
  set them up beforehand.
- **Cost:** evals use your Claude plan. Each case runs once per arm (with and
  without the plugin). Use `--runs 3` before a release for steadier scores.
- **Results:** written to `evals/results/`, which is git-ignored.

## Testing the plugin in Claude

- **Claude Code:** `claude --plugin-dir .`, then ask for something a skill
  covers, or run `/docforge-live:docforge` or one of the three commands, such
  as `/docforge-live:make-template`.
- **claude.ai and Cowork:**
  1. Zip the repository.
  2. Upload it under **Customize > Plugins > Add > Upload plugin**.
  3. Turn on code execution and file creation.
- **claude.ai, skill only:** `python tools/build.py --skill-zip docforge.zip`,
  then **Customize > Skills > Upload a skill**. That uploader rejects plugin
  manifests and nested `SKILL.md` files.

## Releasing

The directory tracks `main`: every commit pushed to it becomes a new
version that is scanned and, once it passes, can be published. So `main`
only ever holds a version you mean to release.

**Before the first version is published:** all work goes on `main`, so the
submission reflects the latest state.

**After the first version is published:** build each new version on its
own branch (for example `release/1.1.0`), never directly on `main`. For each
release:

1. On the branch, raise `version` in `.claude-plugin/plugin.json`.
2. Make sure CI is green there, and that `python tools/build.py --check` and
   `claude plugin validate --strict .` pass.
3. Test the branch in Claude (see "Testing the plugin in Claude").
4. Merge into `main` only when the version is ready to ship. The directory
   then picks it up, scans it, and publishes it according to the plugin's
   publish setting.

The first submission is made in the developer portal at
[claude.ai/directory/manage](https://claude.ai/directory/manage). Choose
**Plugin bundle**, enter this repository with branch `main`, then
**Validate** and submit.

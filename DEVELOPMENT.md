# Developing the DocForge.live plugin

## Layout

```
.claude-plugin/plugin.json          the plugin manifest (this repository is the plugin)
.claude-plugin/marketplace.json     lets Claude Code add this repo as a marketplace
skills/docforge/SKILL.md            what Claude reads first: routing, setting up and running the toolkit
skills/docforge/references/         the three workflows, plus rules and formats
commands/                           /docforge-live:make-template, fill-template, check-document
assets/icon.svg                     the listing icon (the docforge.live mark, no <style>)
evals/                              test cases for Claude Code's plugin evals (with and without the plugin)
.github/workflows/ci.yml            runs the plugin checks
```

The plugin holds only Markdown, JSON, YAML and the icon. Anthropic's
directory accepts nothing else from an organization it hasn't verified, so
there is no code here. The code the skill runs is DocForge's toolkit, the
`docforge-live` package, built in
[r9s9/docforge-toolkit](https://github.com/r9s9/docforge-toolkit) and installed
from PyPI at the version `SKILL.md` pins.

The three commands are entry points only. Each one names a workflow and hands
over to the docforge skill, which holds the rules. They load as slash commands
in Claude Code and Cowork, and as skills in claude.ai chat, so they hold no
paths or placeholders other than one `$ARGUMENTS`.

## Checks

The plugin's checks are Python, so they live in docforge-toolkit's
`plugin_checks/` folder. This repository's CI checks that repository out and
runs them against this one. They cover:

- only the file types, sizes and counts the directory and Claude's uploaders
  accept
- text the directory's scan reads as shell commands
- the Agent Skills spec, the commands, the hand-over rules and the eval format
- the toolkit commands `SKILL.md` and the references mention, which must all
  exist
- one pinned `docforge-live` version everywhere
- the whole make, fill and check flow, set up by following `SKILL.md`'s own
  steps: install the pinned version from PyPI into a fresh environment, then
  run the workflows

To run them locally, have docforge-toolkit next to this repository, install
it with pytest, and run pytest on its `plugin_checks` folder with
`--plugin` pointing here. Also run `claude plugin validate --strict .`.

## Changing the toolkit

1. Change it in docforge-toolkit and release a new version there (see its
   README, "Releasing").
2. Here, raise the pinned version in `skills/docforge/SKILL.md` everywhere it
   appears ("Run the toolkit"); the checks fail if two pins disagree.
3. Raise `version` in `.claude-plugin/plugin.json` and release the plugin
   (see "Releasing").

Never pin a version before it is on PyPI.

## Evals

`evals/` holds six cases in the format of Claude Code's plugin evals
("Plugin evals" in the Claude Code docs):

- make a template that keeps the boilerplate fixed
- make a Full template from one report, and hand over its files
- fill from a brief
- check and fix
- batch
- one ordinary Word request that must not use the plugin

Each case asks Claude to generate the demo documents first, so no binary
fixtures are needed.

Run them from the repository root with Claude Code's plugin eval command,
allowing the Bash, Write and Edit tools.

- **Toolkit:** the runs use Claude Code's sandboxed Bash, which is offline,
  so have the pinned `docforge-live` version in your `python3` beforehand.
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
- **claude.ai, skill only:** zip the `skills/docforge` folder, so that
  `docforge/SKILL.md` is at the top, then **Customize > Skills > Upload a
  skill**. That uploader rejects plugin manifests and nested `SKILL.md` files.

The first test in a new environment shows the toolkit being installed from
PyPI; later ones find it already there.

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
2. Make sure CI is green there, and that `claude plugin validate --strict .`
   passes.
3. Test the branch in Claude (see "Testing the plugin in Claude").
4. Merge into `main` only when the version is ready to ship. The directory
   then picks it up, scans it, and publishes it according to the plugin's
   publish setting.

The first submission is made in the developer portal at
[claude.ai/directory/manage](https://claude.ai/directory/manage). Choose
**Plugin bundle**, enter this repository with branch `main`, then
**Validate** and submit.

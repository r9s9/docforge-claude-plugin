# Bundled third-party code

## docxtpl 0.20.2

[docxtpl](https://pypi.org/project/docxtpl/0.20.2/) by Eric Lapouyade renders
Jinja templates inside Word files. DocForge fills templates with it.

- **License:** GNU Lesser General Public License v2.1 only (LGPL-2.1-only).
  The full text is in `docxtpl-LICENSE.txt`.
- **Unmodified:** the seven files in `docxtpl/` are byte-for-byte the
  published 0.20.2 release. `vendor.lock.json` records their SHA-256 hashes,
  and the plugin's checks fail if a file changes.
- **Why it's bundled:** Claude's code sandboxes usually have every other
  package DocForge needs but not docxtpl. Bundling it means filling templates
  works without downloading anything.
- **Replacing it:** the CLI adds this folder to the *end* of Python's import
  path, so an installed docxtpl takes precedence. Install any version you like
  (`pip install docxtpl`) and it is used instead of this copy.
- **Not needed:** `subdoc.py` imports `docxcompose`, which is not bundled. It
  loads only when sub-documents are used, which DocForge never does.

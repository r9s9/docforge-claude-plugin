# Third-party notices

## Bundled in this plugin

### docxtpl 0.20.2

- Copyright Eric Lapouyade.
- Licensed under the GNU Lesser General Public License v2.1 only
  (LGPL-2.1-only).
- Shipped unmodified in `skills/*/scripts/_vendor/docxtpl/`, with the full
  license text in `skills/*/scripts/_vendor/docxtpl-LICENSE.txt`.
- Source: <https://pypi.org/project/docxtpl/0.20.2/>.

An installed copy of docxtpl takes precedence over the bundled one, so you can
replace it with any version.

### DocForge engine

The document engine in `skills/*/scripts/docforge/` comes from
[DocForge](https://github.com/r9s9/docforge), MIT License,
© The DocForge Authors. That is the same license as this plugin.

## Used but not bundled

These packages are needed at run time and are normally already installed in
Claude's code sandboxes:

| Package | License |
|---|---|
| python-docx | MIT |
| lxml | BSD-3-Clause |
| Jinja2 | BSD-3-Clause |
| pydantic | MIT |
| python-dateutil | Apache-2.0 or BSD-3-Clause |

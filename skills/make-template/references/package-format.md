# Template packages

`build` writes a template package: a folder, or a zip of it, that holds
everything needed to fill and check documents later. Each version folder uses
the same layout and file names as the DocForge web app's template storage.

```
invoice/                        the package (one per template)
  docforge-template.json        id, name, document type, versions
  README.txt                    what the folder is, for whoever finds it
  notes.md                      optional: the person's lasting preferences
  1/                            version 1 (each build into this folder adds one)
    template.docx               the template with {{ tags }}
    with-labels.docx            the template with each field shown as «Label»
    field_definitions.json      the fields: names, types, descriptions, columns
    validation_rules.json       required fields, date and number checks, allowed values
    template_intelligence.json  document type, sections, every element's classification
    manifest.json               id, version, name, source files, creation time
    review_snapshot.json        the reviewed state this version was built from
    representative.json         the example's normalized structure (compliance uses it)
    representative.docx         the example the template was built from
    source_examples/            all the examples
    extracted_sources/          their normalized structure
```

## Versions

Building into an existing package folder adds the next version and never
changes earlier ones. The fill and check commands use the latest version
unless given `--version N`.

## Two .docx files

- **`template.docx`** is a standard [docxtpl](https://docxtpl.readthedocs.io)
  (Jinja-in-Word) template. Other tools can use it too.
- **`with-labels.docx`** reads like a finished document. It's the best file to
  show someone what the template looks like.

## Delivering it

- **Chat:** zip the package (`build --zip`, or `zip <package> --out <file>.zip`)
  and save the zip in the outputs folder. Also save `template.docx` and
  `with-labels.docx` there so they can be opened directly. Tell the person to
  attach the zip whenever they want a document filled or checked.
- **Cowork and Claude Code:** keep the package folder in the working folder,
  under `docforge-templates/<name>/` unless the person keeps templates
  somewhere else.

## Notes

`notes.md` at the package root holds preferences the person asked Claude to
remember for documents made from this template, one per line ("Dates as
2 June 2026", "Always sign off as the account manager"). The fill-template
skill reads it before writing.

- Write to it only when the person asks, and tell them you did.
- It's a plain text file in their own package, so they can read, edit or
  delete it.
- It never holds anything about the person beyond what they asked to keep.

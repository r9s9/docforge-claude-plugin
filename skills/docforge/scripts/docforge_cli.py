"""DocForge toolkit for Claude skills. Run `python3 docforge_cli.py --help`.

Every command prints one JSON object. The engine lives next to this file in
the docforge/ folder (DocForge's document engine plus the plugin toolkit).
"""

import json
import os
import sys

# Runs on old interpreters on purpose, to explain instead of crashing.
if sys.version_info < (3, 10):  # noqa: UP036
    print(json.dumps({
        "ok": False,
        "error": "Python 3.10 or newer is needed; this is " + sys.version.split()[0],
        "hint": "Run this script with a newer python3.",
    }))
    raise SystemExit(1)

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
# Bundled third-party code (docxtpl). Appended, so an installed copy wins.
sys.path.append(os.path.join(HERE, "_vendor"))

from docforge.toolkit.cli import main  # noqa: E402

raise SystemExit(main())

"""Run the skill the way each Claude app resolves it, using SKILL.md's own commands.

- Cowork and Claude Code replace ${CLAUDE_SKILL_DIR} with the skill's
  installed folder, which on a Mac can contain spaces
  (~/Library/Application Support/...).
- Claude chat copies the skill folder into its sandbox and may leave the
  placeholder as-is. SKILL.md then tells Claude to find the CLI, and to find
  attachments if they aren't in the usual uploads folder.

The commands are taken from SKILL.md's text, not retyped here, so a change to
SKILL.md that breaks them fails this test.
"""

from __future__ import annotations

import json
import re
import shutil
import subprocess
import sys
import zipfile
from pathlib import Path

import pytest

ROOT = Path(__file__).resolve().parents[1]
SKILL_MD = (ROOT / "skills" / "docforge" / "SKILL.md").read_text(encoding="utf-8")


def _cli_template() -> str:
    m = re.search(r"```bash\n(python3 \"\$\{CLAUDE_SKILL_DIR\}/scripts/docforge_cli\.py\")\n```", SKILL_MD)
    assert m, "SKILL.md must show the CLI command, quoted"
    return m.group(1).replace("python3", f'"{sys.executable}"', 1)


def _fenced(after: str) -> str:
    """The first ```bash block after the given phrase in SKILL.md."""
    i = SKILL_MD.index(after)
    m = re.search(r"```bash\n(.*?)\n\s*```", SKILL_MD[i:], re.S)
    return re.sub(r"\n\s+", "\n", m.group(1)).strip()


def _sh(command: str, cwd: Path) -> subprocess.CompletedProcess:
    return subprocess.run(["bash", "-c", command], cwd=cwd, capture_output=True, text=True, timeout=180)


def _run(docforge: str, args: str, cwd: Path) -> dict:
    proc = _sh(f"{docforge} {args}", cwd)
    assert proc.returncode == 0, proc.stdout + proc.stderr
    return json.loads(proc.stdout)


def _workflow(docforge: str, work: Path) -> None:
    """Make, fill and check, as the workflows tell Claude to."""
    assert _run(docforge, "doctor", work)["ok"] is True
    _run(docforge, "demo --out demo", work)
    _run(docforge, "analyze demo/invoice_1.docx demo/invoice_2.docx --work w", work)
    built = _run(docforge, 'build --work w --name "Invoice" --out "docforge-templates/invoice"', work)
    assert built["with_labels_docx"]
    (work / "values.json").write_text(json.dumps({"values": {
        "invoice_number": "INV-1", "invoice_date": "2026-11-06", "bill_to": "Acme & Co",
        "line_items": [{"description": "Audit", "qty": "1", "unit_price": "$10", "amount": "$10"}],
        "total_due": "$10"}}))
    rendered = _run(docforge, 'render "docforge-templates/invoice" --values values.json --out "out/INV 1.docx"', work)
    assert rendered["validation"]["status"] == "pass"
    checked = _run(docforge, 'check "docforge-templates/invoice" demo/invoice_edited.docx', work)
    assert {d["kind"] for d in checked["differences"]} >= {"changed_fixed", "changed_fixed_minor"}


def test_cowork_and_code_with_spaces_in_the_install_path(tmp_path):
    installed = tmp_path / "Library" / "Application Support" / "Claude" / "plugins" / "docforge-live" / "skills" / "docforge"
    shutil.copytree(ROOT / "skills" / "docforge", installed,
                    ignore=shutil.ignore_patterns("__pycache__"))
    docforge = _cli_template().replace("${CLAUDE_SKILL_DIR}", str(installed))
    work = tmp_path / "My Documents"
    work.mkdir()
    _workflow(docforge, work)


def test_chat_with_the_placeholder_left_as_is(tmp_path):
    # The sandbox: the uploaded skill zip unpacked somewhere, an attachment
    # somewhere else, and the placeholder not filled in.
    zip_path = tmp_path / "docforge.zip"
    subprocess.run([sys.executable, str(ROOT / "tools" / "build.py"), "--skill-zip", str(zip_path)],
                   check=True, capture_output=True, timeout=120)
    sandbox = tmp_path / "sandbox"
    zipfile.ZipFile(zip_path).extractall(sandbox / "mnt" / "skills" / "user")
    work = sandbox / "home" / "claude"
    work.mkdir(parents=True)

    # Unfilled, the command can't work: bash expands the placeholder to nothing.
    proc = _sh(_cli_template() + " doctor", work)
    assert proc.returncode != 0

    # SKILL.md's fallback finds the CLI (searching the sandbox instead of /).
    find_cli = _fenced("If you don't know that path").replace("find / ", f'find "{sandbox}" ', 1)
    found = _sh(find_cli, work).stdout.strip()
    assert found.endswith("docforge/scripts/docforge_cli.py"), found
    docforge = f'"{sys.executable}" "{found}"'
    _workflow(docforge, work)

    # SKILL.md's fallback also finds an attachment outside the uploads folder.
    upload = sandbox / "tmp" / "attachments" / "Contract v2.docx"
    upload.parent.mkdir(parents=True)
    shutil.copyfile(work / "demo" / "invoice_1.docx", upload)
    find_uploads = _fenced("If they aren't there").replace("find / ", f'find "{sandbox}" ', 1)
    listed = _sh(find_uploads, work).stdout
    assert str(upload) in listed
    assert "/scripts/" not in listed


@pytest.mark.parametrize("relative", ["scripts/docforge_cli.py"])
def test_chat_relative_path_from_the_skill_folder(tmp_path, relative):
    skill = tmp_path / "docforge"
    shutil.copytree(ROOT / "skills" / "docforge", skill, ignore=shutil.ignore_patterns("__pycache__"))
    proc = subprocess.run([sys.executable, relative, "doctor"], cwd=skill,
                          capture_output=True, text=True, timeout=60)
    assert proc.returncode == 0 and json.loads(proc.stdout)["ok"] is True

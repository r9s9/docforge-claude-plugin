"""Plugin-level guarantees: isolation from the web app, skill consistency, manifest."""

from __future__ import annotations

import json
import re
import subprocess
import sys
from pathlib import Path

import pytest

from docforge.toolkit.cli import build_parser

ROOT = Path(__file__).resolve().parents[1]
SKILLS = sorted(p.parent for p in (ROOT / "skills").glob("*/SKILL.md"))

BLOCKER = """
import importlib.abc, runpy, sys
BLOCKED = {"anthropic", "fastapi", "httpx", "jwt", "openai", "psycopg2",
           "pydantic_settings", "sqlalchemy", "starlette", "uvicorn"}
class Blocker(importlib.abc.MetaPathFinder):
    def find_spec(self, name, path, target=None):
        if name.split(".")[0] in BLOCKED:
            raise ImportError("blocked: " + name)
sys.meta_path.insert(0, Blocker())
sys.argv = [sys.argv[1]] + sys.argv[2:]
runpy.run_path(sys.argv[0], run_name="__main__")
"""


@pytest.mark.parametrize("skill", SKILLS, ids=lambda p: p.name)
def test_shipped_cli_runs_without_web_app_packages(skill, tmp_path):
    launcher = skill / "scripts" / "docforge_cli.py"
    demo = subprocess.run(
        [sys.executable, "-c", BLOCKER, str(launcher), "demo", "--out", str(tmp_path / "d")],
        capture_output=True, text=True, timeout=120,
    )
    assert demo.returncode == 0, demo.stdout + demo.stderr
    run = subprocess.run(
        [sys.executable, "-c", BLOCKER, str(launcher), "analyze",
         str(tmp_path / "d" / "invoice_1.docx"), str(tmp_path / "d" / "invoice_2.docx"),
         "--work", str(tmp_path / "w")],
        capture_output=True, text=True, timeout=120,
    )
    assert run.returncode == 0, run.stdout + run.stderr
    assert json.loads(run.stdout)["proposed_fields"]


def test_doctor_reports_packages(cli):
    code, out = cli("doctor")
    assert out["python_ok"] is True
    assert set(out["packages"]) >= {"python-docx", "docxtpl", "lxml", "pydantic"}
    assert code == (0 if out["ok"] else 1)


@pytest.mark.parametrize("skill", SKILLS, ids=lambda p: p.name)
def test_skill_frontmatter_and_size(skill):
    text = (skill / "SKILL.md").read_text(encoding="utf-8")
    front = re.match(r"^---\n(.*?)\n---\n", text, re.S)
    assert front, "SKILL.md needs YAML frontmatter"
    name = re.search(r"^name: (.+)$", front.group(1), re.M).group(1).strip()
    description = re.search(r"^description: (.+)$", front.group(1), re.M).group(1).strip()
    assert name == skill.name
    assert re.fullmatch(r"[a-z0-9-]{1,64}", name)
    assert 0 < len(description) <= 1024
    assert len(text.splitlines()) < 500


@pytest.mark.parametrize("skill", SKILLS, ids=lambda p: p.name)
def test_skill_mentions_only_real_commands_and_files(skill):
    commands = set(build_parser()._subparsers._group_actions[0].choices)  # noqa: SLF001
    docs = [skill / "SKILL.md", *sorted((skill / "references").glob("*.md"))]
    used: set[str] = set()
    for doc in docs:
        text = doc.read_text(encoding="utf-8")
        used |= set(re.findall(r"\bdocforge ([a-z][a-z-]+)", text))
        for ref in re.findall(r"`(references/[\w.-]+)`", text):
            assert (skill / ref).is_file(), f"{doc.name}: {ref} is referenced but missing"
    assert used, "the skill should show how to run the toolkit"
    assert used <= commands, f"unknown commands: {used - commands}"
    # Every workflow the SKILL.md routes to exists, and every command is documented.
    assert commands <= used, f"undocumented commands: {commands - used}"


def test_fits_upload_and_directory_limits():
    proc = subprocess.run([sys.executable, str(ROOT / "tools" / "build.py")],
                          capture_output=True, text=True, timeout=120)
    assert proc.returncode == 0, proc.stdout + proc.stderr


def test_manifest_has_directory_fields():
    manifest = json.loads((ROOT / ".claude-plugin" / "plugin.json").read_text())
    assert manifest["name"] == "docforge-live"
    assert manifest["displayName"] == "DocForge.live"
    for key in ("version", "description", "author", "license", "homepage"):
        assert manifest.get(key), key
    for key in ("documentationUrl", "supportUrl", "privacyPolicyUrl", "termsOfServiceUrl"):
        assert manifest[key].startswith("https://"), key
    assert (ROOT / manifest["icon"]).is_file()
    market = json.loads((ROOT / ".claude-plugin" / "marketplace.json").read_text())
    assert market["plugins"][0]["name"] == manifest["name"]
    assert not (ROOT / "bin").exists()


# --- the bundled docxtpl ------------------------------------------------------

FORCE_VENDORED = """
import importlib.abc, importlib.machinery, runpy, sys
VENDOR = sys.argv[1]
class ForceVendored(importlib.abc.MetaPathFinder):
    # Resolve docxtpl only from the bundled folder, hiding any installed copy.
    def find_spec(self, name, path, target=None):
        if name == "docxtpl":
            return importlib.machinery.PathFinder.find_spec(name, [VENDOR])
        return None
sys.meta_path.insert(0, ForceVendored())
sys.argv = sys.argv[2:]
runpy.run_path(sys.argv[0], run_name="__main__")
"""


def _run_vendored(skill: Path, *args) -> dict:
    scripts = skill / "scripts"
    proc = subprocess.run(
        [sys.executable, "-c", FORCE_VENDORED, str(scripts / "_vendor"),
         str(scripts / "docforge_cli.py"), *[str(a) for a in args]],
        capture_output=True, text=True, timeout=120,
    )
    assert proc.returncode == 0, proc.stdout + proc.stderr
    return json.loads(proc.stdout)


def test_bundled_docxtpl_fills_templates(tmp_path):
    skill = ROOT / "skills" / "docforge"
    doctor = _run_vendored(skill, "doctor")
    assert doctor["packages"]["docxtpl"] == "0.20.2 (bundled)"
    assert "docxtpl==0.20.2" not in doctor.get("missing", [])
    _run_vendored(skill, "demo", "--out", tmp_path / "d")
    _run_vendored(skill, "analyze", tmp_path / "d" / "invoice_1.docx",
                  tmp_path / "d" / "invoice_2.docx", "--work", tmp_path / "w")
    built = _run_vendored(skill, "build", "--work", tmp_path / "w", "--name", "Invoice",
                          "--out", tmp_path / "pkg")
    assert built["with_labels_docx"]  # rendering through docxtpl worked
    values = tmp_path / "v.json"
    values.write_text(json.dumps({"values": {"invoice_number": "INV-9", "bill_to": "Acme"}}))
    rendered = _run_vendored(skill, "render", tmp_path / "pkg", "--values", values,
                             "--out", tmp_path / "out.docx")
    assert Path(rendered["output"]).is_file()


def test_bundled_code_matches_its_lock():
    import hashlib

    lock = json.loads((ROOT / "skills" / "docforge" / "scripts" / "_vendor" / "vendor.lock.json").read_text())
    entry = lock["docxtpl"]
    assert entry["modified"] is False and entry["license"] == "LGPL-2.1-only"
    for base in [s / "scripts" / "_vendor" for s in SKILLS]:
        assert (base / entry["license_file"]).is_file()
        for rel, digest in entry["files"].items():
            assert hashlib.sha256((base / rel).read_bytes()).hexdigest() == digest, base / rel


# --- install guidance -----------------------------------------------------------

def test_doctor_installs_into_a_venv_on_managed_pythons(monkeypatch):
    from docforge.toolkit import deps

    monkeypatch.setattr(deps, "missing_requirements", lambda: ["python-docx==1.2.0"])
    monkeypatch.setattr(deps, "_externally_managed", lambda: True)
    out = deps.doctor()
    assert "--system-site-packages" in out["install"]
    assert out["install"].endswith("pip install --quiet python-docx==1.2.0")
    assert out["then_run_with"].endswith(("bin/python", "python.exe"))
    monkeypatch.setattr(deps, "_externally_managed", lambda: False)
    out = deps.doctor()
    assert out["install"].endswith("-m pip install --quiet python-docx==1.2.0")
    assert "then_run_with" not in out


def test_nothing_suggests_breaking_system_packages():
    for path in [*ROOT.glob("skills/*/SKILL.md"), *ROOT.glob("skills/*/references/*.md"),
                 ROOT / "README.md", ROOT / "skills" / "docforge" / "scripts" / "docforge" / "toolkit" / "deps.py"]:
        assert "break-system-packages" not in path.read_text(encoding="utf-8"), path

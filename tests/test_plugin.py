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
    text = (skill / "SKILL.md").read_text(encoding="utf-8")
    commands = set(build_parser()._subparsers._group_actions[0].choices)  # noqa: SLF001
    used = set(re.findall(r"\bdocforge ([a-z][a-z-]+)", text))
    assert used, "the skill should show how to run the toolkit"
    assert used <= commands, f"unknown commands: {used - commands}"
    for ref in re.findall(r"`(references/[\w.-]+)`", text):
        assert (skill / ref).is_file(), f"{ref} is referenced but missing"


def test_manifest_has_directory_fields():
    manifest = json.loads((ROOT / ".claude-plugin" / "plugin.json").read_text())
    assert manifest["name"] == "docforge"
    for key in ("version", "description", "author", "license", "homepage"):
        assert manifest.get(key), key
    for key in ("documentationUrl", "supportUrl", "privacyPolicyUrl", "termsOfServiceUrl"):
        assert manifest[key].startswith("https://"), key
    assert (ROOT / manifest["icon"]).is_file()
    market = json.loads((ROOT / ".claude-plugin" / "marketplace.json").read_text())
    assert market["plugins"][0]["name"] == manifest["name"]
    assert not (ROOT / "bin").exists()

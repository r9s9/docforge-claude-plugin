#!/usr/bin/env python3
"""Copy the engine into each skill, and check the plugin against the directory's limits.

In claude.ai chat, only the loaded skill's own folder is copied into the code
sandbox, so every skill that runs the engine carries its own copy in
``scripts/``. ``engine/`` is the one place to edit; this script mirrors it.

It also checks that bundled third-party code (engine/_vendor) is exactly the
release recorded in vendor.lock.json.

The checks follow Anthropic's plugin pre-submission checklist: every file
under 256 KiB, at most 512 files, only text, image and font files, no OS junk
files or symlinks, and no top-level bin/ (which stops claude.ai and Cowork
from installing the plugin).

Usage:
  python tools/build.py           mirror the engine into the skills, then check
  python tools/build.py --check   fail if a mirror is stale or a limit is broken (CI)
"""

from __future__ import annotations

import argparse
import filecmp
import hashlib
import json
import re
import shutil
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
ENGINE = ROOT / "engine"
SKILLS = ("make-template", "fill-template", "check-document")

# What the mirror copies from engine/ into skills/<skill>/scripts/.
MIRRORED = ("docforge", "docforge_cli.py", "requirements.txt", "_vendor")
VENDOR_LOCK = ENGINE / "_vendor" / "vendor.lock.json"

MAX_FILE_BYTES = 256 * 1024
MAX_FILES = 512
TEXT_EXTENSIONS = {
    ".py", ".md", ".txt", ".json", ".jsonl", ".csv", ".yml", ".yaml", ".toml", ".cfg",
    ".ini", ".sh", ".svg", "",
}
MEDIA_EXTENSIONS = {".png", ".jpg", ".jpeg", ".gif", ".webp", ".ttf", ".otf", ".woff", ".woff2"}
JUNK_NAMES = {".DS_Store", "Thumbs.db", "desktop.ini"}


def _ignore(_dir: str, names: list[str]) -> set[str]:
    return {n for n in names if n in ("__pycache__", ".pytest_cache") or n.endswith(".pyc")}


def _files(base: Path) -> list[Path]:
    return sorted(
        p for p in base.rglob("*")
        if p.is_file() and "__pycache__" not in p.parts and not p.name.endswith(".pyc")
    )


def mirror() -> None:
    for skill in SKILLS:
        dest = ROOT / "skills" / skill / "scripts"
        dest.mkdir(parents=True, exist_ok=True)
        for name in MIRRORED:
            src, out = ENGINE / name, dest / name
            if out.is_dir():
                shutil.rmtree(out)
            elif out.exists():
                out.unlink()
            if src.is_dir():
                shutil.copytree(src, out, ignore=_ignore)
            else:
                shutil.copyfile(src, out)
    print(f"Mirrored the engine into {len(SKILLS)} skills.")


def stale_mirrors() -> list[str]:
    problems = []
    for skill in SKILLS:
        dest = ROOT / "skills" / skill / "scripts"
        for name in MIRRORED:
            src, out = ENGINE / name, dest / name
            if src.is_dir():
                want = {p.relative_to(src) for p in _files(src)}
                have = {p.relative_to(out) for p in _files(out)} if out.is_dir() else set()
                for rel in sorted(want ^ have):
                    problems.append(f"skills/{skill}/scripts/{name}/{rel}: missing or extra")
                for rel in sorted(want & have):
                    if not filecmp.cmp(src / rel, out / rel, shallow=False):
                        problems.append(f"skills/{skill}/scripts/{name}/{rel}: out of date")
            elif not out.is_file() or not filecmp.cmp(src, out, shallow=False):
                problems.append(f"skills/{skill}/scripts/{name}: missing or out of date")
    return problems


def _plugin_files() -> list[Path]:
    """Files that would be committed (the plugin folder is the repo root)."""
    try:
        out = subprocess.run(
            ["git", "-C", str(ROOT), "ls-files", "--cached", "--others", "--exclude-standard", "-z"],
            check=True, capture_output=True, timeout=60,
        ).stdout.decode("utf-8")
        paths = [ROOT / p for p in out.split("\0") if p]
    except (OSError, subprocess.SubprocessError):
        skip = {".git", ".venv", "__pycache__", ".pytest_cache", ".ruff_cache"}
        paths = [p for p in ROOT.rglob("*") if not skip & set(p.relative_to(ROOT).parts)]
    return sorted(p for p in paths if p.exists() or p.is_symlink())


def check_limits() -> list[str]:
    problems = []
    files = _plugin_files()
    if len(files) > MAX_FILES:
        problems.append(f"{len(files)} files; the directory reviews plugins over {MAX_FILES} by hand")
    if (ROOT / "bin").exists():
        problems.append("a top-level bin/ stops claude.ai and Cowork from installing the plugin")
    for path in files:
        rel = path.relative_to(ROOT).as_posix()
        if path.is_symlink():
            problems.append(f"{rel}: symlinks are not accepted")
            continue
        if path.name in JUNK_NAMES or "__MACOSX" in path.parts:
            problems.append(f"{rel}: operating-system junk file")
            continue
        suffix = path.suffix.lower()
        if suffix in MEDIA_EXTENSIONS:
            continue
        if suffix not in TEXT_EXTENSIONS:
            problems.append(f"{rel}: {suffix} files are held for manual review")
            continue
        data = path.read_bytes()
        if len(data) > MAX_FILE_BYTES:
            problems.append(f"{rel}: {len(data) // 1024} KiB (limit {MAX_FILE_BYTES // 1024} KiB)")
        if b"\0" in data:
            problems.append(f"{rel}: binary content")
    return problems


def check_vendor() -> list[str]:
    """Bundled third-party files are byte-for-byte the locked release (LGPL: unmodified)."""
    if not VENDOR_LOCK.is_file():
        return [f"{VENDOR_LOCK.relative_to(ROOT)} is missing"]
    problems = []
    base = VENDOR_LOCK.parent
    for name, entry in json.loads(VENDOR_LOCK.read_text(encoding="utf-8")).items():
        if not (base / entry["license_file"]).is_file():
            problems.append(f"{name}: license file {entry['license_file']} is missing")
        for rel, digest in entry["files"].items():
            path = base / rel
            if not path.is_file():
                problems.append(f"engine/_vendor/{rel}: missing")
            elif hashlib.sha256(path.read_bytes()).hexdigest() != digest:
                problems.append(f"engine/_vendor/{rel}: differs from {name} {entry['version']}")
        on_disk = {p.relative_to(base).as_posix() for p in (base / name).rglob("*.py")}
        for rel in sorted(on_disk - set(entry["files"])):
            problems.append(f"engine/_vendor/{rel}: not in vendor.lock.json")
    return problems


def check_pins() -> list[str]:
    """requirements.txt and toolkit/deps.py name the same versions."""
    sys.path.insert(0, str(ENGINE))
    try:
        from docforge.toolkit.deps import REQUIRED
    finally:
        sys.path.pop(0)
    pins = {}
    for line in (ENGINE / "requirements.txt").read_text(encoding="utf-8").splitlines():
        m = re.match(r"^\s*([A-Za-z0-9_.-]+)==([^\s#]+)", line)
        if m:
            pins[m.group(1).lower()] = m.group(2)
    problems = []
    for dist, _minimum, pinned in REQUIRED.values():
        if pins.get(dist.lower()) != pinned:
            problems.append(f"requirements.txt pins {dist}=={pins.get(dist.lower())}, deps.py says {pinned}")
    return problems


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    parser.add_argument("--check", action="store_true", help="check only; change nothing")
    args = parser.parse_args(argv)
    if not args.check:
        mirror()
    problems = check_pins() + check_vendor() + stale_mirrors() + check_limits()
    if problems:
        print("Plugin checks failed:\n  " + "\n  ".join(problems), file=sys.stderr)
        if args.check and any("out of date" in p or "missing or extra" in p for p in problems):
            print("Run `python tools/build.py` to refresh the skill copies.", file=sys.stderr)
        return 1
    print(f"Plugin checks passed ({len(_plugin_files())} files).")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

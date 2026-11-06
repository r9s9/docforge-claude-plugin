#!/usr/bin/env python3
"""Check the plugin against the limits of Claude's apps and Anthropic's directory.

- Bundled third-party code (skills/docforge/scripts/_vendor) is exactly the
  release recorded in vendor.lock.json, unmodified as its license expects.
- requirements.txt and toolkit/deps.py name the same pinned versions.
- The plugin fits Claude's plugin upload: at most 200 entries (files and
  folders) in a zip of the repository, which is the plugin folder.
- Anthropic's pre-submission checklist: every file under 256 KiB, only text,
  image and font files, no OS junk files or symlinks, and no top-level bin/
  (which stops claude.ai and Cowork from installing the plugin).

The engine lives once, in skills/docforge/scripts/, because claude.ai chat
copies only the active skill's folder into the code sandbox.

Usage:
  python tools/build.py                        run the checks
  python tools/build.py --check                the same (kept for CI)
  python tools/build.py --skill-zip FILE.zip   also write the skill on its own, for
                                               claude.ai's Customize > Skills upload
"""

from __future__ import annotations

import argparse
import hashlib
import json
import re
import subprocess
import sys
import zipfile
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SCRIPTS = ROOT / "skills" / "docforge" / "scripts"
VENDOR_LOCK = SCRIPTS / "_vendor" / "vendor.lock.json"

MAX_FILE_BYTES = 256 * 1024
# claude.ai "Upload plugin" refuses larger zips: "Zip contains too many files (maximum 200)".
MAX_ZIP_ENTRIES = 200
TEXT_EXTENSIONS = {
    ".py", ".md", ".txt", ".json", ".jsonl", ".csv", ".yml", ".yaml", ".toml", ".cfg",
    ".ini", ".sh", ".svg", "",
}
MEDIA_EXTENSIONS = {".png", ".jpg", ".jpeg", ".gif", ".webp", ".ttf", ".otf", ".woff", ".woff2"}
JUNK_NAMES = {".DS_Store", "Thumbs.db", "desktop.ini"}


def plugin_files() -> list[Path]:
    """Files that would be committed (the plugin folder is the repo root)."""
    try:
        out = subprocess.run(
            ["git", "-C", str(ROOT), "ls-files", "--cached", "--others", "--exclude-standard", "-z"],
            check=True, capture_output=True, timeout=60,
        ).stdout.decode("utf-8")
        paths = [ROOT / p for p in out.split("\0") if p]
    except (OSError, subprocess.SubprocessError):
        skip = {".git", ".venv", "__pycache__", ".pytest_cache", ".ruff_cache"}
        paths = [
            p for p in ROOT.rglob("*")
            if p.is_file() and not skip & set(p.relative_to(ROOT).parts)
        ]
    return sorted(p for p in paths if p.exists() or p.is_symlink())


def zip_entries(files: list[Path]) -> int:
    """Files plus every folder holding them, plus the top-level folder, as a zip lists them."""
    folders = {"."}
    for path in files:
        for parent in path.relative_to(ROOT).parents:
            folders.add(parent.as_posix())
    return len(files) + len(folders)


def check_limits() -> list[str]:
    problems = []
    files = plugin_files()
    entries = zip_entries(files)
    if entries > MAX_ZIP_ENTRIES:
        problems.append(
            f"a zip of the plugin holds {entries} entries (files and folders); "
            f"Claude's plugin upload accepts at most {MAX_ZIP_ENTRIES}"
        )
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
                problems.append(f"_vendor/{rel}: missing")
            elif hashlib.sha256(path.read_bytes()).hexdigest() != digest:
                problems.append(f"_vendor/{rel}: differs from {name} {entry['version']}")
        on_disk = {p.relative_to(base).as_posix() for p in (base / name).rglob("*.py")}
        for rel in sorted(on_disk - set(entry["files"])):
            problems.append(f"_vendor/{rel}: not in vendor.lock.json")
    return problems


def check_pins() -> list[str]:
    """requirements.txt and toolkit/deps.py name the same versions."""
    sys.path.insert(0, str(SCRIPTS))
    try:
        from docforge.toolkit.deps import REQUIRED
    finally:
        sys.path.pop(0)
    pins = {}
    for line in (SCRIPTS / "requirements.txt").read_text(encoding="utf-8").splitlines():
        m = re.match(r"^\s*([A-Za-z0-9_.-]+)==([^\s#]+)", line)
        if m:
            pins[m.group(1).lower()] = m.group(2)
    problems = []
    for dist, _minimum, pinned in REQUIRED.values():
        if pins.get(dist.lower()) != pinned:
            problems.append(f"requirements.txt pins {dist}=={pins.get(dist.lower())}, deps.py says {pinned}")
    return problems


def write_skill_zip(out: Path) -> int:
    """The skill alone, as Customize > Skills expects: docforge/SKILL.md at the top.

    The repository zip is a plugin (it has .claude-plugin/plugin.json) and goes
    to Customize > Plugins instead. Returns the number of zip entries.
    """
    skill = ROOT / "skills" / "docforge"
    files = [p for p in plugin_files() if skill in p.parents]
    out.parent.mkdir(parents=True, exist_ok=True)
    with zipfile.ZipFile(out, "w", compression=zipfile.ZIP_DEFLATED) as zf:
        for path in files:
            zf.write(path, (Path(skill.name) / path.relative_to(skill)).as_posix())
    return len(files)


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    parser.add_argument("--check", action="store_true", help="same as no flag; kept for CI")
    parser.add_argument("--skill-zip", type=Path, help="write the skill alone as a zip here")
    args = parser.parse_args(argv)
    problems = check_pins() + check_vendor() + check_limits()
    if problems:
        print("Plugin checks failed:\n  " + "\n  ".join(problems), file=sys.stderr)
        return 1
    files = plugin_files()
    print(f"Plugin checks passed ({len(files)} files, {zip_entries(files)} zip entries).")
    if args.skill_zip:
        n = write_skill_zip(args.skill_zip)
        print(f"Wrote {args.skill_zip} ({n} files, top folder docforge/).")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

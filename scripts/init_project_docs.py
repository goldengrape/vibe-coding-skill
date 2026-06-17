#!/usr/bin/env python3
"""Initialize Vibe Coding docs for a new project.

Usage:
    python scripts/init_project_docs.py --target . --level standard --force
"""

from __future__ import annotations

import argparse
import json
import shutil
from datetime import datetime, timezone
from pathlib import Path

LEVELS = {"simple", "standard", "strict"}


def package_root() -> Path:
    return Path(__file__).resolve().parents[1]


def copy_tree(src: Path, dst: Path, force: bool) -> list[str]:
    written: list[str] = []
    for path in src.rglob("*"):
        rel = path.relative_to(src)
        out = dst / rel
        if path.is_dir():
            out.mkdir(parents=True, exist_ok=True)
            continue
        out.parent.mkdir(parents=True, exist_ok=True)
        if out.exists() and not force:
            continue
        shutil.copy2(path, out)
        written.append(str(out))
    return written


def remove_standard_only_files(target: Path, level: str) -> None:
    if level != "simple":
        return
    # In simple mode, keep only the documents needed to avoid early bloat.
    for rel in ["docs/MDD.md", "docs/RMD.md", "okf/log.md"]:
        path = target / rel
        if path.exists():
            path.unlink()


def update_doc_state(target: Path, level: str) -> None:
    path = target / ".vibe" / "doc_state.json"
    if not path.exists():
        return
    data = json.loads(path.read_text(encoding="utf-8"))
    data["document_strength"] = level
    data["last_updated"] = datetime.now(timezone.utc).isoformat()
    path.write_text(json.dumps(data, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")


def render_dynamic_templates(target: Path) -> None:
    now = datetime.now(timezone.utc)
    replacements = {
        "{{DATE}}": now.date().isoformat(),
        "{{TIMESTAMP}}": now.isoformat(),
    }
    for path in target.rglob("*.md"):
        text = path.read_text(encoding="utf-8")
        updated = text
        for old, new in replacements.items():
            updated = updated.replace(old, new)
        if updated != text:
            path.write_text(updated, encoding="utf-8")


def main() -> int:
    parser = argparse.ArgumentParser(description="Initialize project docs/okf/.vibe for a new Vibe Coding project.")
    parser.add_argument("--target", default=".", help="Target project directory")
    parser.add_argument("--level", default="standard", choices=sorted(LEVELS), help="Document strength")
    parser.add_argument("--force", action="store_true", help="Overwrite existing template files")
    args = parser.parse_args()

    target = Path(args.target).resolve()
    target.mkdir(parents=True, exist_ok=True)

    root = package_root()
    templates = root / "templates"
    if not templates.exists():
        raise SystemExit(f"templates directory not found: {templates}")

    written = copy_tree(templates, target, args.force)
    remove_standard_only_files(target, args.level)
    render_dynamic_templates(target)
    update_doc_state(target, args.level)

    print(f"Initialized Vibe Coding docs at: {target}")
    print(f"Document strength: {args.level}")
    print(f"Files written: {len(written)}")
    if args.level == "simple":
        print("Simple mode removed docs/MDD.md and docs/RMD.md. Add them later only if the project needs them.")
    print("Next step: discuss the Idea Brief with the user before creating the Design Split.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

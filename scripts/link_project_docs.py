#!/usr/bin/env python3
"""Append a trace link to .vibe/trace.json and docs/TRACE.md."""

from __future__ import annotations

import argparse
import json
from datetime import datetime, timezone
from pathlib import Path


def load_json(path: Path) -> dict:
    if not path.exists():
        return {"version": 1, "items": [], "links": []}
    return json.loads(path.read_text(encoding="utf-8"))


def save_json(path: Path, data: dict) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(data, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")


def append_markdown_trace(path: Path, source: str, relation: str, target: str, note: str) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    if not path.exists():
        path.write_text("# TRACE — Project Map / Traceability\n\n| Source ID | Relation | Target ID / Path | Notes |\n| --- | --- | --- | --- |\n", encoding="utf-8")
    with path.open("a", encoding="utf-8") as f:
        f.write(f"| {source} | {relation} | {target} | {note} |\n")


def main() -> int:
    parser = argparse.ArgumentParser(description="Append project trace relationship.")
    parser.add_argument("--root", default=".", help="Project root")
    parser.add_argument("--source", required=True, help="Source ID")
    parser.add_argument("--target", required=True, help="Target ID or path")
    parser.add_argument("--relation", required=True, help="Relation, e.g. refines_to, verified_by")
    parser.add_argument("--note", default="", help="Human-readable note")
    args = parser.parse_args()

    root = Path(args.root).resolve()
    trace_json = root / ".vibe" / "trace.json"
    trace_md = root / "docs" / "TRACE.md"

    data = load_json(trace_json)
    now = datetime.now(timezone.utc).isoformat()

    for item_id in [args.source, args.target]:
        if item_id.startswith("wiki/"):
            continue
        if not any(item.get("id") == item_id for item in data.get("items", [])):
            data.setdefault("items", []).append({"id": item_id, "created_at": now})

    link = {
        "source": args.source,
        "relation": args.relation,
        "target": args.target,
        "note": args.note,
        "updated_at": now,
    }
    data.setdefault("links", []).append(link)
    save_json(trace_json, data)
    append_markdown_trace(trace_md, args.source, args.relation, args.target, args.note)

    print(f"Added trace: {args.source} --{args.relation}--> {args.target}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

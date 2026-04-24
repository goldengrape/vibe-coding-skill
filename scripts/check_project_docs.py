#!/usr/bin/env python3
"""Lightweight check for Vibe Coding document health.

Checks:
- required folders/files
- suspicious document bloat
- long wiki pages
- missing trace file
- orphan-like IDs not appearing in trace links
- rough ADD matrix coupling classification hints
"""

from __future__ import annotations

import argparse
import json
import re
import sys
from dataclasses import dataclass
from pathlib import Path

ID_RE = re.compile(r"\b(?:URD|ADD|MDD|TDD|RMD|WIKI|PROB|DEC|PARK)-[A-Z]+-?\d{3}\b")

REQUIRED_STANDARD = [
    "docs/URD.md",
    "docs/ADD.md",
    "docs/MDD.md",
    "docs/TDD.md",
    "docs/RMD.md",
    "docs/TRACE.md",
    "docs/CHANGELOG.md",
    "docs/PARKING_LOT.md",
    "wiki/index.md",
    ".vibe/trace.json",
]

REQUIRED_SIMPLE = [
    "docs/URD.md",
    "docs/ADD.md",
    "docs/TDD.md",
    "docs/TRACE.md",
    "docs/PARKING_LOT.md",
    "wiki/index.md",
    ".vibe/trace.json",
]


@dataclass
class Finding:
    level: str
    path: str
    message: str


def read_text(path: Path) -> str:
    try:
        return path.read_text(encoding="utf-8")
    except UnicodeDecodeError:
        return path.read_text(errors="ignore")


def collect_ids(root: Path) -> dict[str, set[str]]:
    ids: dict[str, set[str]] = {}
    for base in [root / "docs", root / "wiki"]:
        if not base.exists():
            continue
        for path in base.rglob("*.md"):
            text = read_text(path)
            found = set(ID_RE.findall(text))
            if found:
                ids[str(path.relative_to(root))] = found
    return ids


def load_trace(root: Path) -> dict:
    path = root / ".vibe" / "trace.json"
    if not path.exists():
        return {"items": [], "links": []}
    try:
        return json.loads(path.read_text(encoding="utf-8"))
    except json.JSONDecodeError:
        return {"items": [], "links": [], "_error": "invalid json"}


def check_required(root: Path, level: str, findings: list[Finding]) -> None:
    required = REQUIRED_SIMPLE if level == "simple" else REQUIRED_STANDARD
    for rel in required:
        if not (root / rel).exists():
            findings.append(Finding("error", rel, "required file is missing"))


def check_doc_bloat(root: Path, findings: list[Finding]) -> None:
    limits = {
        "docs/URD.md": 260,
        "docs/ADD.md": 260,
        "docs/MDD.md": 320,
        "docs/TDD.md": 320,
        "docs/RMD.md": 240,
    }
    for rel, limit in limits.items():
        path = root / rel
        if path.exists():
            lines = read_text(path).splitlines()
            if len(lines) > limit:
                findings.append(Finding("warn", rel, f"document has {len(lines)} lines; run Ockham check and remove repetition"))


def check_wiki(root: Path, findings: list[Finding]) -> None:
    wiki = root / "wiki"
    if not wiki.exists():
        return
    for path in wiki.rglob("*.md"):
        rel = str(path.relative_to(root))
        lines = read_text(path).splitlines()
        if len(lines) > 120:
            findings.append(Finding("warn", rel, f"wiki page has {len(lines)} lines; split into focused pages"))
        text = "\n".join(lines).lower()
        if "source_ids" not in text and path.name != "index.md":
            findings.append(Finding("warn", rel, "wiki page lacks source_ids; derived pages should cite source IDs"))


def check_trace(root: Path, findings: list[Finding]) -> None:
    ids_by_path = collect_ids(root)
    all_ids = set().union(*ids_by_path.values()) if ids_by_path else set()
    trace = load_trace(root)
    if trace.get("_error"):
        findings.append(Finding("error", ".vibe/trace.json", "invalid JSON"))
        return
    linked = set()
    for link in trace.get("links", []):
        if isinstance(link, dict):
            linked.add(str(link.get("source", "")))
            linked.add(str(link.get("target", "")))
    for item in trace.get("items", []):
        if isinstance(item, dict):
            linked.add(str(item.get("id", "")))
    # Ignore placeholders in untouched templates.
    for item_id in sorted(all_ids):
        if item_id.endswith("999") or item_id.startswith("PARK-"):
            continue
        if item_id not in linked:
            findings.append(Finding("warn", "docs/TRACE.md", f"ID appears in docs/wiki but not in .vibe trace: {item_id}"))


def parse_add_matrix(root: Path, findings: list[Finding]) -> None:
    path = root / "docs" / "ADD.md"
    if not path.exists():
        return
    text = read_text(path)
    if "## FR / DP Design Matrix" not in text:
        findings.append(Finding("error", "docs/ADD.md", "missing FR / DP Design Matrix section"))
        return
    lower = text.lower()
    if "classification:" not in lower:
        findings.append(Finding("warn", "docs/ADD.md", "missing matrix classification"))
    if "coupled" in lower and "accepted coupling" not in lower:
        findings.append(Finding("warn", "docs/ADD.md", "coupling mentioned without Accepted Coupling section"))


def check_ockham_smells(root: Path, findings: list[Finding]) -> None:
    smell_terms = [
        "未来可能",
        "以后可以",
        "nice to have",
        "later we can",
        "TBD TBD",
    ]
    for base in [root / "docs", root / "wiki"]:
        if not base.exists():
            continue
        for path in base.rglob("*.md"):
            text = read_text(path)
            rel = str(path.relative_to(root))
            for term in smell_terms:
                if term in text and "PARKING_LOT" not in rel:
                    findings.append(Finding("info", rel, f"possible future-scope content found: {term!r}"))


def print_findings(findings: list[Finding]) -> None:
    if not findings:
        print("Project doc check passed: no findings.")
        return
    for f in findings:
        print(f"[{f.level}] {f.path}: {f.message}")


def main() -> int:
    parser = argparse.ArgumentParser(description="Check project docs/wiki/trace.")
    parser.add_argument("--root", default=".", help="Project root")
    parser.add_argument("--level", choices=["simple", "standard", "strict"], default=None, help="Document strength")
    args = parser.parse_args()

    root = Path(args.root).resolve()
    level = args.level
    if level is None:
        state = root / ".vibe" / "doc_state.json"
        if state.exists():
            try:
                level = json.loads(state.read_text(encoding="utf-8")).get("document_strength", "standard")
            except json.JSONDecodeError:
                level = "standard"
        else:
            level = "standard"

    findings: list[Finding] = []
    check_required(root, level, findings)
    check_doc_bloat(root, findings)
    check_wiki(root, findings)
    check_trace(root, findings)
    parse_add_matrix(root, findings)
    check_ockham_smells(root, findings)

    print_findings(findings)
    return 1 if any(f.level == "error" for f in findings) else 0


if __name__ == "__main__":
    raise SystemExit(main())

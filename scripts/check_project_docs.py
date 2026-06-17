#!/usr/bin/env python3
"""Lightweight check for Vibe Coding document and OKF bundle health.

Checks:
- required folders/files
- suspicious document bloat
- OKF v0.1 reserved files: index.md and log.md
- OKF concept frontmatter and required type
- common OKF recommended fields and soft guidance
- missing trace file
- orphan-like IDs not appearing in trace links
- rough ADD matrix coupling classification hints
"""

from __future__ import annotations

import argparse
import json
import re
from dataclasses import dataclass
from datetime import datetime
from pathlib import Path
from typing import Any
from urllib.parse import urlparse

try:  # PyYAML is optional; OKF itself does not require dedicated tooling.
    import yaml  # type: ignore[import-untyped]
except Exception:  # pragma: no cover - depends on host environment
    yaml = None

ID_RE = re.compile(
    r"\b(?:URD|ADD|MDD|TDD|RMD)-[A-Z]+-?\d{3}\b"
    r"|\b(?:OKF-PAGE|PROB|DEC|PARK)-\d{3}\b"
)
MARKDOWN_LINK_RE = re.compile(r"(?<!!)\[[^\]]+\]\(([^)]+)\)")
DATE_HEADING_RE = re.compile(r"^##\s+(\d{4}-\d{2}-\d{2})\s*$", re.MULTILINE)
ISO_DATE_RE = re.compile(r"^\d{4}-\d{2}-\d{2}$")

REQUIRED_STANDARD = [
    "docs/URD.md",
    "docs/ADD.md",
    "docs/MDD.md",
    "docs/TDD.md",
    "docs/RMD.md",
    "docs/TRACE.md",
    "docs/CHANGELOG.md",
    "docs/PARKING_LOT.md",
    "okf/index.md",
    ".vibe/trace.json",
]

REQUIRED_SIMPLE = [
    "docs/URD.md",
    "docs/ADD.md",
    "docs/TDD.md",
    "docs/TRACE.md",
    "docs/PARKING_LOT.md",
    "okf/index.md",
    ".vibe/trace.json",
]

RESERVED_OKF_NAMES = {"index.md", "log.md"}


@dataclass
class Finding:
    level: str
    path: str
    message: str


@dataclass
class Frontmatter:
    raw: str
    body: str
    data: dict[str, Any] | None
    parse_error: str | None = None


def read_text(path: Path) -> str:
    try:
        return path.read_text(encoding="utf-8")
    except UnicodeDecodeError:
        return path.read_text(errors="ignore")


def split_frontmatter(text: str) -> Frontmatter | None:
    """Return YAML frontmatter and body if the file starts with a block."""
    lines = text.splitlines()
    if not lines or lines[0].strip() != "---":
        return None
    for index, line in enumerate(lines[1:], start=1):
        if line.strip() == "---":
            raw = "\n".join(lines[1:index])
            body = "\n".join(lines[index + 1 :])
            try:
                data = parse_frontmatter(raw)
                parse_error = None
            except Exception as exc:
                data = None
                parse_error = f"OKF frontmatter is not parseable YAML: {exc}"
            return Frontmatter(raw=raw, body=body, data=data, parse_error=parse_error)
    return Frontmatter(raw="\n".join(lines[1:]), body="", data=None, parse_error="missing closing frontmatter delimiter")


def parse_frontmatter(raw: str) -> dict[str, Any] | None:
    if yaml is not None:
        loaded = yaml.safe_load(raw)  # type: ignore[no-untyped-call]
        if loaded is None:
            return {}
        if isinstance(loaded, dict):
            return loaded
        raise ValueError("frontmatter must be a YAML mapping")

    # Fallback parser for the common scalar/list keys used by this skill.
    data: dict[str, Any] = {}
    current_list_key: str | None = None
    for line in raw.splitlines():
        stripped = line.strip()
        if not stripped or stripped.startswith("#"):
            continue
        if stripped.startswith("-") and current_list_key:
            data.setdefault(current_list_key, []).append(stripped[1:].strip().strip('"\''))
            continue
        current_list_key = None
        if ":" not in line:
            continue
        key, value = line.split(":", 1)
        key = key.strip()
        value = value.strip()
        if value == "":
            data[key] = []
            current_list_key = key
        elif value.startswith("[") and value.endswith("]"):
            inner = value[1:-1].strip()
            data[key] = [item.strip().strip('"\'') for item in inner.split(",") if item.strip()]
        else:
            data[key] = value.strip('"\'')
    return data


def collect_ids(root: Path) -> dict[str, set[str]]:
    ids: dict[str, set[str]] = {}
    for base in [root / "docs", root / "okf"]:
        if not base.exists():
            continue
        for path in base.rglob("*.md"):
            text = read_text(path)
            found = set(ID_RE.findall(text))
            if found:
                ids[str(path.relative_to(root))] = found
    return ids


def load_trace(root: Path) -> dict[str, Any]:
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


def check_okf(root: Path, findings: list[Finding]) -> None:
    okf = root / "okf"
    if not okf.exists():
        return
    for path in okf.rglob("*.md"):
        rel = str(path.relative_to(root))
        text = read_text(path)
        lines = text.splitlines()
        if len(lines) > 120 and path.name not in RESERVED_OKF_NAMES:
            findings.append(Finding("warn", rel, f"OKF concept page has {len(lines)} lines; split into focused pages"))
        if path.name == "index.md":
            check_okf_index(root, path, text, findings)
            continue
        if path.name == "log.md":
            check_okf_log(path, text, root, findings)
            continue
        check_okf_concept(root, path, text, findings)


def check_okf_index(root: Path, path: Path, text: str, findings: list[Finding]) -> None:
    rel = str(path.relative_to(root))
    fm = split_frontmatter(text)
    is_root_index = path == root / "okf" / "index.md"
    body = text
    if fm is not None:
        body = fm.body
        if fm.parse_error:
            findings.append(Finding("error", rel, fm.parse_error))
            return
        if not is_root_index:
            findings.append(Finding("error", rel, "OKF directory index.md must not use frontmatter"))
        else:
            data = fm.data or {}
            unknown = set(data) - {"okf_version"}
            if unknown:
                findings.append(Finding("warn", rel, "root OKF index frontmatter should only declare okf_version"))
            if data.get("okf_version") != "0.1":
                findings.append(Finding("warn", rel, "root OKF index should declare okf_version: \"0.1\""))
    elif is_root_index:
        findings.append(Finding("warn", rel, "root OKF index may declare okf_version: \"0.1\""))
    has_local_concepts = any(
        child.is_file() and child.suffix == ".md" and child.name not in RESERVED_OKF_NAMES
        for child in path.parent.iterdir()
    )
    has_subdirs = any(child.is_dir() for child in path.parent.iterdir())
    if body.strip() and "[" not in body and (is_root_index or has_local_concepts or has_subdirs):
        findings.append(Finding("warn", rel, "OKF index should list linked entries for progressive disclosure"))
    check_markdown_links(root, path, body, findings)
    check_citations(path, body, root, findings)


def check_okf_log(path: Path, text: str, root: Path, findings: list[Finding]) -> None:
    rel = str(path.relative_to(root))
    if split_frontmatter(text) is not None:
        findings.append(Finding("error", rel, "OKF log.md is reserved and must not use concept frontmatter"))
    dates = DATE_HEADING_RE.findall(text)
    bad_heading = [line for line in text.splitlines() if line.startswith("## ") and not ISO_DATE_RE.match(line[3:].strip())]
    for line in bad_heading:
        findings.append(Finding("error", rel, f"log.md date heading must use YYYY-MM-DD: {line}"))
    if text.strip() and not dates:
        findings.append(Finding("warn", rel, "log.md should contain date-grouped entries with ## YYYY-MM-DD headings"))
    parsed = [datetime.fromisoformat(date).date() for date in dates]
    if parsed != sorted(parsed, reverse=True):
        findings.append(Finding("warn", rel, "log.md entries should be newest first"))


def check_okf_concept(root: Path, path: Path, text: str, findings: list[Finding]) -> None:
    rel = str(path.relative_to(root))
    concept_id = str(path.relative_to(root / "okf")).removesuffix(".md")
    fm = split_frontmatter(text)
    if fm is None:
        findings.append(Finding("error", rel, "OKF concept page must start with YAML frontmatter"))
        return
    if fm.parse_error:
        findings.append(Finding("error", rel, fm.parse_error))
        return
    try:
        data = fm.data if fm.data is not None else parse_frontmatter(fm.raw)
    except Exception as exc:
        findings.append(Finding("error", rel, f"OKF concept frontmatter is not parseable YAML: {exc}"))
        return
    if not isinstance(data, dict):
        findings.append(Finding("error", rel, "OKF concept frontmatter must be a YAML mapping"))
        return

    concept_type = data.get("type")
    if not isinstance(concept_type, str) or not concept_type.strip():
        findings.append(Finding("error", rel, "OKF concept frontmatter must include a non-empty type field"))
    for key in ["title", "description"]:
        value = data.get(key)
        if value is not None and (not isinstance(value, str) or not value.strip()):
            findings.append(Finding("warn", rel, f"OKF {key} should be a non-empty string when present"))
    if "tags" in data and not isinstance(data.get("tags"), list):
        findings.append(Finding("warn", rel, "OKF tags should be a YAML list"))
    if "timestamp" in data and not looks_like_iso_datetime(data.get("timestamp")):
        findings.append(Finding("warn", rel, "OKF timestamp should be an ISO 8601 datetime"))
    if "source_ids" not in data:
        findings.append(Finding("warn", rel, "derived OKF concept should cite source_ids"))
    if " " in concept_id:
        findings.append(Finding("warn", rel, "concept ID contains spaces; prefer portable path slugs"))
    check_markdown_links(root, path, fm.body, findings)
    check_citations(path, fm.body, root, findings)


def looks_like_iso_datetime(value: Any) -> bool:
    if isinstance(value, datetime):
        return True
    if not isinstance(value, str):
        return False
    candidate = value.strip().replace("Z", "+00:00")
    try:
        datetime.fromisoformat(candidate)
        return True
    except ValueError:
        return False


def check_markdown_links(root: Path, path: Path, body: str, findings: list[Finding]) -> None:
    okf_root = root / "okf"
    rel = str(path.relative_to(root))
    for raw_target in MARKDOWN_LINK_RE.findall(body):
        target = raw_target.split("#", 1)[0].strip()
        if not target or urlparse(target).scheme or target.startswith("mailto:"):
            continue
        if not target.endswith(".md") and ".md" not in target:
            continue
        resolved = (okf_root / target.lstrip("/")) if target.startswith("/") else (path.parent / target)
        if not resolved.resolve().is_relative_to(okf_root.resolve()):
            findings.append(Finding("warn", rel, f"OKF internal link points outside the bundle: {raw_target}"))
            continue
        if not resolved.exists():
            # OKF consumers must tolerate broken links, so this is intentionally a warning.
            findings.append(Finding("warn", rel, f"OKF internal link target does not exist yet: {raw_target}"))


def check_citations(path: Path, body: str, root: Path, findings: list[Finding]) -> None:
    rel = str(path.relative_to(root))
    external_urls = [target for target in MARKDOWN_LINK_RE.findall(body) if urlparse(target).scheme in {"http", "https"}]
    if external_urls and "# Citations" not in body:
        findings.append(Finding("warn", rel, "external claims should be collected under a # Citations section when they support body text"))


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
            findings.append(Finding("warn", "docs/TRACE.md", f"ID appears in docs/okf but not in .vibe trace: {item_id}"))


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
    for base in [root / "docs", root / "okf"]:
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
    for finding in findings:
        print(f"[{finding.level}] {finding.path}: {finding.message}")


def main() -> int:
    parser = argparse.ArgumentParser(description="Check project docs/okf/trace.")
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
    check_okf(root, findings)
    check_trace(root, findings)
    parse_add_matrix(root, findings)
    check_ockham_smells(root, findings)

    print_findings(findings)
    return 1 if any(finding.level == "error" for finding in findings) else 0


if __name__ == "__main__":
    raise SystemExit(main())

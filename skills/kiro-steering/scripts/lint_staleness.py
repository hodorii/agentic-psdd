from __future__ import annotations

import argparse
import re
from datetime import date
from pathlib import Path

from lint_findings import ERROR, WARNING, Finding, markdown_files_under, read_lines, relative_path
from lint_value_chain import Node

DATE_PATTERN = re.compile(r"^(\d{4})-(\d{2})-(\d{2})(?:[T ].*)?$")
FRONT_MATTER_DATE_PATTERN = re.compile(r"^updated_at:\s*(?P<value>.*?)\s*$")
PLACEHOLDER_PREFIX = "<"


def parse_date(text: str) -> date | None:
    match = DATE_PATTERN.match(text.strip())
    if not match:
        return None
    try:
        return date(int(match[1]), int(match[2]), int(match[3]))
    except ValueError:
        return None


def judge_date(text: str, asof: date, max_age_days: int) -> tuple[str, str] | None:
    parsed = parse_date(text)
    if parsed is None:
        return ERROR, f"date must be YYYY-MM-DD, found '{text}'"
    age_days = (asof - parsed).days
    if age_days > max_age_days:
        return WARNING, f"{text} is {age_days} days before {asof.isoformat()} (limit {max_age_days})"
    return None


def front_matter_updated_at(lines: list[str]) -> tuple[int, str] | None:
    if not lines or lines[0].strip() != "---":
        return None
    for number, line in enumerate(lines[1:], start=2):
        if line.strip() == "---":
            return None
        match = FRONT_MATTER_DATE_PATTERN.match(line)
        if match:
            return number, match["value"]
    return None


def check_file_staleness(steering: Path, root: Path, asof: date, max_age_days: int) -> list[Finding]:
    findings = []
    for path in markdown_files_under(steering):
        found = front_matter_updated_at(read_lines(path))
        if not found or found[1].startswith(PLACEHOLDER_PREFIX):
            continue
        verdict = judge_date(found[1], asof, max_age_days)
        if verdict:
            rule = "date-format" if verdict[0] == ERROR else "stale-file"
            findings.append(Finding(relative_path(path, root), found[0], verdict[0], rule, f"updated_at {verdict[1]}"))
    return findings


def check_node_staleness(nodes: list[Node], value_chain_path: Path, root: Path, asof: date, max_age_days: int) -> list[Finding]:
    findings = []
    for node in nodes:
        text = node.tag("asof")
        verdict = judge_date(text, asof, max_age_days) if text is not None else None
        if verdict:
            rule = "date-format" if verdict[0] == ERROR else "stale-node"
            findings.append(Finding(relative_path(value_chain_path, root), node.line, verdict[0], rule, f"{node.id} asof {verdict[1]}"))
    return findings


def check_staleness(nodes: list[Node], steering: Path, root: Path, asof: date, max_age_days: int) -> list[Finding]:
    findings = check_file_staleness(steering, root, asof, max_age_days)
    return findings + check_node_staleness(nodes, steering / "value-chain.md", root, asof, max_age_days)


def parse_asof(text: str) -> date:
    parsed = parse_date(text)
    if parsed is None or len(text) != len("YYYY-MM-DD"):
        raise argparse.ArgumentTypeError(f"must be YYYY-MM-DD, found '{text}'")
    return parsed

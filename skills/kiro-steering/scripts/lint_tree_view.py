from __future__ import annotations

import re
from collections import Counter
from pathlib import Path

from lint_findings import ERROR, Finding, markdown_files_under, read_lines, relative_path
from lint_business_rules import BR_DEFINITION_PATTERN

TREE_VIEW_DIRECTORY = Path(".kiro") / "reference" / "biz-process-tree"
PROCESS_ID_PATTERN = r"BP-[A-Za-z0-9-]+(?:\.[AFS]\d+)*"
RULE_ID_PATTERN = r"BR-[A-Za-z0-9-]+-\d{3}"
RULE_TOKEN_PATTERN = r"BR-[A-Za-z0-9-]+"
TRAILING_MARKER_PATTERN = re.compile(r"\s*(?:\[[0-9.,~ ]+\]|\u26a0.*|\u2192\s*\S+)$")
HEADING_ID_PATTERN = re.compile(rf"^#+ L[1-4] [^:]*:.*\(({PROCESS_ID_PATTERN})[;)]")
VIEW_PROCESS_PATTERN = re.compile(rf"[▣■□●]\s+({PROCESS_ID_PATTERN})(?![A-Za-z0-9.-])")
VIEW_RULE_PATTERN = re.compile(rf"◆\s+({RULE_TOKEN_PATTERN})(?![A-Za-z0-9-])")
DETAIL_HEADING_PATTERN = re.compile(r"^#+ L5 DetailStep:\s*(.+?)\s*$")
VIEW_DETAIL_PATTERN = re.compile(rf"[\u25b6\u25c6]\s+(?!{RULE_TOKEN_PATTERN}(?![A-Za-z0-9-]))(\S.*?)\s*$")


def source_ids(biz_process: Path) -> set[str]:
    ids = set()
    for line in read_lines(biz_process):
        match = HEADING_ID_PATTERN.match(line) or BR_DEFINITION_PATTERN.match(line)
        if match:
            ids.add(match[1])
    return ids


def view_ids(view: Path) -> dict[str, int]:
    ids: dict[str, int] = {}
    for number, line in enumerate(read_lines(view), start=1):
        for pattern in (VIEW_PROCESS_PATTERN, VIEW_RULE_PATTERN):
            for match in pattern.finditer(line):
                ids.setdefault(match[1], number)
    return ids


def check_tree_views(root: Path, specs: Path) -> list[Finding]:
    findings = []
    for view in markdown_files_under(root / TREE_VIEW_DIRECTORY):
        shown_path = relative_path(view, root)
        biz_process = specs / view.stem / "biz-process.md"
        if not biz_process.is_file():
            findings.append(Finding(shown_path, 1, ERROR, "tree-source-missing", f"no {relative_path(biz_process, root)} for this view"))
            continue
        expected, actual = source_ids(biz_process), view_ids(view)
        findings += [Finding(shown_path, 1, ERROR, "tree-id-missing", f"{identifier} is in biz-process.md but not in the view") for identifier in sorted(expected - actual.keys())]
        findings += check_detail_names(shown_path, biz_process, view)
        findings += [Finding(shown_path, actual[identifier], ERROR, "tree-id-extra", f"{identifier} is in the view but not in biz-process.md") for identifier in sorted(actual.keys() - expected)]
    return findings


def source_detail_names(biz_process: Path) -> Counter:
    matches = (DETAIL_HEADING_PATTERN.match(line) for line in read_lines(biz_process))
    return Counter(match[1] for match in matches if match)


def strip_trailing_markers(text: str) -> str:
    stripped = TRAILING_MARKER_PATTERN.sub("", text)
    return stripped if stripped == text else strip_trailing_markers(stripped)


def view_detail_names(view: Path) -> dict[str, list[int]]:
    names: dict[str, list[int]] = {}
    for number, line in enumerate(read_lines(view), start=1):
        match = VIEW_DETAIL_PATTERN.search(line)
        if match:
            names.setdefault(strip_trailing_markers(match[1]), []).append(number)
    return names


def check_detail_names(shown_path: str, biz_process: Path, view: Path) -> list[Finding]:
    expected, actual = source_detail_names(biz_process), view_detail_names(view)
    findings = []
    for name in sorted(set(expected) | set(actual)):
        shown = len(actual.get(name, []))
        if shown < expected[name]:
            findings.append(Finding(shown_path, 1, ERROR, "tree-detail-step-missing", f"L5 DetailStep '{name}' appears {shown} of {expected[name]} times in the view"))
        elif shown > expected[name]:
            findings.append(Finding(shown_path, actual[name][expected[name]], ERROR, "tree-detail-step-extra", f"'{name}' appears {shown} times in the view but {expected[name]} in biz-process.md"))
    return findings

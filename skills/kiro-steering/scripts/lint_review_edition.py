from __future__ import annotations

import re
from pathlib import Path

from lint_findings import ERROR, Finding, read_lines, relative_path

DECLARATION_PATTERN = re.compile(r"^<!--\s*derived-from:\s*([^/\s]+\.md)\s*(?:;\s*omitted:\s*([^>]*?))?\s*-->\s*$")
DECISION_PATTERN = re.compile(r"^\s*(?:[-*+]\s+|\d+[.)]\s+|\|\s*)(?:\*\*)?(D\d+)(?![A-Za-z0-9])")
ID_LIST_TAIL_PATTERN = re.compile(r"^(?:\*\*)?\s*[,~]\s*(?:\*\*)?D\d")
OMITTED_SEPARATOR_PATTERN = re.compile(r"[,;\s]+")
DECISION_TOKEN_PATTERN = re.compile(r"^D\d+$")
FENCE_PATTERN = re.compile(r"^\s*(`{3,}|~{3,})")


def readable_lines(path: Path) -> list[str] | None:
    try:
        return read_lines(path)
    except (OSError, UnicodeDecodeError):
        return None


def lines_outside_fences(path: Path) -> list[tuple[int, str]]:
    kept, open_fence = [], ""
    for number, line in enumerate(readable_lines(path) or [], start=1):
        line = line.lstrip("\ufeff")
        fence = FENCE_PATTERN.match(line)
        if open_fence:
            if fence and fence[1][0] == open_fence[0] and len(fence[1]) >= len(open_fence):
                open_fence = ""
        elif fence:
            open_fence = fence[1]
        else:
            kept.append((number, line))
    return kept


def decision_ids(path: Path, is_notice_excluded: bool = False) -> dict[str, int]:
    ids: dict[str, int] = {}
    for number, line in lines_outside_fences(path):
        match = DECISION_PATTERN.match(line)
        if match and not (is_notice_excluded and ID_LIST_TAIL_PATTERN.match(line[match.end(1):])):
            ids.setdefault(match[1], number)
    return ids


def declaration_of(path: Path) -> tuple[int, str, list[str]] | None:
    for number, line in lines_outside_fences(path):
        match = DECLARATION_PATTERN.match(line)
        if match:
            omitted = [token.strip() for token in OMITTED_SEPARATOR_PATTERN.split(match[2] or "") if token]
            return number, match[1], omitted
    return None


def check_edition(edition: Path, spec_dir: Path, project_root: Path) -> list[Finding]:
    declaration = declaration_of(edition)
    if declaration is None:
        return []
    declared_line, source_name, omitted = declaration
    shown_path = relative_path(edition, project_root)
    source = spec_dir / source_name
    if readable_lines(source) is None or source.resolve() == edition.resolve():
        return [Finding(shown_path, declared_line, ERROR, "edition-source-missing", f"derived-from {source_name} is not another file of this spec")]
    original, shown = decision_ids(source), decision_ids(edition, is_notice_excluded=True)
    if not original:
        if not shown and not omitted:
            return []
        return [Finding(shown_path, declared_line, ERROR, "edition-source-unnumbered", f"{source_name} has no decision id D<n>; number its decisions before the edition can be checked")]
    findings = [
        Finding(shown_path, line, ERROR, "edition-decision-extra", f"{identifier} is in the edition but not in {source_name}")
        for identifier, line in shown.items()
        if identifier not in original
    ]
    findings += check_omissions(shown_path, declared_line, source_name, original, shown, omitted)
    return findings


def check_omissions(shown_path: str, declared_line: int, source_name: str, original: dict[str, int], shown: dict[str, int], omitted: list[str]) -> list[Finding]:
    findings = []
    for token in omitted:
        if not DECISION_TOKEN_PATTERN.match(token):
            findings.append(Finding(shown_path, declared_line, ERROR, "edition-omission-invalid", f"omitted entry '{token}' is not a decision id"))
        elif token not in original:
            findings.append(Finding(shown_path, declared_line, ERROR, "edition-omission-invalid", f"omitted {token} is not in {source_name}"))
        elif token in shown:
            findings.append(Finding(shown_path, shown[token], ERROR, "edition-omission-invalid", f"{token} is declared omitted but appears in the edition"))
    declared = set(omitted)
    findings += [
        Finding(shown_path, declared_line, ERROR, "edition-omission-undeclared", f"{identifier} is in {source_name} but neither in the edition nor in the omitted list")
        for identifier in original
        if identifier not in shown and identifier not in declared
    ]
    return findings


def check_review_editions(specs: Path, project_root: Path) -> list[Finding]:
    findings = []
    if specs.is_dir():
        for spec_dir in sorted(p for p in specs.iterdir() if p.is_dir()):
            for edition in sorted(p for p in spec_dir.glob("*.md") if p.is_file()):
                findings += check_edition(edition, spec_dir, project_root)
    return findings

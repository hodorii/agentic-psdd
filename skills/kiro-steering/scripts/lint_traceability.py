from __future__ import annotations

import re
from pathlib import Path

from lint_findings import ERROR, Finding, read_lines, relative_path

CRITERION_PATTERN = re.compile(r"^\s*-\s*(\d+\.\d+)\s*:")
TABLE_ROW_PATTERN = re.compile(r"^\|\s*(\d+\.\d+)\s*\|")
DESIGN_ID_PATTERN = re.compile(r"(\d+)\.(\d+)(?:~\1\.(\d+))?")


def requirement_ids(requirements_path: Path) -> dict[str, int]:
    ids: dict[str, int] = {}
    for number, line in enumerate(read_lines(requirements_path), start=1):
        match = CRITERION_PATTERN.match(line) or TABLE_ROW_PATTERN.match(line)
        if match:
            ids.setdefault(match[1], number)
    return ids


def ids_mentioned(design_path: Path) -> set[str]:
    mentioned = set()
    for line in read_lines(design_path):
        for group, first, last in DESIGN_ID_PATTERN.findall(line):
            end = int(last) if last else int(first)
            mentioned.update(f"{group}.{minor}" for minor in range(int(first), end + 1))
    return mentioned


def check_spec(spec_dir: Path, project_root: Path) -> list[Finding]:
    requirements_path, design_path = spec_dir / "requirements.md", spec_dir / "design.md"
    if not (requirements_path.is_file() and design_path.is_file()):
        return []
    mentioned = ids_mentioned(design_path)
    shown_path = relative_path(requirements_path, project_root)
    return [
        Finding(shown_path, line, ERROR, "requirement-not-in-design", f"{identifier} does not appear in {design_path.name}")
        for identifier, line in requirement_ids(requirements_path).items()
        if identifier not in mentioned
    ]


def check_requirements_traceability(specs: Path, project_root: Path) -> list[Finding]:
    findings = []
    if specs.is_dir():
        for spec_dir in sorted(p for p in specs.iterdir() if p.is_dir()):
            findings.extend(check_spec(spec_dir, project_root))
    return findings

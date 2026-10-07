import unicodedata
from pathlib import Path

from lint_findings import ERROR, Finding, read_lines, relative_path

RULE = "human-typeable"
SUPPRESS_MARKER = "lint-ignore: human-typeable"
CHECKED_SUFFIXES = {".md", ".json"}
ALLOWED_CONTROL_CHARACTERS = {"\t"}
FENCE_MARK = "```"
EXEMPT_FENCE_KINDS = {"quote", "output"}


def is_typeable(character: str) -> bool:
    if character in ALLOWED_CONTROL_CHARACTERS:
        return True
    if ord(character) < 128:
        return character.isprintable()
    return unicodedata.category(character)[0] in {"L", "M"}


def describe(character: str) -> str:
    name = unicodedata.name(character, "UNNAMED")
    return f"U+{ord(character):04X} {name}"


def forbidden_characters(line: str) -> list[str]:
    return [character for character in line if not is_typeable(character)]


def checked_lines(lines: list[str]) -> list[tuple[int, str]]:
    kept, fence_kind = [], None
    for number, line in enumerate(lines, start=1):
        stripped = line.strip()
        if stripped.startswith(FENCE_MARK):
            fence_kind = None if fence_kind is not None else stripped[len(FENCE_MARK):].strip()
            kept.append((number, line))
        elif fence_kind not in EXEMPT_FENCE_KINDS:
            kept.append((number, line))
    return kept


def check_file(path: Path, project_root: Path) -> list[Finding]:
    findings = []
    for line_number, line in checked_lines(read_lines(path)):
        if SUPPRESS_MARKER in line:
            continue
        found = forbidden_characters(line)
        if not found:
            continue
        extra = f" (+{len(found) - 1} more on this line)" if len(found) > 1 else ""
        message = f"{describe(found[0])}{extra}; use words or ASCII"
        findings.append(Finding(relative_path(path, project_root), line_number, ERROR, RULE, message))
    return findings


def files_to_check(targets: list[Path]) -> list[Path]:
    files = []
    for target in targets:
        if target.is_dir():
            files.extend(p for p in sorted(target.rglob("*")) if p.suffix in CHECKED_SUFFIXES)
        elif target.is_file():
            files.append(target)
    return files


def check_human_typeable(targets: list[Path], project_root: Path) -> list[Finding]:
    findings = []
    for path in files_to_check(targets):
        findings.extend(check_file(path, project_root))
    return findings

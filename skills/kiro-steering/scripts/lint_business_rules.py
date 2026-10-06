import re
from pathlib import Path

from lint_findings import ERROR, WARNING, Finding, markdown_files_under, read_lines, relative_path
from lint_value_chain import Node

BP_DEFINITION_PATTERN = re.compile(r"^#+ L1 Process:.*\((BP-[A-Za-z0-9-]+)[;)]")
BR_DEFINITION_PATTERN = re.compile(r"^\s*-\s+(BR-[A-Za-z0-9-]+-\d{3})\s*:")
BR_TOKEN_PATTERN = re.compile(r"BR-[A-Za-z0-9-]+-\d{3}")
TASK_BP_PATTERN = re.compile(r"_BizProcess:\s*(.*)")
BP_TOKEN_PATTERN = re.compile(r"BP-[A-Za-z0-9]+(?:-[A-Za-z0-9]+)*")


def scan_definitions(specs: Path, root: Path) -> tuple[dict[str, tuple[str, int]], dict[str, tuple[str, int]], list[Finding]]:
    processes: dict[str, tuple[str, int]] = {}
    rules: dict[str, tuple[str, int]] = {}
    findings = []
    for path in markdown_files_under(specs, "biz-process.md"):
        shown_path = relative_path(path, root)
        for number, line in enumerate(read_lines(path), start=1):
            for pattern, table, rule in ((BP_DEFINITION_PATTERN, processes, "bp-unique"), (BR_DEFINITION_PATTERN, rules, "br-unique")):
                match = pattern.match(line)
                if not match:
                    continue
                if match[1] in table:
                    findings.append(Finding(shown_path, number, ERROR, rule, f"{match[1]} already defined at {table[match[1]][0]}:{table[match[1]][1]}"))
                table.setdefault(match[1], (shown_path, number))
    return processes, rules, findings


def check_biz_process_refs(units: list[Node], processes: dict[str, tuple[str, int]], root: Path, steering: Path) -> list[Finding]:
    shown_path = relative_path(steering / "value-chain.md", root)
    findings, referenced = [], set()
    for unit in units:
        reference = unit.tag("bizProcessRef") or "gap"
        if reference == "gap":
            continue
        referenced.add(reference)
        if reference not in processes:
            findings.append(Finding(shown_path, unit.line, ERROR, "biz-process-ref", f"{reference} has no L1 Process heading in any biz-process.md"))
    for identifier, (path, line) in processes.items():
        if identifier not in referenced:
            findings.append(Finding(path, line, WARNING, "bp-unused", f"{identifier} is defined but no Unit names it in bizProcessRef"))
    return findings


def check_task_process_tags(specs: Path, processes: dict[str, tuple[str, int]], root: Path) -> list[Finding]:
    findings = []
    for path in markdown_files_under(specs, "tasks.md"):
        for number, line in enumerate(read_lines(path), start=1):
            match = TASK_BP_PATTERN.search(line)
            for token in BP_TOKEN_PATTERN.findall(match[1]) if match else []:
                if token not in processes:
                    findings.append(Finding(relative_path(path, root), number, ERROR, "biz-process-ref", f"{token} has no L1 Process heading in any biz-process.md"))
    return findings


def rule_references(specs: Path) -> list[tuple[Path, int, str]]:
    references = []
    for path in markdown_files_under(specs):
        for number, line in enumerate(read_lines(path), start=1):
            if BR_DEFINITION_PATTERN.match(line):
                continue
            references.extend((path, number, token) for token in BR_TOKEN_PATTERN.findall(line))
    return references


def check_rule_references(specs: Path, rules: dict[str, tuple[str, int]], root: Path) -> list[Finding]:
    findings, referenced = [], set()
    for path, number, token in rule_references(specs):
        referenced.add(token)
        if token not in rules:
            findings.append(Finding(relative_path(path, root), number, ERROR, "br-ref", f"{token} is not defined in any biz-process.md"))
    for identifier, (path, line) in rules.items():
        if identifier not in referenced:
            findings.append(Finding(path, line, WARNING, "br-unused", f"{identifier} is defined but nothing references it"))
    return findings


def check_rule_prefixes(processes: dict[str, tuple[str, int]], rules: dict[str, tuple[str, int]]) -> list[Finding]:
    known_names = {identifier[len("BP-"):] for identifier in processes}
    return [
        Finding(path, line, ERROR, "br-prefix", f"{identifier} must be BR-<x>-<nnn> with a defined BP-<x>")
        for identifier, (path, line) in rules.items()
        if identifier[len("BR-"):].rsplit("-", 1)[0] not in known_names
    ]

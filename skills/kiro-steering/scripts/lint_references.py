from __future__ import annotations

import re
from pathlib import Path

from lint_findings import ERROR, WARNING, Finding, markdown_files_under, read_lines, relative_path
from lint_value_chain import UNIT_LEVEL, Node

KPI_ROW_PATTERN = re.compile(r"^\|\s*(KPI-\d+)\s*\|")
VALUE_CHAIN_TOKEN_PATTERN = re.compile(r"VC-[A-Za-z0-9]+(?:-[A-Za-z0-9]+)*")
LABELLED_TOKEN_PATTERN = re.compile(r"valueChainRef\W{0,4}(VC-[A-Za-z0-9]+(?:-[A-Za-z0-9]+)*)")


def kpi_definitions(product_path: Path) -> dict[str, int]:
    if not product_path.is_file():
        return {}
    definitions = {}
    for number, line in enumerate(read_lines(product_path), start=1):
        match = KPI_ROW_PATTERN.match(line)
        if match:
            definitions.setdefault(match[1], number)
    return definitions


def check_kpi_references(units: list[Node], definitions: dict[str, int], steering: Path, root: Path) -> list[Finding]:
    value_chain_path = relative_path(steering / "value-chain.md", root)
    product_path = relative_path(steering / "product.md", root)
    findings, used = [], set()
    for unit in units:
        for kpi_id in re.findall(r"KPI-\d+", unit.tag("kpi") or ""):
            used.add(kpi_id)
            if kpi_id not in definitions:
                findings.append(Finding(value_chain_path, unit.line, ERROR, "kpi-undefined", f"{kpi_id} is not in the product.md KPI table"))
    for kpi_id, line in definitions.items():
        if kpi_id not in used:
            findings.append(Finding(product_path, line, WARNING, "kpi-unused", f"{kpi_id} is defined but no Unit references it"))
    return findings


def value_chain_references(path: Path) -> list[tuple[int, str]]:
    is_biz_process = path.name == "biz-process.md"
    pattern = VALUE_CHAIN_TOKEN_PATTERN if is_biz_process else LABELLED_TOKEN_PATTERN
    references = []
    for number, line in enumerate(read_lines(path), start=1):
        for match in pattern.finditer(line):
            references.append((number, match.group(match.lastindex or 0)))
    return references


def unit_lookup(nodes: list[Node]) -> tuple[dict[str, Node], dict[str, Node]]:
    by_identifier = {}
    for node in nodes:
        by_identifier[node.id] = node
        for alias in node.tags.get("alias", []):
            by_identifier[alias.strip()] = node
    return by_identifier, {n.id: n for n in nodes if n.level == UNIT_LEVEL}


def check_value_chain_references(nodes: list[Node], specs: Path, root: Path) -> tuple[list[Finding], set[str]]:
    by_identifier, units = unit_lookup(nodes)
    findings, referenced_units = [], set()
    for path in markdown_files_under(specs):
        for line, identifier in value_chain_references(path):
            target = by_identifier.get(identifier)
            if target is not None and target.level == UNIT_LEVEL:
                referenced_units.add(target.id)
                continue
            reason = "is not a Unit id" if target is not None else "is not defined in value-chain.md"
            findings.append(Finding(relative_path(path, root), line, ERROR, "value-chain-ref", f"{identifier} {reason}"))
    return findings, referenced_units


def check_back_links(units: list[Node], referenced_units: set[str], root: Path, steering: Path) -> list[Finding]:
    shown_path = relative_path(steering / "value-chain.md", root)
    return [
        Finding(shown_path, unit.line, WARNING, "back-link", f"{unit.id} names {unit.tag('bizProcessRef')} but no spec points back with valueChainRef")
        for unit in units
        if unit.id not in referenced_units and (unit.tag("bizProcessRef") or "gap") != "gap"
    ]

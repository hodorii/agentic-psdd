#!/usr/bin/env python3
"""Deterministic lint of a project's .kiro steering and specs; see kiro-steering rules/doc-lint.md."""
from __future__ import annotations

import argparse
import sys
from pathlib import Path

import lint_business_rules as business_rules
import lint_references as references
from lint_findings import ERROR, WARNING, Finding
from lint_human_typeable import check_human_typeable
from lint_traceability import check_requirements_traceability
from lint_value_chain import UNIT_LEVEL, check_value_chain


def parse_arguments(argv: list[str]) -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Lint .kiro/steering and .kiro/specs of a project.")
    parser.add_argument("project_root", nargs="?", default=".", type=Path)
    parser.add_argument("--also", action="append", default=[], type=Path, metavar="PATH", help="extra file or directory for the human-typeable check")
    parser.add_argument("--strict", action="store_true", help="exit 1 on warnings too")
    return parser.parse_args(argv)


def check_cross_references(root: Path, steering: Path, specs: Path) -> list[Finding]:
    value_chain_path = steering / "value-chain.md"
    nodes, findings = [], []
    if value_chain_path.is_file():
        nodes, findings = check_value_chain(value_chain_path, root)
    units = [node for node in nodes if node.level == UNIT_LEVEL]
    definitions = references.kpi_definitions(steering / "product.md")
    findings += references.check_kpi_references(units, definitions, steering, root)
    reference_findings, referenced_units = references.check_value_chain_references(nodes, specs, root)
    findings += reference_findings + references.check_back_links(units, referenced_units, root, steering)
    processes, rules, definition_findings = business_rules.scan_definitions(specs, root)
    findings += definition_findings + business_rules.check_biz_process_refs(units, processes, root, steering)
    findings += business_rules.check_task_process_tags(specs, processes, root)
    findings += business_rules.check_rule_references(specs, rules, root) + business_rules.check_rule_prefixes(processes, rules)
    findings += check_requirements_traceability(specs, root)
    return findings


def lint_project(root: Path, extra_targets: list[Path]) -> list[Finding]:
    steering, specs = root / ".kiro" / "steering", root / ".kiro" / "specs"
    findings = check_human_typeable([steering, specs] + extra_targets, root)
    return findings + check_cross_references(root, steering, specs)


def main(argv: list[str]) -> int:
    arguments = parse_arguments(argv)
    root = arguments.project_root.resolve()
    if not (root / ".kiro").is_dir():
        print(f"error: {root} has no .kiro directory", file=sys.stderr)
        return 2
    findings = sorted(lint_project(root, arguments.also), key=lambda f: (f.path, f.line, f.rule))
    for finding in findings:
        print(finding.render())
    errors = sum(1 for f in findings if f.level == ERROR)
    warnings = sum(1 for f in findings if f.level == WARNING)
    print(f"{errors} errors, {warnings} warnings")
    return 1 if errors or (arguments.strict and warnings) else 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))

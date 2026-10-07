import re
from dataclasses import dataclass, field
from pathlib import Path

from lint_findings import ERROR, WARNING, Finding, read_lines, relative_path

NODE_PATTERN = re.compile(r"^(?P<indent> *)- (?P<id>VC-\S+) (?P<rest>.*)$")
ID_SEGMENT_PATTERN = re.compile(r"^[A-Za-z0-9]+$")
KPI_LIST_PATTERN = re.compile(r"^(none|KPI-\d+(\s*,\s*KPI-\d+)*)$")
BIZ_PROCESS_REF_PATTERN = re.compile(r"^(gap|BP-[A-Za-z0-9-]+)$")
PERCENT_NUMBER_PATTERN = re.compile(r"\d+(\.\d+)?\s*%")
LEVEL_NAMES = ["Value", "Mega", "Main", "Unit"]
UNIT_LEVEL = 3
REQUIRED_TAGS_BY_LEVEL = [
    ["evidence"],
    ["kind", "pcf", "evidence"],
    ["pcf", "evidence"],
    ["role", "kpi", "pcf", "evidence", "bizProcessRef"],
]


@dataclass
class Node:
    line: int
    level: int
    id: str
    name: str
    tags: dict[str, list[str]] = field(default_factory=dict)

    def tag(self, key: str) -> str | None:
        values = self.tags.get(key)
        return values[0].strip() if values else None


def split_trailing_group(text: str) -> tuple[str, str]:
    text = text.rstrip()
    if not text.endswith(")"):
        return text, ""
    depth = 0
    for index in range(len(text) - 1, -1, -1):
        depth += {")": 1, "(": -1}.get(text[index], 0)
        if depth == 0:
            return text[:index].rstrip(), text[index + 1 : -1]
    return text, ""


def parse_tags(group: str) -> dict[str, list[str]]:
    tags: dict[str, list[str]] = {}
    for part in group.split(";"):
        key, separator, value = part.partition(":")
        if separator:
            tags.setdefault(key.strip(), []).append(value.strip())
    return tags


def parse_node(line_number: int, match: re.Match) -> Node:
    name, group = split_trailing_group(match["rest"])
    level = len(match["indent"]) // 2
    return Node(line_number, level, match["id"], name, parse_tags(group))


def comment_and_front_matter_free_lines(lines: list[str]) -> list[tuple[int, str]]:
    kept, in_comment, in_front_matter = [], False, False
    for number, line in enumerate(lines, start=1):
        stripped = line.strip()
        if number == 1 and stripped == "---":
            in_front_matter = True
            continue
        if in_front_matter:
            in_front_matter = stripped != "---"
            continue
        if in_comment or stripped.startswith("<!--"):
            in_comment = "-->" not in stripped
            continue
        kept.append((number, line))
    return kept


def check_node_shape(node: Node, parent: Node | None, indent: int) -> list[tuple[str, str]]:
    problems = []
    if indent % 2 or node.level > UNIT_LEVEL:
        problems.append(("tree-level", "indent must be 2 spaces per level, at most 4 levels"))
        return problems
    last_segment = node.id.rsplit("-", 1)[-1]
    if node.level == 0:
        expected_prefix = "VC"
    else:
        expected_prefix = parent.id if parent else ""
    if node.level and not parent:
        problems.append(("tree-level", f"{LEVEL_NAMES[node.level]} has no parent node above it"))
    elif node.id != f"{expected_prefix}-{last_segment}" or not ID_SEGMENT_PATTERN.match(last_segment):
        problems.append(("id-format", f"id must be <parent id>-<one segment of letters and digits>, parent is {expected_prefix}"))
    return problems


def check_node_tags(node: Node) -> list[tuple[str, str]]:
    problems = []
    for key in REQUIRED_TAGS_BY_LEVEL[node.level]:
        if node.tag(key) is None:
            problems.append(("required-tag", f"{LEVEL_NAMES[node.level]} {node.id} lacks tag '{key}'"))
    if node.level == 1 and node.tag("kind") not in (None, "primary", "support"):
        problems.append(("mega-kind", "kind must be primary or support"))
    kpi = node.tag("kpi")
    if kpi is not None and not KPI_LIST_PATTERN.match(kpi):
        problems.append(("kpi-number", f"kpi must be 'none' or KPI ids only, found '{kpi}'"))
    reference = node.tag("bizProcessRef")
    if reference is not None and not BIZ_PROCESS_REF_PATTERN.match(reference):
        problems.append(("biz-process-ref-format", f"bizProcessRef must be 'gap' or a BP id, found '{reference}'"))
    return problems


def collect_nodes_and_prose(lines: list[str]) -> tuple[list[tuple[Node, int]], list[int]]:
    nodes, prose_lines = [], []
    for number, line in comment_and_front_matter_free_lines(lines):
        match = NODE_PATTERN.match(line)
        if match:
            nodes.append((parse_node(number, match), len(match["indent"])))
        elif line.strip() and not line.lstrip().startswith("#"):
            prose_lines.append(number)
    return nodes, prose_lines


def check_node(node: Node, indent: int, parents: dict[int, Node]) -> list[tuple[str, str]]:
    problems = check_node_shape(node, parents.get(node.level - 1), indent)
    problems += check_node_tags(node)
    if PERCENT_NUMBER_PATTERN.search(node.name + " ".join(sum(node.tags.values(), []))):
        problems.append(("kpi-number", "numeric target found; numbers live in the product.md KPI table"))
    return problems


def check_ids_unique(nodes: list[Node]) -> list[tuple[int, str, str]]:
    seen: dict[str, int] = {}
    findings = []
    for node in nodes:
        for identifier in [node.id] + [a.strip() for a in node.tags.get("alias", [])]:
            if identifier in seen:
                findings.append((node.line, "id-unique", f"{identifier} already defined at line {seen[identifier]}"))
            seen.setdefault(identifier, node.line)
    return findings


def check_value_chain(path: Path, project_root: Path) -> tuple[list[Node], list[Finding]]:
    shown_path = relative_path(path, project_root)
    nodes_with_indent, prose_lines = collect_nodes_and_prose(read_lines(path))
    problems: list[tuple[int, str, str, str]] = []
    parents: dict[int, Node] = {}
    for node, indent in nodes_with_indent:
        parents = {level: n for level, n in parents.items() if level < node.level}
        parents[node.level] = node
        problems += [(node.line, ERROR, rule, message) for rule, message in check_node(node, indent, parents)]
    nodes = [node for node, _ in nodes_with_indent]
    problems += [(line, ERROR, rule, message) for line, rule, message in check_ids_unique(nodes)]
    if sum(1 for node in nodes if node.level == 0) != 1:
        problems.append((1, ERROR, "tree-root", "exactly one Value root node is required (table format? see the upgrade path in biz-process rules)"))
    if prose_lines:
        first = prose_lines[0]
        problems.append((first, WARNING, "value-chain-prose", f"{len(prose_lines)} non-tree lines (first here); the file holds only the tree"))
    return nodes, [Finding(shown_path, line, level, rule, message) for line, level, rule, message in problems]

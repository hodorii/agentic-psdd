import shutil
import subprocess
import sys
import tempfile
import unittest
from collections import Counter
from pathlib import Path

HERE = Path(__file__).parent
DOC_LINT = HERE.parents[1] / "skills" / "kiro-steering" / "scripts" / "doc_lint.py"
FIXED_ASOF = "2026-10-10"
sys.path.insert(0, str(DOC_LINT.parent))
from lint_review_edition import check_review_editions  # noqa: E402
PLACEHOLDERS = {"{{MIDDLE_DOT}}": "\u00b7", "{{ARROW}}": "\u2192", "{{SQUARE}}": "\u25a0", "{{BOX_VERTICAL}}": "\u2502"}

EXPECTED_VIOLATION_RULES = Counter({
    ("error", "human-typeable"): 4,
    ("error", "required-tag"): 1,
    ("error", "mega-kind"): 1,
    ("error", "kpi-number"): 2,
    ("error", "id-unique"): 1,
    ("error", "kpi-undefined"): 1,
    ("error", "value-chain-ref"): 1,
    ("error", "biz-process-ref"): 2,
    ("error", "br-ref"): 1,
    ("error", "br-prefix"): 1,
    ("error", "requirement-not-in-design"): 2,
    ("error", "tree-id-missing"): 3,
    ("error", "tree-id-extra"): 2,
    ("error", "tree-detail-step-missing"): 1,
    ("error", "tree-detail-step-extra"): 1,
    ("error", "tree-source-missing"): 1,
    ("error", "edition-source-missing"): 1,
    ("error", "edition-decision-extra"): 1,
    ("error", "edition-omission-undeclared"): 1,
    ("error", "edition-omission-invalid"): 3,
    ("warning", "value-chain-prose"): 1,
    ("warning", "kpi-unused"): 2,
    ("warning", "bp-unused"): 1,
    ("warning", "br-unused"): 2,
    ("warning", "back-link"): 1,
    ("warning", "stale-file"): 1,
    ("warning", "stale-node"): 1,
    ("error", "date-format"): 1,
})


def materialize_fixture(name: str, destination: Path) -> Path:
    project = destination / name
    shutil.copytree(HERE / "fixtures" / name, project)
    for path in project.rglob("*.md"):
        text = path.read_text(encoding="utf-8")
        for placeholder, character in PLACEHOLDERS.items():
            text = text.replace(placeholder, character)
        path.write_text(text, encoding="utf-8")
    return project


def run_lint(project: Path) -> tuple[int, list[str]]:
    result = subprocess.run([sys.executable, str(DOC_LINT), str(project), "--asof", FIXED_ASOF], capture_output=True, text=True, env={"PYTHONDONTWRITEBYTECODE": "1"})
    return result.returncode, result.stdout.splitlines()


def rule_counts(lines: list[str]) -> Counter:
    counts = Counter()
    for line in lines[:-1]:
        level, rule = line.split(": ", 1)[1].split(" ", 2)[:2]
        counts[(level, rule.strip("[]"))] += 1
    return counts


class DocLintFixtures(unittest.TestCase):
    def setUp(self):
        self.workdir = Path(tempfile.mkdtemp())
        self.addCleanup(shutil.rmtree, self.workdir)

    def test_clean_project_has_no_findings(self):
        code, lines = run_lint(materialize_fixture("clean", self.workdir))
        self.assertEqual(code, 0, lines)
        self.assertEqual(lines, ["0 errors, 0 warnings"])

    def test_violations_are_reported_by_rule(self):
        code, lines = run_lint(materialize_fixture("violations", self.workdir))
        self.assertEqual(code, 1)
        actual = rule_counts(lines)
        for key, count in EXPECTED_VIOLATION_RULES.items():
            self.assertEqual(actual[key], count, f"{key}: {lines}")
        self.assertEqual(sum(actual.values()), sum(EXPECTED_VIOLATION_RULES.values()), lines)


class ReviewEditionEdgeCases(unittest.TestCase):
    def setUp(self):
        self.workdir = Path(tempfile.mkdtemp())
        self.addCleanup(shutil.rmtree, self.workdir)
        self.spec = self.workdir / ".kiro" / "specs" / "feature"
        self.spec.mkdir(parents=True)

    def lint_rules(self) -> Counter:
        return rule_counts(run_lint(self.workdir)[1])

    def write(self, name: str, text: str, encoding: str = "utf-8") -> None:
        (self.spec / name).write_bytes(text.encode(encoding))

    def test_unreadable_markdown_is_skipped_by_the_edition_check(self):
        self.write("design.md", "- D1 decision\n")
        self.write("latin.md", "caf\u00e9 - D1\n", "latin-1")
        (self.spec / "folder.md").mkdir()
        self.assertEqual(check_review_editions(self.workdir / ".kiro" / "specs", self.workdir), [])

    def test_numbered_list_bold_and_two_digit_ids_are_read(self):
        self.write("design.md", "1. D1 first\n- **D10 tenth**\n")
        self.write("edition.md", "<!-- derived-from: design.md -->\n| D1 | first |\n| **D10** | tenth |\n")
        self.assertEqual(self.lint_rules(), Counter())

    def test_template_decision_line_with_trailing_citation_is_read(self):
        self.write("design.md", "- **D1 [decision]**: content - reason: one line\n- **D2 [decision]**: other (D1)\nFlow step ends here (D2)\n")
        self.write("edition.md", "<!-- derived-from: design.md; omitted: D2 -->\n- **D1 [decision]**: worded (D1)\n")
        self.assertEqual(self.lint_rules(), Counter())

    def test_prose_line_starting_with_an_id_is_not_a_decision(self):
        self.write("design.md", "- D1 first\nD2 is mentioned in prose\n")
        self.write("edition.md", "<!-- derived-from: design.md -->\n- D1 first\n")
        self.assertEqual(self.lint_rules(), Counter())

    def test_omitted_entries_split_on_spaces_and_commas(self):
        self.write("design.md", "- D1 a\n- D2 b\n- D3 c\n")
        self.write("edition.md", "<!-- derived-from: design.md; omitted: D2 D3 -->\n- D1 a\n")
        self.assertEqual(self.lint_rules(), Counter())

    def test_path_in_derived_from_is_not_a_declaration(self):
        self.write("design.md", "- D1 a\n")
        self.write("edition.md", "<!-- derived-from: ../feature/design.md -->\n- D9 x\n")
        self.assertEqual(self.lint_rules(), Counter())

    def test_unreadable_original_is_reported_as_missing(self):
        self.write("design.md", "caf\u00e9\n", "latin-1")
        self.write("edition.md", "<!-- derived-from: design.md -->\n- D1 a\n")
        findings = check_review_editions(self.workdir / ".kiro" / "specs", self.workdir)
        self.assertEqual([finding.rule for finding in findings], ["edition-source-missing"])


if __name__ == "__main__":
    unittest.main()

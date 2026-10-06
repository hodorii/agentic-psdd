import shutil
import subprocess
import sys
import tempfile
import unittest
from collections import Counter
from pathlib import Path

HERE = Path(__file__).parent
DOC_LINT = HERE.parents[1] / "skills" / "kiro-steering" / "scripts" / "doc_lint.py"
PLACEHOLDERS = {"{{MIDDLE_DOT}}": "\u00b7", "{{ARROW}}": "\u2192"}

EXPECTED_VIOLATION_RULES = Counter({
    ("error", "human-typeable"): 2,
    ("error", "required-tag"): 1,
    ("error", "mega-kind"): 1,
    ("error", "kpi-number"): 2,
    ("error", "id-unique"): 1,
    ("error", "kpi-undefined"): 1,
    ("error", "value-chain-ref"): 1,
    ("error", "biz-process-ref"): 2,
    ("error", "br-ref"): 1,
    ("error", "br-prefix"): 1,
    ("warning", "value-chain-prose"): 1,
    ("warning", "kpi-unused"): 2,
    ("warning", "bp-unused"): 1,
    ("warning", "br-unused"): 2,
    ("warning", "back-link"): 1,
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
    result = subprocess.run([sys.executable, str(DOC_LINT), str(project)], capture_output=True, text=True, env={"PYTHONDONTWRITEBYTECODE": "1"})
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


if __name__ == "__main__":
    unittest.main()

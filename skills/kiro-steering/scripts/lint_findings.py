from dataclasses import dataclass
from pathlib import Path

ERROR = "error"
WARNING = "warning"


@dataclass(frozen=True)
class Finding:
    path: str
    line: int
    level: str
    rule: str
    message: str

    def render(self) -> str:
        return f"{self.path}:{self.line}: {self.level} [{self.rule}] {self.message}"


def relative_path(path: Path, project_root: Path) -> str:
    try:
        return str(path.relative_to(project_root))
    except ValueError:
        return str(path)


def read_lines(path: Path) -> list[str]:
    return path.read_text(encoding="utf-8").splitlines()


def markdown_files_under(directory: Path, file_name: str | None = None) -> list[Path]:
    if not directory.is_dir():
        return []
    pattern = file_name or "*.md"
    return sorted(directory.rglob(pattern))

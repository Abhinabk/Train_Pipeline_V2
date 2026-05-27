from pathlib import Path


def ensure_path(path: Path):
    path.mkdir(parents=True, exist_ok=True)


def save_html(full_path: Path, content: str):
    ensure_path(full_path.parent)
    with open(file=full_path, mode="w", encoding="utf-8") as f:
        f.write(content)

from pathlib import Path
import pandas as pd

def ensure_path(path:Path):
    path.mkdir(parents=True,exist_ok=True)

def load_csv(path_to_csv:Path):
    if path_to_csv.is_file():
        return pd.read_csv(path_to_csv)

def save_html(full_path:Path,content:str):
    ensure_path(full_path.parent)
    with open(
        file=full_path,
        mode="w",
        encoding="utf-8"
    ) as f:
        f.write(content)
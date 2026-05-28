from pathlib import Path
import pandas as pd

def ensure_path(path: Path):
    path.mkdir(parents=True, exist_ok=True)


def save_html(full_path: Path, content: str):
    ensure_path(full_path.parent)
    with open(file=full_path, mode="w", encoding="utf-8") as f:
        f.write(content)
        
def save_dataframe_as_csv(full_path: Path, content: dict,index_name:str|None=None):
    ensure_path(full_path.parent)
    df = pd.DataFrame(data=content)
    if index_name:
        df.index.name = index_name
        df.to_csv(full_path)
        
    df.to_csv(full_path,index=False)


from pathlib import Path
import pandas as pd


def load(path_to_csv: Path, type: str):
    if type == "csv":
        if path_to_csv.is_file():
            return pd.read_csv(path_to_csv)
from pathlib import Path
import pandas as pd


def load_csv(path_to_csv: Path):
    if path_to_csv.is_file():
        return pd.read_csv(path_to_csv)
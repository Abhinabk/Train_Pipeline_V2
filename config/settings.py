'''Handels project paths'''
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parent.parent

DATA_DIR = PROJECT_ROOT / "storage/data"
LOG_DIR = PROJECT_ROOT / "log"
CONFIG_DIR = PROJECT_ROOT / "config"

BRONZE_HTML_DIR = DATA_DIR / "bronze" / "bronze_raw_train_html"
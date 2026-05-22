'''Handels project paths'''
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parent.parent
DATABASE_NAME = "pipeline.db"
DATA_DIR = PROJECT_ROOT / "storage"/"data"
LOG_DIR = PROJECT_ROOT / "log"
CONFIG_DIR = PROJECT_ROOT / "config"

BRONZE_HTML_DIR = DATA_DIR / "bronze" / "bronze_raw_train_html"
DUCK_DB_DATABASE = PROJECT_ROOT/"storage"/DATABASE_NAME
SQL_DIR = PROJECT_ROOT/"sql"

'''Handels project paths'''
from pathlib import Path
MOTHERDUCK_DATABASE_NAME='train_pipeline'

PROJECT_ROOT = Path(__file__).resolve().parent.parent
DATABASE_NAME = "pipeline.duckdb"
DATA_DIR = PROJECT_ROOT / "storage"/"data"
LOG_DIR = PROJECT_ROOT / "log"
CONFIG_DIR = PROJECT_ROOT / "config"

BRONZE_HTML_DIR = DATA_DIR / "bronze" / "bronze_raw_train_html"
DUCK_DB_DATABASE = PROJECT_ROOT/"storage"/"database"/DATABASE_NAME
SQL_DIR = PROJECT_ROOT/"sql"

SOURCES_YML = CONFIG_DIR /"sources.yaml"
TRAINS_CSV = CONFIG_DIR / "trains.csv"
S3_BUCKET="train-pipeline-v2"
S3_PREFIX_BRONZE_TRAIN =  "bronze/bronze_raw_train_html" 
S3_PREFIX_SILVER_TRAIN = "silver"
CACHE_DIR = PROJECT_ROOT/".cache"
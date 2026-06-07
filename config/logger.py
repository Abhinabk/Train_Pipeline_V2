
import sys

from loguru import logger
from config.settings import LOG_DIR
#getting duplicate logs withot this
logger.remove()

generic_logger = logger.bind(name="generic")
bronze_logger = logger.bind(name="bronze")
silver_logger = logger.bind(name="silver")
gold_logger = logger.bind(name="gold")

logger.level("SKIP", no=25, color="<yellow>")

logger.add(
    sys.stderr,
    filter=lambda r: r["extra"].get("name") in ("bronze", "silver", "gold"),
)

logger.add(
    LOG_DIR / "bronze.log",
    filter=lambda r: r["extra"].get("name") == "bronze",
    rotation="20 MB",#will create new file after 20mb
    retention="30 days" #deletes after 30 days
)

logger.add(
    LOG_DIR / "silver.log",
    filter=lambda r: r["extra"].get("name") == "silver",
    rotation="20 MB",#will create new file after 20mb
    retention="30 days" #deletes after 30 days
)

logger.add(
    LOG_DIR/ "gold.log",
    filter=lambda r: r["extra"].get("name") == "gold",
    rotation="20 MB",#will create new file after 20mb
    retention="30 days" #deletes after 30 days
)
logger.add(
    LOG_DIR/ "generic.log",
    filter=lambda r: r["extra"].get("name") == "generic",
    rotation="20 MB",#will create new file after 20mb
    retention="30 days" #deletes after 30 days
)
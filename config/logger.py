
from loguru import logger
from config.settings import LOG_DIR
#getting duplicate logs withot this
logger.remove()

bronze_logger = logger.bind(name="bronze")
silver_logger = logger.bind(name="silver")
gold_logger = logger.bind(name="gold")

logger.add(
    LOG_DIR / "bronze.log",
    filter=lambda r: r["extra"].get("name") == "bronze"
)

logger.add(
    LOG_DIR / "silver.log",
    filter=lambda r: r["extra"].get("name") == "silver"
)

logger.add(
    LOG_DIR/ "gold.log",
    filter=lambda r: r["extra"].get("name") == "gold"
)
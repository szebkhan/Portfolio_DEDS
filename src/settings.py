from pathlib import Path
from loguru import logger

class Settings():
    basedir = Path.cwd()
    rawdir = Path("raw")
    processeddir = Path("processed")
    logdir = basedir / "log"

    sales_activity_columns = [
        "sales",
        "country",
        "retailer",
        "returned",
        "branch",
        "order",
        "staff",
        "order_header",
        "details",
        "product_type",
        "reason",
    ]

settings = Settings()
logger.add("logfile.log")
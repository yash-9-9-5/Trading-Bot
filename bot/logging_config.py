import logging
import sys

def setup_logger(): #logger for bot for console and terminal
    logger = logging.getLogger("bot")
    logger.setLevel(logging.DEBUG)

    formatter = logging.Formatter( #log format
        "%(asctime)s - %(name)s - %(levelname)s - %(message)s"
    )

    # Console handler
    ch = logging.StreamHandler(sys.stdout)
    ch.setLevel(logging.INFO)
    ch.setFormatter(formatter)

    # File handler
    fh = logging.FileHandler("bot.log")
    fh.setLevel(logging.DEBUG)
    fh.setFormatter(formatter)

    if not logger.handlers:
        logger.addHandler(ch)
        logger.addHandler(fh)

    return logger

logger = setup_logger()

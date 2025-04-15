import logging
from logging.handlers import RotatingFileHandler
from colorlog import ColoredFormatter
from pythonjsonlogger import jsonlogger

# --------- Logger Setup ---------
logger = logging.getLogger("access_logger")
logger.setLevel(logging.INFO)

# --------- Formatters ---------

# Colored formatter for terminal output
color_formatter = ColoredFormatter(
    "%(log_color)s%(asctime)s - %(levelname)s - %(message)s",
    datefmt="%Y-%m-%d %H:%M:%S",
    log_colors={
        "DEBUG": "cyan",
        "INFO": "green",
        "WARNING": "yellow",
        "ERROR": "red",
        "CRITICAL": "bold_red",
    }
)

# JSON formatter for file logs
json_formatter = jsonlogger.JsonFormatter(
    fmt="%(asctime)s %(levelname)s %(message)s %(name)s",
    datefmt="%Y-%m-%d %H:%M:%S"
)

# --------- Handlers ---------

# Rotating file handler (writes in JSON)
file_handler = RotatingFileHandler("access_logs.json", maxBytes=1_000_000, backupCount=5)
file_handler.setFormatter(json_formatter)

# Color terminal stream handler
stream_handler = logging.StreamHandler()
stream_handler.setFormatter(color_formatter)

# --------- Attach Handlers ---------

if not logger.hasHandlers():
    logger.addHandler(file_handler)
    logger.addHandler(stream_handler)

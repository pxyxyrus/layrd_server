import os
from config import config
import logging
from logging.handlers import TimedRotatingFileHandler
import datetime


# Define the log file directory
log_dir = config['logger']['log_dir']

# Ensure the log directory exists
os.makedirs(log_dir, exist_ok=True)

logger = logging.getLogger("daily_logger")

# any logging below or equal to debug will be just ingnored
logger.setLevel(logging.DEBUG)

# Define the log format
log_format = logging.Formatter("%(asctime)s - %(levelname)s - %(message)s")

# Get the current date for the log filename
log_filename = os.path.join(log_dir, f"server_log")

# Create a TimedRotatingFileHandler with a daily interval
file_handler = TimedRotatingFileHandler(log_filename, when="midnight", interval=1, backupCount=7)
file_handler.suffix = "_%Y-%m-%d.log"

# Set the log format for the file handler
file_handler.setFormatter(log_format)

# Add the file handler to the logger
logger.addHandler(file_handler)



    
import os
import logging
from datetime import datetime
from from_root import from_root
from logging.handlers import RotatingFileHandler

# Constants for logging configuration
LOG_DIR = 'logs' # Directory to store log files
LOG_FILE = f'{datetime.now().strftime("%m_%d_%Y_%H_%M_%S")}.log' # Log file name
MAX_LOG_SIZE = 5 * 1024 * 1024 # Maximum log file size in bytes (5 MB)
BACKUP_COUNT = 3 # Number of backup log files to keep

# Create log directory if it doesn't exist
log_dir_path = os.path.join(from_root(), LOG_DIR)
os.makedirs(log_dir_path, exist_ok=True)
log_file_path = os.path.join(log_dir_path, LOG_FILE)

def configure_logger():
    """
    Configure logging with a rotating file handler(rotation means that the log file will be rotated when it reaches a certain size) and a console handler.
    """

    # Create a custom logger with the specified name
    logger = logging.getLogger()
    logger.setLevel(logging.DEBUG)

    # Define formatter
    formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')

    # Define handlers for console and file logging with rotation
    # File handler
    file_handler = RotatingFileHandler(log_file_path, maxBytes=MAX_LOG_SIZE, backupCount=BACKUP_COUNT)
    file_handler.setFormatter(formatter)
    file_handler.setLevel(logging.INFO)
    # Console handler
    console_handler = logging.StreamHandler()
    console_handler.setFormatter(formatter)
    console_handler.setLevel(logging.DEBUG)

    # Add handlers to the logger that means that the logger will use these handlers to log messages
    logger.addHandler(file_handler)
    logger.addHandler(console_handler)

# Call the configure_logger function to apply the configuration
configure_logger()
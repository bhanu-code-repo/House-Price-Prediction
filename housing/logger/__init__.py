# housing/logger/__init__.py

# Import required libraries and packages
import logging
from housing.constant import *

# Define the log file name using the current timestamp
LOG_FILE_NAME = f'log_{CURRENT_TIMESTAMP}.log'

# Create the log folder if it doesn't exist
os.makedirs(LOG_FOLDER_NAME, exist_ok=True)

# Define the log file path by joining the log folder and log file name
LOG_FILE_PATH = os.path.join(LOG_FOLDER_NAME, LOG_FILE_NAME)

# Configure the logging module with the log file path and other settings
logging.basicConfig(
    filename=LOG_FILE_PATH,
    filemode='w',
    format='[%(asctime)s]^;%(levelname)s^;%(lineno)d^;%(filename)s^;%(funcName)s()^;%(message)s',
    level=logging.INFO
)

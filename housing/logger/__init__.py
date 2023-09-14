
import logging
from housing.constant import *

LOG_FILE_NAME = f'log_{CURRENT_TIMESTAMP}.log'
os.makedirs(LOG_FOLDER_NAME, exist_ok=True)
LOG_FILE_PATH = os.path.join(LOG_FOLDER_NAME, LOG_FILE_NAME)

logging.basicConfig(
    filename=LOG_FILE_PATH,
    filemode='w',
    format='[%(asctime)s]^;%(levelname)s^;%(lineno)d^;%(filename)s^;%(funcName)s()^;%(message)s',
    level=logging.INFO
)

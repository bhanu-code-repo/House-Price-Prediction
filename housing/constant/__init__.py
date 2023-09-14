# housing/util/__init__.py

import os
from datetime import datetime

ROOT_DIR = os.getcwd()

CONFIG_DIR = 'config'
CONFIG_FILE_NAME = 'config.yaml'
CONFIG_FILE_PATH = os.path.join(ROOT_DIR, CONFIG_DIR, CONFIG_FILE_NAME)

LOG_FOLDER_NAME = 'logs'
LOG_DIR = os.path.join(ROOT_DIR, LOG_FOLDER_NAME)

PIPELINE_FOLDER_NAME = 'housing'
PIPELINE_DIR = os.path.join(ROOT_DIR, PIPELINE_FOLDER_NAME)

SAVED_MODELS_DIR_NAME = 'saved-models'
MODEL_DIR = os.path.join(ROOT_DIR, SAVED_MODELS_DIR_NAME)

MODEL_FILE_NAME = 'model.yaml'
MODEL_CONFIG_FILE_PATH = os.path.join(ROOT_DIR, CONFIG_DIR, MODEL_FILE_NAME)

CURRENT_TIMESTAMP = f"{datetime.now().strftime('%Y-%m-%d-%H-%M-%S')}"

# Training Pipeline
TRAINING_PIPELINE_CONFIG_KEY = 'training_pipeline_config'
TRAINING_PIPELINE_ARTIFACT_DIR_KEY = 'artifact_dir'
TRAINING_PIPELINE_NAME_KEY = 'pipeline_name'

# Data Ingestion 
DATA_INGESTION_CONFIG_KEY = 'data_ingestion_config'
DATA_INGESTION_ARTIFACT_DIR = 'data_ingestion'
DATA_INGESTION_DOWNLOAD_URL_KEY = 'dataset_download_url'
DATA_INGESTION_RAW_DATA_DIR_KEY = 'raw_data_dir'
DATA_INGESTION_TGZ_DOWNLOAD_DIR_KEY = 'tgz_download_dir'
DATA_INGESTION_INGESTED_DIR_NAME_KEY = 'ingested_dir'
DATA_INGESTION_TRAIN_DIR_KEY = 'ingested_train_dir'
DATA_INGESTION_TEST_DIR_KEY = 'ingested_test_dir'
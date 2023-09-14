# housing/config/__init__.py
import sys

from housing.constant import *
from housing.exception import CustomException

from housing.util import read_yaml
from housing.constant import *
from housing.entity.config_entity import *

class Configuration:

    def __init__(self, config_file_path:str=CONFIG_FILE_PATH, current_timestamp:str=CURRENT_TIMESTAMP) -> None:
        try:
            self.config_info = read_yaml(file_path=config_file_path)
            self.pipeline_config_training = self.training_pipeline_config()
            self.timestamp = current_timestamp
        except Exception as e:
            raise CustomException(e, sys) from e
        

    def data_ingestion_config(self) -> DataIngestionConfig:
        try:
            # artifact directory from training pipeline configuration
            artifact_dir = self.pipeline_config_training.artifact_dir

            data_ingestion_artifact_dir = os.path.join(
                artifact_dir,
                DATA_INGESTION_ARTIFACT_DIR,
                self.timestamp
            )

            data_ingestion_info = self.config_info[DATA_INGESTION_CONFIG_KEY]
            dataset_download_url = data_ingestion_info[DATA_INGESTION_DOWNLOAD_URL_KEY]

            tgz_download_dir = os.path.join(
                data_ingestion_artifact_dir,
                data_ingestion_info[DATA_INGESTION_TGZ_DOWNLOAD_DIR_KEY]
            )

            raw_data_dir = os.path.join(
                data_ingestion_artifact_dir,
                data_ingestion_info[DATA_INGESTION_RAW_DATA_DIR_KEY]
            )

            ingested_data_dir = os.path.join(
                data_ingestion_artifact_dir,
                data_ingestion_info[DATA_INGESTION_INGESTED_DIR_NAME_KEY]
            )

            ingested_train_dir = os.path.join(
                ingested_data_dir,
                data_ingestion_info[DATA_INGESTION_TRAIN_DIR_KEY]
            )

            ingested_test_dir =os.path.join(
                ingested_data_dir,
                data_ingestion_info[DATA_INGESTION_TEST_DIR_KEY]
            )

            return DataIngestionConfig(
                dataset_download_url=dataset_download_url,
                tgz_download_dir=tgz_download_dir,
                raw_data_dir=raw_data_dir,
                ingested_train_dir=ingested_train_dir,
                ingested_test_dir=ingested_test_dir
            )
        except Exception as e:
            raise CustomException(e, sys) from e
        
    def data_validation_config(self) -> DataValidationConfig:
        try:
            pass
        except Exception as e:
            raise CustomException(e, sys) from e
        
    def data_transformation_config(self) -> DataTransformationConfig:
        try:
            pass
        except Exception as e:
            raise CustomException(e, sys) from e
        
    def model_trainer_config(self) -> ModelTrainerConfig:
        try:
            pass
        except Exception as e:
            raise CustomException(e, sys) from e
        
    def model_evaluation_config(self) -> ModelEvaluationConfig:
        try:
            pass
        except Exception as e:
            raise CustomException(e, sys) from e
        
    def model_pusher_config(self) -> ModelPusherConfig:
        try:
            pass
        except Exception as e:
            raise CustomException(e, sys) from e
        
    def training_pipeline_config(self) -> TrainingPipelineConfig:
        try:
            # get training pipeline configuration
            training_pipeline_config = self.config_info[TRAINING_PIPELINE_CONFIG_KEY]
            
            # create artifact directory
            artifact_dir = os.path.join(
                ROOT_DIR,
                training_pipeline_config[TRAINING_PIPELINE_NAME_KEY],
                training_pipeline_config[TRAINING_PIPELINE_ARTIFACT_DIR_KEY]
            )

            # return training pipeline configuration
            return TrainingPipelineConfig(
                artifact_dir=artifact_dir
            )
        except Exception as e:
            raise CustomException(e, sys) from e
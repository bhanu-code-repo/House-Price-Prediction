
import os
import sys
from housing.logger import logging
from housing.exception import CustomException
from housing.entity.artifact_entity import DataIngestionArtifact, DataValidationArtifact, ModelTrainerArtifact
from housing.entity.config_entity import ModelEvaluationConfig

class ModelEvaluation:
    
    def __init__(
        self,
        model_evaluation_config: ModelEvaluationConfig,
        data_ingestion_artifact: DataIngestionArtifact,
        data_validation_artifact: DataValidationArtifact,
        model_trainer_artifact: ModelTrainerArtifact
    ) -> None:
        try:
            logging.info(f"{'>>' * 30} model evaluation log started {'<<' * 30} ")
            self.model_evaluation_config = model_evaluation_config
            self.model_trainer_artifact = model_trainer_artifact
            self.data_ingestion_artifact = data_ingestion_artifact
            self.data_validation_artifact = data_validation_artifact
        except Exception as e:
            # Raise a custom exception if an error occurs during the extraction process
            raise CustomException(e, sys) from e
        
    def get_best_model(self):
        try:
            model = None
            model_evaluation_file_path = self.model_evaluation_config.model_evaluation_file_path
            if not os.path.exists(model_evaluation_file_path):
                write_yaml(file_path=model_evaluation_file_path, data={})
                return model
            model_eval_file_content = read_yaml(file_path=model_evaluation_file_path)

            model_eval_file_content = dict() if model_eval_file_content is None else model_eval_file_content

            if BEST_MODEL_KEY not in model_eval_file_content:
                return model

            model = load_object(file_path=model_eval_file_content[BEST_MODEL_KEY][MODEL_PATH_KEY])
            return model
        except Exception as e:
            # Raise a custom exception if an error occurs during the extraction process
            raise CustomException(e, sys) from e
    
    def update_evaluation_report(self, model_evaluation_artifact: ModelEvaluationArtifact):
        try:
            pass
        except Exception as e:
            # Raise a custom exception if an error occurs during the extraction process
            raise CustomException(e, sys) from e
        
    def initiate_model_evaluation(self) -> ModelEvaluationArtifact:
        try:
            pass
        except Exception as e:
            # Raise a custom exception if an error occurs during the extraction process
            raise CustomException(e, sys)
        
    def __del__(self):
        logging.info(f"{'=' * 20}Model Evaluation log completed.{'=' * 20} ")
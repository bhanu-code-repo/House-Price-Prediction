# housing/entity/config_entity.py

# Import required libraries and packages
from collections import namedtuple

# A named tuple that represents the configuration for data ingestion.
# 
# Attributes:
#     dataset_download_url (str): The URL to download the dataset.
#     tgz_download_dir (str): The directory to store the downloaded .tgz file.
#     raw_data_dir (str): The directory to store the raw data.
#     ingested_train_dir (str): The directory to store the ingested training data.
#     ingested_test_dir (str): The directory to store the ingested testing data.
DataIngestionConfig = namedtuple(
    'DataIngestionConfig',
    [
        'dataset_download_url',
        'tgz_download_dir',
        'raw_data_dir',
        'ingested_train_dir',
        'ingested_test_dir'
    ]
)

# A named tuple that represents the configuration for data validation.
#
# Attributes:
#     schema_file_path (str): The file path to the data schema.
#     report_file_path (str): The file path to store the validation report.
#     report_page_file_path (str): The file path to store the validation report page.
DataValidationConfig = namedtuple(
    'DataValidationConfig',
    [
        'schema_file_path',
        'report_file_path',
        'report_page_file_path'
    ]
)

# A named tuple that represents the configuration for data transformation.
#
# Attributes:
#     add_bedroom_per_room (bool): Flag indicating whether to add a feature for bedrooms per room.
#     transformed_train_dir (str): The directory to store the transformed training data.
#     transformed_test_dir (str): The directory to store the transformed testing data.
#     preprocessed_object_file_path (str): The file path to store the preprocessed object.
DataTransformationConfig = namedtuple(
    'DataTransformationConfig',
    [
        'add_bedroom_per_room',
        'transformed_train_dir',
        'transformed_test_dir',
        'preprocessed_object_file_path'
    ]
)

# A named tuple that represents the configuration for model training.
#
# Attributes:
#     trained_model_file_path (str): The file path to store the trained model.
#     base_accuracy (float): The base accuracy for the model.
#     model_config_file_path (str): The file path to the model configuration.
ModelTrainerConfig = namedtuple(
    'ModelTrainerConfig',
    [
        'trained_model_file_path',
        'base_accuracy',
        'model_config_file_path'
    ]
)

# A named tuple that represents the configuration for model evaluation.
#
# Attributes:
#     model_evaluation_file_path (str): The file path to store the model evaluation data.
#     time_stamp (int): The timestamp for the model evaluation.
ModelEvaluationConfig = namedtuple(
    'ModelEvaluationConfig',
    [
        'model_evaluation_file_path',
        'time_stamp'
    ]
)

# A named tuple that represents the configuration for model pushing.
#
# Attributes:
#     export_dir_path (str): The directory path to export the model.
ModelPusherConfig = namedtuple(
    'ModelPusherConfig',
    [
        'export_dir_path'
    ]
)

# A named tuple that represents the configuration for the training pipeline.
#
# Attributes:
#     artifact_dir (str): The directory path to store the training artifacts.
TrainingPipelineConfig = namedtuple(
    'TrainingPipelineConfig',
    [
        'artifact_dir'
    ]
)
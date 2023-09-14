# housing/entity/config_entity.py

from collections import namedtuple

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

DataValidationConfig = namedtuple(
    'DataValidationConfig',
    []
)

DataTransformationConfig = namedtuple(
    'DataTransformationConfig',
    []
)

ModelTrainerConfig = namedtuple(
    'ModelTrainerConfig',
    []
)

ModelEvaluationConfig = namedtuple(
    'ModelEvaluationConfig',
    []
)

ModelPusherConfig = namedtuple(
    'ModelPusherConfig',
    []
)

TrainingPipelineConfig = namedtuple(
    'TrainingPipelineConfig',
    [
        'artifact_dir'
    ]
)
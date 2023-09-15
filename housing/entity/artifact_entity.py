# housing/entity/artifact_entity.py

# Import required libraries and packages
from collections import namedtuple

# A named tuple that represents the data ingestion artifact.
#
# Attributes:
#     train_file_path (str): The file path of the ingested training data.
#     test_file_path (str): The file path of the ingested testing data.
#     is_ingested (bool): Flag indicating whether the data is ingested.
#     message (str): Additional message related to the data ingestion.
DataIngestionArtifact = namedtuple(
    'DataIngestionArtifact', 
    [
        'train_file_path',
        'test_file_path',
        'is_ingested',
        'message'
    ]
)

# A named tuple that represents the data validation artifact.
#
# Attributes:
#     schema_file_path (str): The file path of the data schema.
#     report_file_path (str): The file path of the validation report.
#     report_page_file_path (str): The file path of the validation report page.
#     is_validated (bool): Flag indicating whether the data is validated.
#     message (str): Additional message related to the data validation.
DataValidationArtifact = namedtuple(
    'DataValidationArtifact',
    [
        'schema_file_path',
        'report_file_path',
        'report_page_file_path',
        'is_validated',
        'message'
    ]
)

# A named tuple that represents the data transformation artifact.
#
# Attributes:
#     is_transformed (bool): Flag indicating whether the data is transformed.
#     message (str): Additional message related to the data transformation.
#     transformed_train_file_path (str): The file path of the transformed training data.
#     transformed_test_file_path (str): The file path of the transformed testing data.
#     preprocessed_object_file_path (str): The file path of the preprocessed object.
DataTransformationArtifact = namedtuple(
    'DataTransformationArtifact',
    [
        'is_transformed',
        'message',
        'transformed_train_file_path',
        'transformed_test_file_path',
        'preprocessed_object_file_path'
    ]
)

# A named tuple that represents the model trainer artifact.
#
# Attributes:
#     is_trained (bool): Flag indicating whether the model is trained.
#     message (str): Additional message related to the model training.
#     trained_model_file_path (str): The file path of the trained model.
#     train_rmse (float): The root mean squared error for the training data.
#     test_rmse (float): The root mean squared error for the testing data.
#     train_accuracy (float): The accuracy score for the training data.
#     test_accuracy (float): The accuracy score for the testing data.
#     model_accuracy (float): The overall accuracy score for the model.
ModelTrainerArtifact = namedtuple(
    'ModelTrainerArtifact',
    [
        'is_trained',
        'message',
        'trained_model_file_path',
        'train_rmse',
        'test_rmse',
        'train_accuracy',
        'test_accuracy',
        'model_accuracy'
    ]
)

# A named tuple that represents the model evaluation artifact.
#
# Attributes:
#     is_model_accepted (bool): Flag indicating whether the model is accepted.
#     evaluated_model_path (str): The file path of the evaluated model.
ModelEvaluationArtifact = namedtuple(
    'ModelEvaluationArtifact',
    [
        'is_model_accepted',
        'evaluated_model_path'
    ]
)

# A named tuple that represents the model pusher artifact.
#
# Attributes:
#     is_model_pusher (bool): Flag indicating whether the model is pushed.
#     export_model_file_path (str): The file path of the exported model.
ModelPusherArtifact = namedtuple(
    'ModelPusherArtifact',
    [
        'is_model_pusher',
        'export_model_file_path'
    ]
)
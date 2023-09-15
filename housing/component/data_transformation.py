# hoing/component/data_transformation.py

# Import required libraries and packages
import numpy as np
import os
import sys
from sklearn.preprocessing import StandardScaler, OneHotEncoder
from sklearn.pipeline import Pipeline
from sklearn.compose import ColumnTransformer
from sklearn.impute import SimpleImputer

from housing.logger import logging
from housing.util import read_yaml
from housing.entity.config_entity import DataTransformationConfig
from housing.entity.artifact_entity import DataIngestionArtifact, DataValidationArtifact, DataTransformationArtifact

from housing.component.feature_generator import FeatureGenerator
from housing.util import save_numpy_array_data, save_object, load_data

class DataTransformation:

    def __init__(
        self,
        data_transformation_config: DataTransformationConfig,
        data_ingestion_artifact: DataIngestionArtifact,
        data_validation_artifact: DataValidationArtifact
    ) -> None:
        """
        Initializes a new instance of the DataTransformation class.

        Parameters:
        - data_transformation_config (DataTransformationConfig): The configuration object for data transformation.
        - data_ingestion_artifact (DataIngestionArtifact): The artifact object for data ingestion.
        - data_validation_artifact (DataValidationArtifact): The artifact object for data validation.

        Return Type:
        - None

        Raises:
        - CustomException: If an error occurs during the extraction process.
        """
        try:
            logging.info(f"{'>>' * 30} data transformation log started {'<<' * 30} ")
            
            # Store the data transformation configuration
            self.data_transformation_config= data_transformation_config
            
            # Store the data ingestion artifact
            self.data_ingestion_artifact = data_ingestion_artifact
            
            # Store the data validation artifact
            self.data_validation_artifact = data_validation_artifact
        except Exception as e:
            # Raise a custom exception if an error occurs during the extraction process
            raise CustomException(e, sys) from e
        

    def initiate_data_transformation(self) -> DataTransformationArtifact:
        """
        Initiates the data transformation process.

        Returns:
            DataTransformationArtifact: An object containing information about the
            data transformation process. This object includes the following attributes:
                - is_transformed (bool): Indicates whether the data transformation was successful.
                - message (str): A message indicating the status of the data transformation process.
                - transformed_train_file_path (str): The file path of the transformed training data.
                - transformed_test_file_path (str): The file path of the transformed testing data.
                - preprocessed_object_file_path (str): The file path of the preprocessed object.
        
        Raises:
            CustomException: If an error occurs during the data transformation process.
        """
        try:
            # Obtain the preprocessing object
            logging.info('obtaining preprocessing object')
            preprocessing_obj = self.get_data_transformer_object()
            
            # Obtain the file paths for training and test data
            logging.info('obtaining training and test file path')
            train_file_path = self.data_ingestion_artifact.train_file_path
            test_file_path = self.data_ingestion_artifact.test_file_path
            
            # Obtain the schema file path
            schema_file_path = self.data_validation_artifact.schema_file_path
            
            # Load the training and test data as pandas dataframes
            logging.info('loading training and test data as pandas dataframe')
            train_df = load_data(file_path=train_file_path, schema_file_path=schema_file_path)
            test_df = load_data(file_path=test_file_path, schema_file_path=schema_file_path)
            
            # Read the schema file to obtain the target column name
            schema = read_yaml(file_path=schema_file_path)
            target_column_name = schema[TARGET_COLUMN_KEY]
            
            # Split the input and target features from the training and testing dataframes
            logging.info('splitting input and target feature from training and testing dataframe')
            input_feature_train_df = train_df.drop(columns=[target_column_name], axis=1)
            target_feature_train_df = train_df[target_column_name]
            input_feature_test_df = test_df.drop(columns=[target_column_name], axis=1)
            target_feature_test_df = test_df[target_column_name]
            
            # Apply the preprocessing object on the training and testing dataframes
            logging.info('applying preprocessing object on training and testing dataframe')
            input_feature_train_arr = preprocessing_obj.fit_transform(input_feature_train_df)
            input_feature_test_arr = preprocessing_obj.transform(input_feature_test_df)

            # Combine the input and target features into arrays
            train_arr = np.c_[input_feature_train_arr, np.array(target_feature_train_df)]
            test_arr = np.c_[input_feature_test_arr, np.array(target_feature_test_df)]
            
            # Obtain the transformed train and test directories
            transformed_train_dir = self.data_transformation_config.transformed_train_dir
            transformed_test_dir = self.data_transformation_config.transformed_test_dir

            # Generate file names for the transformed train and test data
            train_file_name = os.path.basename(train_file_path).replace(".csv", ".npz")
            test_file_name = os.path.basename(test_file_path).replace(".csv", ".npz")

            # Create file paths for the transformed train and test data
            transformed_train_file_path = os.path.join(transformed_train_dir, train_file_name)
            transformed_test_file_path = os.path.join(transformed_test_dir, test_file_name)
            
            # Save the transformed train and test data as numpy arrays
            logging.info('saving transformed training and testing array')
            save_numpy_array_data(file_path=transformed_train_file_path, array=train_arr)
            save_numpy_array_data(file_path=transformed_test_file_path, array=test_arr)

            # Save the preprocessing object
            preprocessing_obj_file_path = self.data_transformation_config.preprocessed_object_file_path
            logging.info('saving preprocessing object')
            save_object(file_path=preprocessing_obj_file_path, obj=preprocessing_obj)

            # Create a data transformation artifact
            data_transformation_artifact = DataTransformationArtifact(
                is_transformed=True,
                message="data transformation successful",
                transformed_train_file_path=transformed_train_file_path,
                transformed_test_file_path=transformed_test_file_path,
                preprocessed_object_file_path=preprocessing_obj_file_path
            )

            # Log the data transformation artifact
            logging.info(f"data transformation artifact: [{data_transformation_artifact}]")

            # Return the data transformation artifact
            return data_transformation_artifact
        except Exception as e:
            # Raise a custom exception if an error occurs during the data transformation process
            raise CustomException(e, sys) from e

    def get_data_transformer_object(self) -> ColumnTransformer:
        """
        A function to create a ColumnTransformer object for data transformation.

        Parameters:
        - self: The object instance.
        
        Returns:
        - ColumnTransformer: The created ColumnTransformer object.

        Raises:
        - CustomException: If an error occurs during the extraction process.
        """
        try:
            # Get the file path of the dataset schema
            schema_file_path = self.data_validation_artifact.schema_file_path
            
            # Read the dataset schema from the file
            dataset_schema = read_yaml(file_path=schema_file_path)
            
            # Get the list of numerical columns from the dataset schema
            numerical_columns = dataset_schema[NUMERICAL_COLUMN_KEY]
            logging.info(f'numerical columns: [{numerical_columns}]')
            
            # Get the list of categorical columns from the dataset schema
            categorical_columns = dataset_schema[CATEGORICAL_COLUMN_KEY]
            logging.info(f'categorical columns: [{categorical_columns}]')
            
            # Create a pipeline for numerical column preprocessing
            num_pipeline = Pipeline(steps=[
                # Impute missing values with median
                ('imputer', SimpleImputer(strategy='median')),
                # Generate additional features if required
                ('feature_generator', FeatureGenerator(
                    add_bedrooms_per_room=self.data_transformation_config.add_bedroom_per_room,
                    columns=numerical_columns
                )),
                # Scale the numerical features
                ('scaler', StandardScaler())  
            ])
            
            # Create a pipeline for categorical column preprocessing
            cat_pipeline = Pipeline(steps=[
                # Impute missing values with most frequent value
                ('impute', SimpleImputer(strategy='most_frequent')),
                # One-hot encode categorical features
                ('one_hot_encoder', OneHotEncoder()),
                # Scale the categorical features
                ('scaler', StandardScaler(with_mean=False))
            ])
            
            # Create a ColumnTransformer to apply different preprocessing steps to different columns
            preprocessing = ColumnTransformer([
                ('num_pipeline', num_pipeline, numerical_columns),
                ('cat_pipeline', cat_pipeline, categorical_columns),
            ])
            
            return preprocessing
        except Exception as e:
            # Raise a custom exception if an error occurs during the extraction process
            raise CustomException(e, sys) from e

    def __del__(self):
            """
            The __del__ method is a special method in Python that is automatically called when an object is about to be destroyed. This method is used to perform any cleanup operations before the object is deallocated from memory. In this case, the __del__ method logs a message indicating that the data transformation log has been completed.

            Parameters:
            - self: The instance of the class.

            Return Type:
            - None
            """
            logging.info(f"{'>>'*30} data transformation log completed {'<<'*30} \n\n")


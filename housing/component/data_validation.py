
import os
import json

from evidently.model_profile import Profile
from evidently.model_profile.sections import DataDriftProfileSection
from evidently.dashboard import Dashboard
from evidently.dashboard.tabs import DataDriftTab

from housing.logger import logging
from housing.entity.artifact_entity import DataIngestionArtifact
from housing.entity.config_entity import DataValidationConfig
from housing.exception import CustomException

class DataValidation:
    
    def __init__(
        self,
        data_validation_config: DataValidationConfig,
        data_ingestion_artifact: DataIngestionArtifact
    ) -> None:
        """
        Initialize the DataValidation class.
    
        Args:
            data_validation_config: Configuration for data validation.
            data_ingestion_artifact: Artifact containing the ingested data.
        """
        try:
            logging.info(f"{'>>'*30} data validation log started {'<<'*30} \n\n")
            self.data_validation_config = data_validation_config
            self.data_ingestion_artifact = data_ingestion_artifact
        except Exception as e:
            # Raise a custom exception if an error occurs during the extraction process
            raise CustomException(e, sys) from e

    def initiate_data_validation(self) -> DataValidationArtifact:
        """
        Initiate the data validation process.

        This function performs the following steps:
        1. Checks if the train and test files exist.
        2. Validates the dataset schema.
        3. Checks for any data drift.
        
        Returns:
            DataValidationArtifact: An object containing the paths to the schema file, 
            report file, report page file, validation status, and a success message.
        
        Raises:
            CustomException: If an error occurs during the data validation process.
        """
        try:
            # Step 1: Check if the train and test files exist
            self.is_train_test_file_exists()

            # Step 2: Validate the dataset schema
            self.validate_dataset_schema()

            # Step 3: Check for any data drift
            self.is_data_drift_found()

            # Create a DataValidationArtifact object with the necessary information
            data_validation_artifact = DataValidationArtifact(
                schema_file_path=self.data_validation_config.schema_file_path,
                report_file_path=self.data_validation_config.report_file_path,
                report_page_file_path=self.data_validation_config.report_page_file_path,
                is_validated=True,
                message="data validation performed successfully."
            )

            # Log the data validation artifact
            logging.info(f'data validation artifact: {data_validation_artifact}')

            # Return the data validation artifact
            return data_validation_artifact

        except Exception as e:
            # Raise a CustomException if an error occurs during the data validation process
            raise CustomException(e, sys)
        
    def get_train_and_test_df(self):
        """
        Reads the train and test dataframes from CSV files and returns them.

        Parameters:
            self (object): The instance of the class.
        
        Returns:
            tuple: A tuple containing the train dataframe and the test dataframe.
        
        Raises:
            CustomException: If an error occurs during the extraction process.
        """
        try:
            # Read the train dataframe from the CSV file
            train_df = pd.read_csv(self.data_ingestion_artifact.train_file_path)
            
            # Read the test dataframe from the CSV file
            test_df = pd.read_csv(self.data_ingestion_artifact.test_file_path)
            
            # Return the train and test dataframes as a tuple
            return train_df, test_df
        except Exception as e:
            # Raise a custom exception if an error occurs during the extraction process
            raise CustomException(e, sys) from e
            
    def is_train_test_file_exists(self) -> bool:
        """
        Checks if the training and testing files are available.

        Returns:
            bool: True if both training and testing files exist, False otherwise.

        Raises:
            Exception: If either the training file or the testing file is not present.
        """
        try:
            # Log a message to indicate that we are checking if the training and testing files are available
            logging.info('checking if training and testing files are available...')
            
            # Get the paths of the training and testing files
            train_file_path = self.data_ingestion_artifact.train_file_path
            test_file_path = self.data_ingestion_artifact.test_file_path
            
            # Check if the training file exists
            is_train_file_exist = os.path.exists(train_file_path)
            
            # Check if the testing file exists
            is_test_file_exist = os.path.exists(test_file_path)
            
            # Check if both the training and testing files exist
            is_available = is_train_file_exist and is_test_file_exist
            
            # Log the availability status of the training and testing files
            logging.info(f'training and testing file availability status: [{is_available}]')
            
            # If either the training or testing file is not present, raise an exception
            if not is_available:
                training_file = self.data_ingestion_artifact.train_file_path
                testing_file = self.data_ingestion_artifact.test_file_path
                message = f"Training file: {training_file} or Testing file: {testing_file} is not present"
                raise Exception(message)
            
            # Return the availability status of the training and testing files
            return is_available
        
        except Exception as e:
            # Raise a custom exception if an error occurs during the extraction process
            raise CustomException(e, sys) from e
            
    def validate_dataset_schema(self) -> bool:
        try:
            # TODO: Implement dataset schema validation logic here
            validation_status = False

            # TODO: Set validation_status to True if dataset schema is valid
            validation_status = True
            return validation_status
        except Exception as e:
            # Raise a custom exception if an error occurs during the extraction process
            raise CustomException(e, sys) from e
            
    def get_and_save_data_drift_report(self):
        """
        Generate and save a data drift report.

        Returns:
            dict: The generated data drift report.
            
        Raises:
            CustomException: If an error occurs during the extraction process.
        """
        try:
            # Create a profile with only the data drift section
            profile = Profile(sections=[DataDriftProfileSection()])
            
            # Get train and test dataframes
            train_df, test_df = self.get_train_and_test_df()
            
            # Calculate data drift using the profile
            profile.calculate(train_df, test_df)
            
            # Convert the profile to JSON format
            report = json.loads(profile.json())
            
            # Get the report file path from the configuration
            report_file_path = self.data_validation_config.report_file_path
            
            # Create the report directory if it doesn't exist
            report_dir = os.path.dirname(report_file_path)
            os.makedirs(report_dir, exist_ok=True)
            
            # Save the report to a file
            with open(report_file_path, 'w') as report_file:
                json.dump(report, report_file, indent=6)
            
            return report
        except Exception as e:
            # Raise a custom exception if an error occurs during the extraction process
            raise CustomException(e, sys) from e
            
    def save_data_drift_report_page(self):
        """
        Saves the data drift report page.
        
        This function creates a Dashboard object with a DataDriftTab, and calculates the data drift using the train and test dataframes. It then gets the file path and directory for the report page, creates the directory if it doesn't exist, and saves the dashboard as a report page at the specified file path.
        
        Parameters:
            self: The instance of the class.
            
        Returns:
            None.
            
        Raises:
            CustomException: If an error occurs during the process.
        """
        try:
            # Create a Dashboard object with a DataDriftTab
            dashboard = Dashboard(tabs=[DataDriftTab()])

            # Get the train and test dataframes
            train_df, test_df = self.get_train_and_test_df()

            # Calculate the data drift using the train and test dataframes
            dashboard.calculate(train_df, test_df)

            # Get the file path and directory for the report page
            report_page_file_path = self.data_validation_config.report_page_file_path
            report_page_dir = os.path.dirname(report_page_file_path)

            # Create the directory if it doesn't exist
            os.makedirs(report_page_dir, exist_ok=True)

            # Save the dashboard as a report page at the specified file path
            dashboard.save(report_page_file_path)
        except Exception as e:
            # Raise a custom exception if an error occurs during the process
            raise CustomException(e, sys)
            
    def is_data_drift_found(self) -> bool:
        try:
            # get and save the data drift report
            report = self.get_and_save_data_drift_report()

            # save the data drift report page
            self.save_data_drift_report_page()

            # return True if no exception is raised
            return True

        except Exception as e:
            # Raise a custom exception if an error occurs during the extraction process
            raise CustomException(e, sys)

            
def __del__(self):
    """
    Destructor method for the class.
    """
    logging.info(f"{'>>'*30} data validation log completed {'<<'*30} \n\n")

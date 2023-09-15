# housing/component/data_ingestion.py

# Import required libraries and packages
import os
import sys
import tarfile
import numpy as np
import pandas as pd
from six.moves import urllib
from sklearn.model_selection import StratifiedShuffleSplit

from housing.logger import logging
from housing.exception import CustomException

from housing.entity.artifact_entity import DataIngestionArtifact
from housing.entity.config_entity import DataIngestionConfig

class DataIngestion:

    def __init__(self, data_ingestion_config: DataIngestionConfig) -> None:
        """
        Initializes a DataIngestion object with the given data ingestion configuration.
    
        Args:
            data_ingestion_config (DataIngestionConfig): The configuration for data ingestion.
            It is an instance of the DataIngestionConfig class that holds the necessary 
            parameters for the data ingestion process.
    
        Raises:
            CustomException: If an error occurs during initialization. This exception is raised 
            if there is an error while initializing the DataIngestion object.
        """
        try:
            logging.info(f"{'>>'*20} data ingestion log started {'<<'*20}")
            # Store the data ingestion configuration in a private variable
            self.__data_ingestion_config = data_ingestion_config
        except Exception as e:
            # If an error occurs during initialization, raise a custom exception
            raise CustomException(e, sys) from e
        
    def initiate_data_ingestion(self) -> DataIngestionArtifact:
        """
        Initiates the data ingestion process.

        Returns:
            DataIngestionArtifact: An object containing the ingested data.

        Raises:
            CustomException: If an error occurs during the ingestion process.
        """
        try:
            # Download the housing data and get the path of the downloaded tgz file
            tgz_file_path = self.__download_housing_data()

            # Extract the downloaded tgz file
            self.__extract_tgz_file(tgz_file_path=tgz_file_path)

            # Split the data into training and testing datasets
            return self.__split_data_as_train_test()
        except Exception as e:
            # If an error occurs during the ingestion process, raise a custom exception
            raise CustomException(e, sys) from e

    def __download_housing_data(self) -> str:
        """
        Downloads the housing data from the given URL and saves it to the specified directory.

        Returns:
            str: The file path where the data is downloaded and saved.

        Raises:
            CustomException: If there is an error during the download process.
        """
        try:
            # Get the download URL and the directory to save the downloaded file
            download_url = self.__data_ingestion_config.dataset_download_url
            tgz_download_dir = self.__data_ingestion_config.tgz_download_dir

            # Create the directory if it doesn't exist
            os.makedirs(tgz_download_dir, exist_ok=True)

            # Extract the file name from the download URL
            housing_file_name = os.path.basename(download_url)

            # Create the file path by combining the download directory and the file name
            tgz_file_path = os.path.join(tgz_download_dir, housing_file_name)

            # Download the file from the URL and save it to the specified path
            logging.info(f'downloading file from :[{download_url}] into :[{tgz_file_path}]')
            urllib.request.urlretrieve(download_url, tgz_file_path)
            logging.info(f'file :[{tgz_file_path}] has been downloaded successfully')

            # Return the file path where the data is downloaded and saved
            return tgz_file_path
        except Exception as e:
            # If there is an error during the download process, raise a custom exception
            raise CustomException(e, sys) from e

    def __extract_tgz_file(self, tgz_file_path: str) -> None:
        """
        Extracts a tar.gz file into a specified directory.
        
        Args:
            tgz_file_path (str): The path to the tar.gz file.
        
        Returns:
            None
        
        Raises:
            CustomException: If an error occurs during the extraction process.
        """
        try:
            # Get the directory where the extracted files will be stored
            raw_data_dir = self.__data_ingestion_config.raw_data_dir
            
            # If the directory already exists, remove it
            if os.path.exists(raw_data_dir):
                os.remove(raw_data_dir)
            
            # Create the directory if it doesn't exist
            os.makedirs(raw_data_dir, exist_ok=True)
            
            # Log the extraction process
            logging.info(f'extracting tgz file: [{tgz_file_path}] into dir: [{raw_data_dir}]')
            
            # Extract the tar.gz file into the specified directory
            with tarfile.open(tgz_file_path) as housing_tgz_file_obj:
                housing_tgz_file_obj.extractall(path=raw_data_dir)
            
            # Log the completion of the extraction process
            logging.info(f'extraction completed')
        except Exception as e:
            # Raise a custom exception if an error occurs during the extraction process
            raise CustomException(e, sys) from e

    def __split_data_as_train_test(self) -> DataIngestionArtifact:
        """
        Splits the data into train and test sets for data ingestion.

        Returns:
            DataIngestionArtifact: The artifact containing the file paths for the
            train and test datasets, as well as a flag indicating if the data
            ingestion was successful and a message describing the result.
        """
        try:
            # Get the directory of raw data
            raw_data_dir = self.__data_ingestion_config.raw_data_dir
            
            # Get the filename of the first file in the directory
            file_name = os.listdir(raw_data_dir)[0]
            
            # Get the full path of the housing file
            housing_file_path = os.path.join(raw_data_dir, file_name)

            # Read the housing data from the CSV file
            housing_data_frame = pd.read_csv(housing_file_path)
            
            # Create a new column 'income_cat' based on 'median_income' column
            housing_data_frame['income_cat'] = pd.cut(
                housing_data_frame['median_income'],
                bins=[0.0, 1.5, 3.0, 4.5, 6.0, np.inf],
                labels=[1, 2, 3, 4, 5]
            )

            # Split the data into train and test sets
            strat_train_set = None
            strat_test_set = None
            split = StratifiedShuffleSplit(n_splits=1, test_size=0.2, random_state=42)
            for train_index,test_index in split.split(housing_data_frame, housing_data_frame['income_cat']):
                strat_train_set = housing_data_frame.loc[train_index].drop(['income_cat'], axis=1)
                strat_test_set = housing_data_frame.loc[test_index].drop(['income_cat'], axis=1)

            # Get the file paths for train and test datasets
            train_file_path = os.path.join(
                self.__data_ingestion_config.ingested_train_dir,
                file_name
            )
            test_file_path = os.path.join(
                self.__data_ingestion_config.ingested_test_dir,
                file_name
            )
            
            # Export the train dataset to file
            if strat_train_set is not None:
                os.makedirs(self.__data_ingestion_config.ingested_train_dir, exist_ok=True)
                strat_train_set.to_csv(train_file_path, index=False)
            
            # Export the test dataset to file
            if strat_test_set is not None:
                os.makedirs(self.__data_ingestion_config.ingested_test_dir, exist_ok=True)
                strat_test_set.to_csv(test_file_path, index=False)

            # Create the data ingestion artifact
            data_ingestion_artifact = DataIngestionArtifact(
                train_file_path=train_file_path,
                test_file_path=test_file_path,
                is_ingested=True,
                message='data ingestion completed successfully'
            )

            return data_ingestion_artifact
        except Exception as e:
            raise CustomException(e, sys) from e

    def __del__(self):
        """
        A destructor method that is automatically called when an object is about to be destroyed.
        This method does not take any parameters and does not return any values.
        """
        try:
            pass
        except Exception as e:
            raise CustomException(e, sys) from e
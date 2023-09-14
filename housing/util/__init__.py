# housing/util/__init__.py
import os
import sys
import yaml
from housing.exception import CustomException
from housing.constant import DATASET_SCHEMA_COLUMNS_KEY

def read_yaml(file_path: str) -> dict:
    """
    Read a YAML file and return its contents as a dictionary.

    Parameters:
        file_path (str): The path to the YAML file.

    Returns:
        dict: The contents of the YAML file as a dictionary.

    Raises:
        CustomException: If there is an error reading the YAML file.
    """
    try:
        # Open the file in read binary mode
        with open(file_path, 'rb') as yaml_file:
            # Load the contents of the file using the yaml module
            return yaml.safe_load(yaml_file)
    except Exception as e:
        # If there's an exception, raise a CustomException with the original exception and the sys module
        raise CustomException(e, sys) from e

import os
import yaml
import sys

def write_yaml(file_path: str, data: dict=None) -> None:
    """
    Write YAML data to a file.

    Args:
        file_path (str): The path to the file.
        data (dict, optional): The YAML data to write. Defaults to None.

    Raises:
        CustomException: If an error occurs during the writing process.

    Returns:
        None: This function does not return anything.
    """
    try:
        # Create the directory for the file if it doesn't exist
        os.makedirs(os.path.dirname(file_path), exist_ok=True)
        
        # Open the file in write mode
        with open(file_path, 'w') as yaml_file:
            # If data is not None, dump the YAML data into the file
            if data is not None:
                yaml.dump(data, yaml_file)
    except Exception as e:
        # If an exception occurs, raise a CustomException with the original exception and the sys module
        raise CustomException(e, sys) from e

def save_numpy_array_data(file_path: str, array: np.array):
    """
    Saves a NumPy array to a file.

    Args:
        file_path (str): The path to the file where the array will be saved.
        array (np.array): The NumPy array to save.

    Raises:
        CustomException: If an exception occurs during the saving process.

    Returns:
        None
    """
    try:
        # Get the directory path from the file path
        dir_path = os.path.dirname(file_path)
        # Create the directory if it does not exist
        os.makedirs(dir_path, exist_ok=True)
        # Open the file in binary write mode
        with open(file_path, 'wb') as file_obj:
            # Save the array to the file using numpy's save function
            np.save(file_obj, array)
    except Exception as e:
        # If an exception occurs, raise a CustomException with the original exception and the sys module
        raise CustomException(e, sys) from e

def load_numpy_array_data(file_path: str) -> np.array:
    """
    Load data from a numpy array file.

    Parameters:
        file_path (str): The path to the numpy array file.

    Returns:
        np.array: The loaded numpy array.

    Raises:
        CustomException: If an exception occurs while loading the numpy array.

    """
    try:
        # Open the file in binary mode
        with open(file_path, 'rb') as file_obj:
            # Load the numpy array from the file
            return np.load(file_obj)
    except Exception as e:
        # If an exception occurs, raise a CustomException with the original exception and the sys module
        raise CustomException(e, sys) from e
    
def save_object(file_path:str, obj):
    try:
        dir_path = os.path.dirname(file_path)
        os.makedirs(dir_path, exist_ok=True)
        with open(file_path, "wb") as file_obj:
            dill.dump(obj, file_obj)
    except Exception as e:
        # If an exception occurs, raise a CustomException with the original exception and the sys module
        raise CustomException(e, sys) from e
    
def load_object(file_path:str):
    try:
        with open(file_path, "rb") as file_obj:
            return dill.load(file_obj)
    except Exception as e:
        # If an exception occurs, raise a CustomException with the original exception and the sys module
        raise CustomException(e, sys) from e
    
def load_data(file_path: str, schema_file_path: str) -> pd.DataFrame:
    """
    Load data from a CSV file into a pandas DataFrame using a given schema.

    Parameters:
        file_path (str): The path to the CSV file.
        schema_file_path (str): The path to the schema file.

    Returns:
        pd.DataFrame: The loaded data as a pandas DataFrame.

    Raises:
        CustomException: If any error occurs during the data loading process.
    """
    try:
        # Read the dataset schema from the schema file
        datatset_schema = read_yaml(schema_file_path)
        
        # Extract the schema from the dataset schema
        schema = datatset_schema[DATASET_SCHEMA_COLUMNS_KEY]
        
        # Read the data from the CSV file into a pandas DataFrame
        dataframe = pd.read_csv(file_path)
        
        # Initialize an empty error message
        error_message = ""
        
        # Iterate over each column in the DataFrame
        for column in dataframe.columns:
            # Check if the column is in the schema
            if column in list(schema.keys()):
                # Convert the column to the specified data type from the schema
                dataframe[column].astype(schema[column])
            else:
                # Append the error message if the column is not in the schema
                error_message = f"{error_message} \nColumn: [{column}] is not in the schema."
        
        # If there are any error messages, raise an exception
        if len(error_message) > 0:
            raise Exception(error_message)
        
        # Return the loaded data as a pandas DataFrame
        return dataframe
    except Exception as e:
        # If an exception occurs, raise a CustomException with the original exception and the sys module
        raise CustomException(e, sys) from e

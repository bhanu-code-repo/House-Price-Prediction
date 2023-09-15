# housing/component/feature_generator.py

# Import required libraries and packages
import sys
from sklearn.base import BaseEstimator, TransformerMixin

from housing.constant import *
from housing.exception import CustomException

class FeatureGenerator(BaseEstimator, TransformerMixin):

    def __init__(
        self,
        add_bedrooms_per_room=True,
        total_rooms_ix=3,
        population_ix=5,
        households_ix=6,
        total_bedrooms_ix=4,
        columns=None
    ) -> None:
        try:
            self.columns = columns
            if self.columns is not None:
                total_rooms_ix = self.columns.index(COLUMN_TOTAL_ROOMS)
                population_ix = self.columns.index(COLUMN_POPULATION)
                households_ix = self.columns.index(COLUMN_HOUSEHOLDS)
                total_bedrooms_ix = self.columns.index(COLUMN_TOTAL_BEDROOM)

            self.add_bedrooms_per_room = add_bedrooms_per_room
            self.total_rooms_ix = total_rooms_ix
            self.population_ix = population_ix
            self.households_ix = households_ix
            self.total_bedrooms_ix = total_bedrooms_ix
        except Exception as e:
            # Raise a custom exception if an error occurs during the extraction process
            raise CustomException(e, sys) from e
        
    def fit(self, X, y=None):
        """
        Fits the model to the training data.

        Parameters:
            X (array-like): The input features.
            y (array-like, optional): The target variable. Defaults to None.

        Returns:
            self: The fitted model.
        """
        return self
    
    def transform(self, X, y=None):
        """
        Transforms the input data by generating additional features based on the provided feature columns.

        Parameters:
            X (numpy.ndarray): The input feature matrix.
            y (numpy.ndarray, optional): The target labels. Defaults to None.

        Returns:
            numpy.ndarray: The transformed feature matrix with additional generated features.

        Raises:
            CustomException: If an error occurs during the extraction process.
        """
        
        try:
            # Calculate the number of rooms per household by dividing the total number of rooms by the number of households
            room_per_household = X[:, self.total_rooms_ix] / X[:, self.households_ix]
            
            # Calculate the population per household by dividing the total population by the number of households
            population_per_household = X[:, self.population_ix] / X[:, self.households_ix]
            
            if self.add_bedrooms_per_room:
                # Calculate the number of bedrooms per room by dividing the total number of bedrooms by the total number of rooms
                bedrooms_per_room = X[:, self.total_bedrooms_ix] / X[:, self.total_rooms_ix]
                
                # Generate the transformed feature matrix by concatenating the original feature matrix with the generated features
                generated_feature = np.c_[
                    X,
                    room_per_household,
                    population_per_household,
                    bedrooms_per_room
                ]
            else:
                # Generate the transformed feature matrix by concatenating the original feature matrix with the generated features
                generated_feature = np.c_[
                    X,
                    room_per_household,
                    population_per_household
                ]
            
            # Return the transformed feature matrix
            return generated_feature
        
        except Exception as e:
            # Raise a custom exception if an error occurs during the extraction process
            raise CustomException(e, sys) from e

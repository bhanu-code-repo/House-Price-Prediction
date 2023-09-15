# housing/component/housing_estimator.py

# Import required libraries and packages
import sys

# Housing Estimator Model Class 
class HousingEstimatorModel:
    """
    Housing Estimator Model class to implement the housing estimator model.
    
    Args:   
        preprocessing_object (object): The preprocessing object.    
        trained_model_object (object): The trained model object.
        
    Raises:
        CustomException: If an error occurs during the housing estimation process.
    """
    def __init__(self, preprocessing_object, trained_model_object):
        try:
            # Store the preprocessing and trained model objects
            self.preprocessing_object = preprocessing_object
            self.trained_model_object = trained_model_object
        except Exception as e: 
            # Raise a custom exception if an error occurs   
            raise CustomException(e, sys) from e
    
    def predict(self, X):
        """
        Make predictions on input data.

        Args:
            X (array-like): Input data to make predictions on.

        Returns:
            array-like: Predicted values.

        Raises:
            CustomException: If an error occurs during the prediction process.
        """
        try:
            # Transform input features
            transformed_feature = self.preprocessing_object.transform(X)
            
            # Make predictions using the trained model
            return self.trained_model_object.predict(transformed_feature)
        
        except Exception as e:
            # Raise a custom exception if an error occurs
            raise CustomException(e, sys) from e
            
    def __repr__(self):
        # Get the name of the class of the trained model object
        class_name = type(self.trained_model_object).__name__

        # Create a formatted string representation of the class name
        repr_string = f"{class_name}()"

        return repr_string

    def __str__(self):
        """
        Returns a string representation of the trained model object's class name.
        """
        return f"{type(self.trained_model_object).__name__}()"

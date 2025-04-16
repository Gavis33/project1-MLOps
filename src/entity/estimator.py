import sys 
import pandas as pd
from sklearn.pipeline import Pipeline

from src.logger import logging
from src.exception import MyException

class TargetValueMapping:
    def __init__(self):
        self.yes: int = 0
        self.no: int = 1
    def _asdict(self):
        """
        this method returns the mapping dictionary mapping keys to values
        """
        return self.__dict__
    def reverse_mapping(self):
        """
        this method returns the reverse mapping dictionary mapping values to keys
        """
        mapping_response = self._asdict()
        return dict(zip(mapping_response.values(), mapping_response.keys()))
    
class MyModel:
    def __init__(self, preprocessing_object: Pipeline, trained_model_object: object):
        """
        preprocessing_object: input preprocessing object
        trained_model_object: input object of trained model
        """
        self.preprocessing_object = preprocessing_object
        self.trained_model_object = trained_model_object

    def predict(self, df: pd.DataFrame) -> pd.DataFrame:
        """
        Function accepts a dataframe as input (with all custom transformations already applied) 
        applies scaling using preprocessing object and then performs prediction 
        """
        try:
            logging.info('Applying preprocessing to inputs')
            # Apply scaling transformations using the pre-trained preprocessing object
            transformed_features = self.preprocessing_object.transform(df)
            # Make predictions using the trained model
            logging.info('Using the trained model to obtain predictions')
            predictions = self.trained_model_object.predict(transformed_features)
            return predictions
        
        except Exception as e:
            raise MyException(e, sys) from e

    def __repr__(self):
        return f'{type(self.trained_model_object).__name__}()'
    
    def __str__(self):
        return f'{type(self.trained_model_object).__name__}()'
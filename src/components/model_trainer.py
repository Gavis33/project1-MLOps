import sys
import numpy as np
from typing import Tuple
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import accuracy_score, f1_score, precision_score, recall_score

from src.logger import logging
from src.exception import MyException
from src.entity.estimator import MyModel
from src.entity.config_entity import ModelTrainerConfig
from src.entity.artifact_entity import DataTransformationArtifact, ModelTrainerArtifact, ClassificationMetricArtifact
from src.utils.main_utils import load_numpy_array_data, load_object, save_object

class ModelTrainer:
    def __init__(self, data_transformation_artifact: DataTransformationArtifact, 
                 model_trainer_config: ModelTrainerConfig):
        """
        data_transformation_artifact: data transformation artifact
        model_trainer_config: model trainer configuration
        """
        self.data_transformation_artifact = data_transformation_artifact
        self.model_trainer_config = model_trainer_config

    def get_model_object_and_report(self, train: np.array, test: np.array) -> Tuple[object, object]:
        """
        This method trains a RandomForestClassifier with specified parameters,
        Returns the model object and classification report
        """
        try:
            logging.info('Training RandomForestClassifier with specified parameters')
            
            # Splitting train and test data into features and target variables
            X_train, y_train , X_test, y_test = train[:, :-1], train[:, -1], test[:, :-1], test[:, -1]
            logging.info('Splitting train and test data into features and target variables is done successfully')

            # Initialize and fit RandomForestClassifier with specified parameters
            model = RandomForestClassifier(
                n_estimators=self.model_trainer_config._n_estimators,
                min_samples_split=self.model_trainer_config._min_samples_split,
                min_samples_leaf=self.model_trainer_config._min_samples_leaf,
                max_depth=self.model_trainer_config._max_depth,
                criterion=self.model_trainer_config._criterion,
                random_state=self.model_trainer_config._random_state
            )

            # Fit the model on the training data
            model.fit(X_train, y_train)
            logging.info('Fitting RandomForestClassifier with specified parameters is done successfully')

            # Make predictions on the test data and calculate metrics
            y_pred = model.predict(X_test)
            accuracy = accuracy_score(y_test, y_pred)
            f1 = f1_score(y_test, y_pred)
            precision = precision_score(y_test, y_pred)
            recall = recall_score(y_test, y_pred)

            # Create a classification report / metrics report
            metric_artifiact = ClassificationMetricArtifact(f1_score=f1, precision_score=precision, recall_score=recall)
            return model, metric_artifiact

        except Exception as e:
            raise MyException(e, sys) from e
        
    def initiate_model_trainer(self) -> ModelTrainerArtifact:
        """
        This method trains a RandomForestClassifier with specified parameters,
        Returns the model object and classification report
        """
        try:
            logging.info('Initiating model trainer')
            print(f'Starting model training with parameters: {self.model_trainer_config}')

            # Load transformed train and test data
            train_arr = load_numpy_array_data(file_path=self.data_transformation_artifact.transformed_train_file_path)
            test_arr = load_numpy_array_data(file_path=self.data_transformation_artifact.transformed_test_file_path)
            logging.info('Loading transformed train and test data is done successfully')

            # Get model object and classification report
            trained_model, metric_artifact = self.get_model_object_and_report(train=train_arr, test=test_arr)
            logging.info('Getting model object and classification report is done successfully')

            # load preprocessor object
            preprocessor_obj = load_object(file_path=self.data_transformation_artifact.transformed_object_file_path)
            logging.info('Loading preprocessor object is done successfully')

            # check if model's accuracy meets the expected threshold
            if accuracy_score(train_arr[:, -1], trained_model.predict(train_arr[:, :-1])) < self.model_trainer_config.expected_accuracy:
                logging.info('Model accuracy is less than expected accuracy')
                raise Exception(f'Model accuracy is less than expected accuracy: {self.model_trainer_config.expected_accuracy}')
            
            # save model object that includes preprocessor object and trained model object
            my_model = MyModel(preprocessing_object=preprocessor_obj, trained_model_object=trained_model)
            save_object(self.model_trainer_config.trained_model_file_path, my_model)

            # create and return model trainer artifact
            model_trainer_artifact = ModelTrainerArtifact(
                trained_model_file_path=self.model_trainer_config.trained_model_file_path,
                metric_artifact=metric_artifact,
            )
            logging.info(f'Model trainer artifact: {model_trainer_artifact}')
            return metric_artifact
        
        except Exception as e:
            raise MyException(e, sys)
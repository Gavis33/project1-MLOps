import os 
import sys
import json
import pandas as pd

from src.logger import logging
from src.exception import MyException
from src.constants import SCHEMA_FILE_PATH
from src.utils.main_utils import read_yaml_file
from src.entity.config_entity import DataValidationConfig
from src.entity.artifact_entity import DataIngestionArtifact, DataValidationArtifact

class DataValidation:
    def __init__(self, data_ingestion_artifact: DataIngestionArtifact, data_validation_config: DataValidationConfig):
        """
        Args:
            data_ingestion_artifact (DataIngestionArtifact): Artifact generated from data ingestion.
            data_validation_config (DataValidationConfig): Configuration for data validation.
        """
        try:
            self.data_ingeston_artifact = data_ingestion_artifact
            self.data_validation_config = data_validation_config
            self.schema_config = read_yaml_file(file_path=SCHEMA_FILE_PATH)

        except Exception as e:  
            raise MyException(e, sys) from e
        
    def validate_number_of_columns(self, df: pd.DataFrame) -> bool:
        """
        Method to validate the number of columns in the dataframe.

        Args:
            df (pd.DataFrame): The dataframe to validate.

        Returns:
            bool: True if the number of columns is valid, False otherwise.
        """
        try:
            status = len(df.columns) == len(self.schema_config['columns'])
            logging.info(f"Is number of columns valid?: {status}")
            return status
        
        except Exception as e:
            raise MyException(e, sys) from e
        
    def is_column_exist(self, df: pd.DataFrame) -> bool:
        """
        Method to check if the required columns are present in the dataframe.

        Args:
            df (pd.DataFrame): The dataframe to check.

        Returns:
            bool: True if all required columns are present, False otherwise.
        """
        try:
            missing_numeric_cols = [col for col in self.schema_config['numerical_columns'] if col not in df.columns]
            if len(missing_numeric_cols) > 0:
                logging.info(f'Missing numeric columns: {missing_numeric_cols}')
                return False
            missing_categorical_cols = [col for col in self.schema_config['categorical_columns'] if col not in df.columns]
            if len(missing_categorical_cols) > 0:
                logging.info(f'Missing categorical columns: {missing_categorical_cols}')
                return False
            return True
        
        except Exception as e:
            raise MyException(e, sys) from e
        
    @staticmethod
    def read_data(file_path: str) -> pd.DataFrame:
        try:
            return pd.read_csv(file_path)
        
        except Exception as e:
            raise MyException(e, sys)
        
    def initiate_data_validation(self) -> DataValidationArtifact:
        """
        Method to initiate the data validation process.

        Returns:
            DataValidationArtifact: Artifact containing the status of the data validation.
        """
        try:
            validation_err_msg = ''
            logging.info('Entered initiate_data_validation method of DataValidation class')
            train_df = DataValidation.read_data(file_path=self.data_ingeston_artifact.trained_file_path)
            test_df = DataValidation.read_data(file_path=self.data_ingeston_artifact.test_file_path)

            status = self.validate_number_of_columns(df=train_df)
            if not status:
                validation_err_msg += 'Number of columns in train data is invalid.\n'
            else:
                logging.info(f'All columns in train data are valid. Number of columns: {train_df.shape[1]}, status: {status}')

            status = self.validate_number_of_columns(df=test_df)
            if not status:
                validation_err_msg += 'Number of columns in test data is invalid.\n'
            else:
                logging.info(f'All columns in test data are valid. Number of columns: {test_df.shape[1]}, status: {status}')

            status = self.is_column_exist(df=train_df)
            if not status:
                validation_err_msg += 'Columns are not valid in train data.\n'
            else:
                logging.info(f'All columns in train data are valid. Number of columns: {train_df.shape[1]}, status: {status}')

            status = self.is_column_exist(df=test_df)
            if not status:
                validation_err_msg += 'Columns are not valid in test data.\n'
            else:
                logging.info(f'All columns in test data are valid. Number of columns: {test_df.shape[1]}, status: {status}')

            validation_status = len(validation_err_msg) == 0

            data_validation_artifact = DataValidationArtifact(
                validation_status = validation_status,
                message = validation_err_msg,
                validation_report_file_path = self.data_validation_config.validation_report_file_path
            )

            os.makedirs(os.path.dirname(self.data_validation_config.validation_report_file_path), exist_ok=True)

            validation_report = {
                'validation_status': validation_status,
                'message': validation_err_msg.strip()
            }

            with open(self.data_validation_config.validation_report_file_path, 'w') as report_file:
                json.dump(validation_report, report_file, indent=4)

            logging.info('Exited initiate_data_validation method of DataValidation class successfully')
            logging.info(f'Data validation artifact: {data_validation_artifact}')
            return data_validation_artifact
        
        except Exception as e:
            raise MyException(e, sys) from e
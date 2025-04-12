import os
import sys

from pandas import DataFrame
from sklearn.model_selection import train_test_split

from src.logger import logging
from src.exception import MyException
from src.data_access.project1_data import Poject1Data
from src.entity.config_entity import DataIngestionConfig
from src.entity.artifact_entity import DataIngestionArtifact

class DataIngestion:
    def __init__(self, data_ingestion_config: DataIngestionConfig = DataIngestionConfig()):
        """
        Args:
            data_ingestion_config (DataIngestionConfig, optional): Configuration for data ingestion. Defaults to DataIngestionConfig().
        """
        try:
            self.data_ingestion_config = data_ingestion_config
        except Exception as e:
            raise MyException(e, sys)
        
    def export_data_into_feature_store(self) -> DataFrame:
        """
        Method to export data from MongoDB to a csv file in feature store
        """
        try:
            logging.info('Exporting data from MongoDB to a csv file in feature store')
            project1_data = Poject1Data()
            df = project1_data.export_collection_as_df(collection_name = self.data_ingestion_config.collection_name)
            logging.info(f'Shape of dataframe: {df.shape}')
            feature_store_file_path = self.data_ingestion_config.feature_store_file_path
            dir_path = os.path.dirname(feature_store_file_path)
            os.makedirs(dir_path, exist_ok=True)
            df.to_csv(feature_store_file_path, index=False, header=True) # header=True to include the column names in the csv file
            return df
        
        except Exception as e:
            raise MyException(e, sys)
        
    def split_data_as_train_test(self, df: DataFrame) -> None:
        """
        Method to split data into train and test sets and test based on split ratio. 
        Create a Folder in S3 bucket to store train and test data
        """
        try:
            train_set, test_set = train_test_split(df, test_size=self.data_ingestion_config.train_test_split_ratio)
            logging.info('Splitting data into train and test sets')

            os.makedirs(os.path.dirname(self.data_ingestion_config.train_file_path), exist_ok=True)

            logging.info(f'Exporting train data to file: {self.data_ingestion_config.train_file_path}')
            train_set.to_csv(self.data_ingestion_config.train_file_path, index=False, header=True)

            logging.info(f'Exporting test data to file: {self.data_ingestion_config.test_file_path}')
            train_set.to_csv(self.data_ingestion_config.train_file_path, index=False, header=True)
            test_set.to_csv(self.data_ingestion_config.test_file_path, index=False, header=True)
            logging.info(f'Train and test data is saved at {self.data_ingestion_config.train_file_path} and {self.data_ingestion_config.test_file_path}')

        except Exception as e:
            raise MyException(e, sys)
        
    def initiate_data_ingestion(self) -> DataIngestionArtifact:
        """
        Method to initiate data ingestion components of training pipeline.
        Train set and test set are returned as artifacts of data ingestion component
        """
        try:
            df = self.export_data_into_feature_store()
            logging.info('Fetched data from MongoDB')
            self.split_data_as_train_test(df)
            logging.info('Performed train test split on fetched dataset')
            data_ingestion_artifact = DataIngestionArtifact(trained_file_path=self.data_ingestion_config.train_file_path, test_file_path=self.data_ingestion_config.test_file_path)
            logging.info(f'Data ingestion artifact: {data_ingestion_artifact}')
            return data_ingestion_artifact
        except Exception as e:
            raise MyException(e, sys)
import sys
from src.logger import logging
from src.exception import MyException

from src.components.data_ingestion import DataIngestion
# more imports here

from src.entity.config_entity import (DataIngestionConfig)
# more imports here

from src.entity.artifact_entity import (DataIngestionArtifact)
# more imports here

class TrainPipeline:
    def __init__(self):
        self.data_ingestion_config = DataIngestionConfig()
        # more initializations here

    def start_data_ingestion(self) -> DataIngestionArtifact:
        try:
            logging.info('Entered start_data_ingestion method of TrainPipeline class')
            logging.info('Getting data from MongoDB')
            data_ingestion = DataIngestion(data_ingestion_config=self.data_ingestion_config)
            data_ingestion_artifact = data_ingestion.initiate_data_ingestion()
            logging.info('Exited start_data_ingestion method of TrainPipeline class successfully')
            return data_ingestion_artifact
        
        except Exception as e:
            raise MyException(e, sys)
        
    # more methods here

    def run_pipeline(self) -> None:
        try:
            data_ingestion_artifact = self.start_data_ingestion()
            # more code here

        except Exception as e:
            raise MyException(e, sys)
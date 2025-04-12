import sys
import numpy as np
import pandas as pd
from typing import Optional

from src.exception import MyException
from src.constants import DATABASE_NAME
from src.configuration.mongo_db_connection import MongoDBClient

class Poject1Data:
    """
    This class to export MongoDB data as pandas dataframe.
    """

    def __init__(self) -> None:
        """
        Initializes a connection to MongoDB using the MONGODB_URL_KEY environment variable. If no existing connection is available, it creates a new client and connects to MongoDB.
        """
        try:
            self.mongo_client = MongoDBClient(database_name=DATABASE_NAME)
        except Exception as e:
            raise MyException(e, sys)
        
    def export_collection_as_df(self, collection_name: str, database_name: Optional[str] = None) -> pd.DataFrame:
        """
        Export the entire collection as a pandas dataframe.

        Args:
            collection_name (str): The name of the collection to export.
            database_name (str, optional): The name of the database to connect to. Defaults to None.

        Returns:
            pd.DataFrame: The collection as a pandas dataframe, with 'id' and column removed and 'na' values replaced with 'NaN'.
        """
        try:
            # Access the collection from default or specified database
            if database_name is None:
                collection = self.mongo_client.database[collection_name]
            else:
                collection = self.mongo_client[database_name][collection_name]
            
            # convert collection to pandas dataframe and preprocess(remove 'id' and 'na' values)
            print(f'Exporting collection: {collection_name}')
            df = pd.DataFrame(list(collection.find()))
            print(f'Exported collection: {collection_name} with {df.shape[0]} rows and {df.shape[1]} columns and length: {len(df)}')
            if 'id' in df.columns.to_list():
                df = df.drop(columns=['id'], axis=1)
            df.replace({'na': np.nan}, inplace=True)
            return df
        
        except Exception as e:
            raise MyException(e, sys)
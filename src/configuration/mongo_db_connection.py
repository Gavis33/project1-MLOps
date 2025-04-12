import os
import sys
import certifi # for ssl certificate verification: https://pypi.org/project/certifi/ - for more info
import pymongo # for mongodb connection

from src.logger import logging
from src.exception import MyException
from src.constants import DATABASE_NAME, MONGODB_URL_KEY

# Load the certificate authority file to avoid timeout errors when connecting to MongoDB
ca =certifi.where()
logging.getLogger("pymongo").setLevel(logging.WARNING)

class MongoDBClient:
    """
    This class is used to connect to MongoDB

    Attributes:
    client: MongoClient - A shared MongoClient instance for the class
    database: Database - The specific database instance that MongoDBClient is connected to

    Methods:
    __init__(database_name: str) -> None: Initializes a new instance of MongoDBClient using the specified database name
    
    """

    client = None # A shared MongoClient instance across all instances of MongoDBClient

    def __init__(self, database_name: str = DATABASE_NAME) -> None:
        """
        Initializes a connection to MongoDB using the MONGODB_URL_KEY environment variable. If no existing connection is available, it creates a new client and connects to MongoDB.
        
        Args:
        database_name (str): The name of the database to connect to. Defaults to 'Project1'.
        
        Returns:
        None
        
        Raises:
        MyException: If an error occurs while connecting to MongoDB or if the MONGODB_URL_KEY environment variable is not set.
        
        """
        try:
            # Check if a MongoDB client connection is already established, otherwise create a new one
            if MongoDBClient.client is None:
                mongo_db_url = os.getenv(MONGODB_URL_KEY) # Get the MongoDB connection URL from the environment variable
                if mongo_db_url is None:
                    raise Exception(f'{MONGODB_URL_KEY} is not set as an environment variable.') # If the environment variable is not set, raise an exception
                
                # Connect to MongoDB using the MONGODB_URL_KEY environment variable
                MongoDBClient.client = pymongo.MongoClient(mongo_db_url, tlsCAFile=ca) # tlsCAFile is for ssl certificate verification: https://pypi.org/project/certifi/ - for more info

            # Get the database instance
            self.client = MongoDBClient.client
            self.database = self.client[database_name]
            self.database_name = database_name
            logging.info(f'Connected to MongoDB database: {database_name}')
        
        except Exception as e:
            raise MyException(e, sys)
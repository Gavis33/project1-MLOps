import os
from datetime import date

# For MongoDB Connection
DATABASE_NAME = 'Project1'
COLLECTION_NAME = 'Project1_Data'
MONGODB_URL_KEY = 'MONGODB_URL'

PIPELINE_NAME: str = '' 
ARTIFACT_DIR: str = 'artifact'

MODEL_FILE_NAME = 'model.pkl'

TARGET_COLUMN = 'Response' 
CURRENT_YEAR = date.today().year
PREPROCESSING_OBJECT_FILE_NAME = 'preprocessing.pkl'

FILE_NAME: str = 'data.csv'
TRAIN_FILE_NAME: str = 'train.csv'
TEST_FILE_NAME: str = 'test.csv'

SCHEMA_FILE_PATH = os.path.join('config', 'schema.yaml') # path to schema.yaml which contains the schema(structure) for the dataset

AWS_ACCESS_KEY_ID_ENV_KEY = 'AWS_ACCESS_KEY_ID'
AWS_SECRET_ACCESS_KEY_ENV_KEY = 'AWS_SECRET_ACCESS_KEY'
REGION_NAME = 'us-east-1'

# Data ingestion related constants with DATA_INGESTION VAR NAME
DATA_INGESTION_COLLECTION_NAME: str = 'Project1_Data'
DATA_INGETSION_DIR_NAME: str = 'data_ingestion'
DATA_INGESTION_FEATURE_STORE_DIR: str = 'feature_store' 
DATA_INGESTION_INGESTED_DIR: str = 'ingested'
DATA_INGESTION_TRAIN_TEST_SPLIT_RATIO: float = 0.25

# Data Validation related constants with DATA_VALIDATION VAR NAME
DATA_VALIDATION_DIR_NAME: str = 'data_validation'
DATA_VALIDATION_REPORT_FILE_NAME: str = 'report.yaml'

# Data Transformation related constants with DATA_TRANSFORMATION VAR NAME
DATA_TRANSFORMATION_DIR_NAME: str = 'data_transformation'
DATA_TRANSFORMATION_TRANSFORMED_DATA_DIR: str = 'transformed'
DATA_TRANSFORMATION_TRANSFORMED_OBJECT_DIR: str = 'transformed_object'

# Model Trainer related constants with MODEL_TRAINER VAR NAME
MODEL_TRAINER_DIR_NAME: str = 'model_trainer'
MODEL_TRAINER_TRAINED_MODEL_DIR: str = 'trained_model'
MODEL_TRAINER_TRAINED_MODEL_NAME: str = 'model.pkl'
MODEL_TRAINER_EXPECTED_SCORE: float = 0.6
MODEL_TRAINER_MODEL_CONFIG_FILE_PATH: str = os.path.join('config', 'model.yaml')
MODEL_TRAINER_N_ESTIMATORS = 200
MODEL_TRAINER_MIN_SAMPLES_SPLIT: int = 7 # minimum number of samples required to be at a node/split before it is split
MODEL_TRAINER_MIN_SAMPLES_LEAF: int = 6 # minimum number of samples required to be at a leaf node 
MIN_SAMPLES_SPLIT_MAX_DEPTH: int = 10 # maximum depth of the tree
MIN_SAMPLES_SPLIT_CRITERION: str = 'entropy'
MIN_SAMPLES_SPLIT_RANDOM_STATE: int = 101 

# Model Evaluation related constants with MODEL_EVALUATION VAR NAME
MODEL_EVALUATION_CHANGED_THRESHOLD_SCORE: float = 0.02
MODEL_BUCKET_NAME = 'my-model-project1mlops'
MODEL_PUSHER_S3_KEY  = 'model-registry'

APP_HOST = '0.0.0.0'
APP_PORT = 5000
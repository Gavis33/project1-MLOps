import os
from src.constants import *
from datetime import datetime
from dataclasses import dataclass

TIMESTAMP: str = datetime.now().strftime('%m_%d_%Y_%H_%M_%S')

@dataclass
class TrainingPipelineConfig:
    pipeline_name = PIPELINE_NAME
    artifact_dir = os.path.join(ARTIFACT_DIR, TIMESTAMP)
    timestamp: str = TIMESTAMP

training_pipeline_config = TrainingPipelineConfig = TrainingPipelineConfig()

@dataclass
class DataIngestionConfig:
    data_ingestion_dir: str = os.path.join(training_pipeline_config.artifact_dir, DATA_INGETSION_DIR_NAME)
    feature_store_file_path: str = os.path.join(data_ingestion_dir, DATA_INGESTION_FEATURE_STORE_DIR, FILE_NAME)
    train_file_path: str = os.path.join(data_ingestion_dir, DATA_INGESTION_INGESTED_DIR, TRAIN_FILE_NAME)
    test_file_path: str = os.path.join(data_ingestion_dir, DATA_INGESTION_INGESTED_DIR, TEST_FILE_NAME)
    train_test_split_ratio: float = DATA_INGESTION_TRAIN_TEST_SPLIT_RATIO
    collection_name: str = DATA_INGESTION_COLLECTION_NAME

@dataclass
class DataValidationConfig:
    data_validation_dir: str = os.path.join(training_pipeline_config.artifact_dir, DATA_VALIDATION_DIR_NAME)
    validation_report_file_path: str = os.path.join(data_validation_dir, DATA_VALIDATION_REPORT_FILE_NAME)

@dataclass
class DataTransformationConfig:
    data_transformation_dir: str = os.path.join(training_pipeline_config.artifact_dir, DATA_TRANSFORMATION_DIR_NAME)
    transformed_train_file_path: str = os.path.join(data_transformation_dir, DATA_TRANSFORMATION_TRANSFORMED_DATA_DIR, TRAIN_FILE_NAME.replace('csv', 'npy'))
    transformed_test_file_path: str = os.path.join(data_transformation_dir, DATA_TRANSFORMATION_TRANSFORMED_DATA_DIR, TEST_FILE_NAME.replace('csv', 'npy'))
    transformed_object_file_path: str = os.path.join(data_transformation_dir, DATA_TRANSFORMATION_TRANSFORMED_OBJECT_DIR, PREPROCESSING_OBJECT_FILE_NAME)

@dataclass
class ModelTrainerConfig:
    model_trainer_dir: str = os.path.join(training_pipeline_config.artifact_dir, MODEL_TRAINER_DIR_NAME)
    trained_model_file_path: str = os.path.join(model_trainer_dir, MODEL_TRAINER_TRAINED_MODEL_DIR, MODEL_FILE_NAME)
    model_config_file_path: str = MODEL_TRAINER_MODEL_CONFIG_FILE_PATH
    expected_accuracy: float = MODEL_TRAINER_EXPECTED_SCORE
    _n_estimators: int = MODEL_TRAINER_N_ESTIMATORS
    _min_samples_split: int = MODEL_TRAINER_MIN_SAMPLES_SPLIT
    _min_samples_leaf: int = MODEL_TRAINER_MIN_SAMPLES_LEAF
    _max_depth: int = MIN_SAMPLES_SPLIT_MAX_DEPTH
    _criterion: str = MIN_SAMPLES_SPLIT_CRITERION
    _random_state: int = MIN_SAMPLES_SPLIT_RANDOM_STATE


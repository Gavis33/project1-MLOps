import sys 
import numpy as np
import pandas as pd
from imblearn.combine import SMOTEENN
from sklearn.pipeline import Pipeline
from sklearn.compose import ColumnTransformer
from sklearn.preprocessing import StandardScaler, MinMaxScaler

from src.logger import logging
from src.exception import MyException
from src.entity.config_entity import DataTransformationConfig
from src.entity.artifact_entity import DataTransformationArtifact, DataIngestionArtifact, DataValidationArtifact
from src.constants import TARGET_COLUMN, SCHEMA_FILE_PATH, CURRENT_YEAR
from src.utils.main_utils import save_object, save_numpy_array_data, read_yaml_file

class DataTransformation:
    def __init__(self, data_ingestion_artifact: DataIngestionArtifact,
                 data_transformation_config: DataTransformationConfig,
                 data_validation_artifact: DataValidationArtifact):
        try:
            self.data_ingestion_artifact = data_ingestion_artifact
            self.data_transformation_config = data_transformation_config
            self.data_validation_artifact = data_validation_artifact
            self._schema_config = read_yaml_file(file_path=SCHEMA_FILE_PATH)

        except Exception as e:
            raise MyException(e, sys)
    
    @staticmethod
    def read_data(file_path: str) -> pd.DataFrame:
        try:
            return pd.read_csv(file_path)
        except Exception as e:
            raise MyException(e, sys)
        
    def get_data_transformer_object(self) -> Pipeline:
        """
        Creates and returns a data transformer object for the pipeline including gender mapping, dummy encoding and scaling and type conversion
        """
        logging.info('Entered get_data_transformer_object method of DataTransformation class')
        try:
            # initialize the transformers
            numeric_transformer = StandardScaler()
            min_max_scaler = MinMaxScaler()
            logging.info('Transformers initialized: StandardScaler, MinMaxScaler')

            # load schema config from yaml
            num_features = self._schema_config['num_features']
            mm_columns = self._schema_config['mm_columns']
            logging.info('Columns initialized: num_features, mm_columns')

            # create the preprocessor pipeline with the transformers
            preprocessor = ColumnTransformer(
                transformers=[
                    ('StandardScaler', numeric_transformer, num_features),
                    ('MinMaxScaler', min_max_scaler, mm_columns) 
                ],
                remainder = 'passthrough' # leaves the categorical columns as it is
            )

            # wrapping the preprocessor into a pipeline
            final_pipeline = Pipeline(steps=[('Preprocessor', preprocessor)])
            logging.info('Final pipeline created. Exited get_data_transformer_object method of DataTransformation class')
            return final_pipeline
        
        except Exception as e:
            raise MyException(e, sys) from e
        
    def _map_gender_column(self, df):
        """"
        Maps the gender column to numeric values- 1 for Male and 0 for Female
        """
        logging.info('Entered _map_gender_column method of DataTransformation class')
        df['Gender'] = df['Gender'].map({'Female': 0, 'Male': 1}).astype(int)
        return df

    def _create_dummy_columns(self, df):
        """
        Creates dummy columns for the categorical columns
        """
        logging.info('Entered _create_dummy_columns method of DataTransformation class')
        df = pd.get_dummies(df, drop_first=True) # drop first column to avoid multicollinearity(one of the dummy columns is a linear combination of the other dummy columns)
        return df 

    def _renanme_columns(self, df):
        """
        Renames specific columns and ensure integer type for dummy columns
        """
        logging.info('Entered _renanme_columns method of DataTransformation class')
        df = df.rename(columns={
            'Vehicle_Age_< 1 Year': 'Vehicle_Age_lt_1_Year',
            'Vehicle_Age_> 2 Year': 'Vehicle_Age_gt_2_Year',
        })
        for col in df.columns:
            df[col] = df[col].astype(int) # ensure integer type for dummy columns
        return df
    
    def _drop_id_column(self, df):
        """
        Drops the id column if present
        """
        logging.info('Entered _drop_id_column method of DataTransformation class')
        drop_col = self._schema_config['drop_columns']
        if drop_col in df.columns:
            df = df.drop(drop_col, axis=1)
        return df
    
    def initiate_data_transformation(self) -> DataTransformationArtifact:
        """
        Initiates the data transformation process for the pipeline and returns a DataTransformationArtifact object.
        """
        try:
            logging.info('Data Transformation started...')
            if not self.data_validation_artifact.validation_status:
                raise Exception(self.data_validation_artifact.message)
            
            # load data
            train_df = self.read_data(file_path=self.data_ingestion_artifact.trained_file_path)
            test_df = self.read_data(file_path=self.data_ingestion_artifact.test_file_path)
            logging.info('Train and test data loaded')

            input_features_train_df = train_df.drop(columns=[TARGET_COLUMN], axis=1)
            target_feature_train_df = train_df[TARGET_COLUMN]
            
            input_features_test_df = test_df.drop(columns=[TARGET_COLUMN], axis=1)
            target_feature_test_df = test_df[TARGET_COLUMN]
            
            logging.info('Input and target features loaded for Train and test data')

            # apply custom transformations to the data in specific order
            input_features_train_df = self._map_gender_column(input_features_train_df)
            input_features_train_df = self._drop_id_column(input_features_train_df)
            input_features_train_df = self._create_dummy_columns(input_features_train_df)
            input_features_train_df = self._renanme_columns(input_features_train_df)

            input_features_test_df = self._map_gender_column(input_features_test_df)
            input_features_test_df = self._drop_id_column(input_features_test_df)
            input_features_test_df = self._create_dummy_columns(input_features_test_df)
            input_features_test_df = self._renanme_columns(input_features_test_df)

            logging.info('Custom transformations applied to the data')

            logging.info('Statrting data transformation')
            preprocessor = self.get_data_transformer_object()
            logging.info('Preprocessor initialized')

            input_feature_train_arr = preprocessor.fit_transform(input_features_train_df) # fit_transform is a method that returns a numpy array of transformed data and also fits the transformer to the data(learn the parameters)
            input_feature_test_arr = preprocessor.transform(input_features_test_df) # transform returns a numpy array of transformed data
            logging.info('Data transformation completed')

            logging.info('Applying SMOTEENN for handling imbalanced dataset...')
            smt = SMOTEENN(sampling_strategy="minority")
            input_feature_train_final, target_feature_train_final = smt.fit_resample(
                input_feature_train_arr, target_feature_train_df
            )
            input_feature_test_final, target_feature_test_final = smt.fit_resample(
                input_feature_test_arr, target_feature_test_df
            )
            logging.info("SMOTEENN applied to train-test df.")

            train_arr = np.c_[input_feature_train_final, np.array(target_feature_train_final)]
            test_arr = np.c_[input_feature_test_final, np.array(target_feature_test_final)]
            logging.info('feature-target concatenation done for train-test split')

            save_object(self.data_transformation_config.transformed_object_file_path, preprocessor)
            save_numpy_array_data(self.data_transformation_config.transformed_train_file_path, array=train_arr)
            save_numpy_array_data(self.data_transformation_config.transformed_test_file_path, array=test_arr)
            logging.info('Saved transformation objest and transformed object')
            logging.info('Data transformation completed successfully...')

            return DataTransformationArtifact(
                transformed_object_file_path=self.data_transformation_config.transformed_object_file_path,
                transformed_train_file_path=self.data_transformation_config.transformed_train_file_path,
                transformed_test_file_path=self.data_transformation_config.transformed_test_file_path
            )
        
        except Exception as e:
            raise MyException(e, sys) from e
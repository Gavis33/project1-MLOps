import os
import sys
import yaml
import dill
import numpy as np
from pandas import DataFrame
from src.logger import logging
from src.exception import MyException

def read_yaml_file(file_path: str) -> dict:
    """
    Reads a YAML file and returns the contents as a dictionary.
    
    Args:
        file_path (str): The path to the YAML file.
        
    Returns:
        dict: The contents of the YAML file as a dictionary.
    """
    try:
        with open(file_path, 'rb') as yaml_file:
            return yaml.safe_load(yaml_file)
    except Exception as e:
        raise MyException(e, sys)
    
def write_yaml_file(file_path: str, content: object, replace: bool = False) -> None:
    """
    Writes a Python object to a YAML file.
    
    Args:
        file_path (str): The path to the YAML file.
        content (object): The Python object to be written to the YAML file.
        replace (bool, optional): Whether to replace the file if it already exists. Defaults to False.
    """
    try:
        if replace:
            if os.path.exists(file_path):
                os.remove(file_path)
        os.makedirs(os.path.dirname(file_path), exist_ok=True)
        with open(file_path, 'w') as file:
            yaml.dump(content, file)
    except Exception as e:
        raise MyException(e, sys)
    
def load_object(file_path: str) -> object:
    """
    Loads an object from a file using dill (a Python serialization(pickling/marshalling) library).
    
    Args:
        file_path (str): The path to the file containing the object.
        
    Returns:
        object: The loaded object.
    """
    try:
        with open(file_path, 'rb') as file_obj:
            obj = dill.load(file_obj)
        return obj
    except Exception as e:
        raise MyException(e, sys)
    
def save_numpy_array_data(file_path: str, array: np.array):
    """
    Saves a NumPy array to a file.
    
    Args:
        file_path (str): The path to the file where the array will be saved.
        array (np.array): The NumPy array to be saved.
    """
    try:
        os.makedirs(os.path.dirname(file_path), exist_ok=True)
        with open(file_path, 'wb') as file_obj:
            np.save(file_obj, array)
    except Exception as e:
        raise MyException(e, sys)
    
def load_numpy_array_data(file_path: str) -> np.array:
    """
    Loads a NumPy array from a file.
    
    Args:
        file_path (str): The path to the file containing the NumPy array.
        
    Returns:
        np.array: The loaded NumPy array.
    """
    try:
        with open(file_path, 'rb') as file_obj:
            return np.load(file_obj)
    except Exception as e:
        raise MyException(e, sys)
    
def save_object(file_path: str, obj: object) -> None:
    logging.info('Entered the save_object method of MainUtils class')
    try:
        os.makedirs(os.path.dirname(file_path), exist_ok=True)
        with open(file_path, 'wb') as file_obj:
            dill.dump(obj, file_obj)
        logging.info('Exited the save_object method of MainUtils class')
    except Exception as e:
        raise MyException(e, sys)
    
def drop_columns(df: DataFrame, cols_to_drop: list) -> DataFrame:
    """
    Drops specified columns from a DataFrame.
    
    Args:
        df (DataFrame): The DataFrame to drop columns from.
        cols_to_drop (list): A list of column names to drop.
        
    Returns:
        DataFrame: The DataFrame with the specified columns dropped.
    """
    logging.info('Dropping columns')
    try:
        df = df.drop(columns=cols_to_drop, axis=1)
        logging.info('Exited drop_columns method of utils')
        return df
    except Exception as e:
        raise MyException(e, sys) from e
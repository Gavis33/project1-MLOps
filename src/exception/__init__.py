import sys
import logging

def error_message_detail(error: Exception, error_detail: sys) -> str:
    """
    Extracts detailed error information from an exception and its traceback.
    including the error message, error type, and traceback details ie file name, line number, etc.
    Args:
        error (Exception): The exception object.
        error_detail (sys): The traceback object.

    Returns:
        str: A string containing the error message and traceback details.
    """

    # Extracting the traceback information (exception type, error message, and traceback details)
    _, _, exc_tb = error_detail.exc_info()

    # Get the filename where the exception occured
    file_name = exc_tb.tb_frame.f_code.co_filename

    # Create a formatted error message with file name, line number, and error message
    line_number = exc_tb.tb_lineno
    error_message = f'Error occured in python script name {file_name} at line number {line_number}: Error message: {str(error)}'

    # Log the error for better tracking
    logging.info(error_message)

    return error_message

class MyException(Exception):
    """
    Custom exception class for handling errors in the US visa application.
    """
    def __init__(self, error_message: str, error_detail: sys):
        """
        Initializes a new instance of the MyException class with a detailed error message and traceback.

        Args:
            error_message (str): A detailed error message.
            error_detail (sys): The traceback object.

        Returns:
            None
        """
        # Call the parent class constructor with the error message
        super().__init__(error_message)

        # Format the error message with file name, line number, and error message
        self.error_message = error_message_detail(error_message, error_detail)

    def __str__(self) -> str:
        """
        Returns a string representation of the MyException object.
        Returns:
            str: A formatted error message.
        """
        return self.error_message
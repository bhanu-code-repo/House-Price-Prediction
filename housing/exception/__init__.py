# housing/exception/__init__.py
import os
import sys

class CustomException(Exception):

    def __init__(self, error_message: Exception, error_detail: sys) -> None:
        super().__init__(error_message)
        self.error_message=CustomException.get_message(error_message=error_message, error_detail=error_detail)

    
@staticmethod
def get_message(error_message: Exception, error_detail: sys) -> str:
    """
    Generates a formatted error message with information about the error location and details.

    Args:
        error_message (Exception): The error message that triggered the exception.
        error_detail (sys): The details of the error.

    Returns:
        str: The formatted error message containing the script name, try block line number, exception block line number, and error message.
    """
    # Get the traceback of the error
    _, _ , exec_tb = error_detail.exc_info()
    
    # Get the line number where the exception occurred
    exception_block_line_number = exec_tb.tb_frame.f_lineno
    
    # Get the line number where the try block started
    try_block_line_number = exec_tb.tb_lineno
    
    # Get the filename of the script where the error occurred
    file_name = exec_tb.tb_frame.f_code.co_filename
    
    # Create the formatted error message with all the information
    error_message = f'''
    error occured in script:
    [{file_name}] at
    try block line number: [{try_block_line_number}] and exception block line number: [{exception_block_line_number}]
    error message: [{error_message}]
    '''
    
    # Return the formatted error message
    return error_message
    
    def __str__(self) -> str:
        """
        Convert the object to a string representation.

        :return: A string representation of the object.
        :rtype: str
        """
        return self.error_message

    def __repr__(self) -> str:
        """
        Return a string representation of the CustomException object.

        Returns:
            str: The string representation of the CustomException object.
        """
        return CustomException.__name__.str()
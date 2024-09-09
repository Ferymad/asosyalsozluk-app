import logging
import traceback
import streamlit as st

# Configure logging
logging.basicConfig(filename='app.log', level=logging.ERROR, 
                    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

def handle_error(error: Exception, user_message: str = "An error occurred. Please try again."):
    """
    Handle exceptions by logging them and displaying a user-friendly message.
    
    Args:
    error (Exception): The exception that was raised.
    user_message (str): A user-friendly message to display in the Streamlit app.
    """
    # Log the full error with traceback
    logger.error(f"An error occurred: {str(error)}\n{traceback.format_exc()}")
    
    # Display a user-friendly message in the Streamlit app
    st.error(user_message)

def custom_exception_handler(func):
    """
    A decorator to wrap functions with custom error handling.
    
    Usage:
    @custom_exception_handler
    def some_function():
        # function code here
    """
    def wrapper(*args, **kwargs):
        try:
            return func(*args, **kwargs)
        except Exception as e:
            handle_error(e)
    return wrapper
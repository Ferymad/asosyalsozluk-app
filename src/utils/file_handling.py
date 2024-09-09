import os
import tempfile
from typing import Union
import streamlit as st

def save_uploaded_file(uploaded_file: st.UploadedFile) -> Union[str, None]:
    """
    Save the uploaded file to a temporary directory.
    
    Args:
    uploaded_file (st.UploadedFile): The uploaded file object from Streamlit.
    
    Returns:
    Union[str, None]: The path to the saved file, or None if an error occurred.
    """
    try:
        with tempfile.NamedTemporaryFile(delete=False, suffix='.csv') as tmp_file:
            tmp_file.write(uploaded_file.getvalue())
            return tmp_file.name
    except Exception as e:
        st.error(f"Error saving file: {e}")
        return None

def remove_temp_file(file_path: str) -> None:
    """
    Remove a temporary file.
    
    Args:
    file_path (str): The path to the file to be removed.
    """
    try:
        os.remove(file_path)
    except Exception as e:
        st.warning(f"Error removing temporary file: {e}")

def get_file_size(file_path: str) -> int:
    """
    Get the size of a file in bytes.
    
    Args:
    file_path (str): The path to the file.
    
    Returns:
    int: The size of the file in bytes.
    """
    return os.path.getsize(file_path)

def is_file_empty(file_path: str) -> bool:
    """
    Check if a file is empty.
    
    Args:
    file_path (str): The path to the file.
    
    Returns:
    bool: True if the file is empty, False otherwise.
    """
    return get_file_size(file_path) == 0

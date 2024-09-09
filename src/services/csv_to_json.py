import csv
import json
from typing import List, Dict, Any
import streamlit as st
import pandas as pd

def csv_to_json(csv_content: str) -> List[Dict[str, Any]]:
    """
    Convert CSV content to a list of dictionaries (JSON-like structure).
    
    Args:
    csv_content (str): The content of the CSV file as a string.
    
    Returns:
    List[Dict[str, Any]]: A list of dictionaries, each representing a blog post.
    """
    blog_posts = []
    
    # Use StringIO to create a file-like object from the string
    from io import StringIO
    csv_file = StringIO(csv_content)
    
    csv_reader = csv.DictReader(csv_file)
    
    for row in csv_reader:
        post = {
            "skor": int(row["skor"]),
            "baslik": row["baslik"],
            "entiri": row["entiri"],
            "silinmis": row["silinmis"].lower() == "true",
            "tarih": row["tarih"]
        }
        blog_posts.append(post)
    
    return blog_posts

def convert_csv_to_json(csv_content: str) -> str:
    """
    Convert CSV content to a JSON string.
    
    Args:
    csv_content (str): The content of the CSV file as a string.
    
    Returns:
    str: JSON string representation of the data.
    """
    blog_posts = csv_to_json(csv_content)
    return json.dumps(blog_posts, ensure_ascii=False, indent=2)

# Example usage within Streamlit app
def process_uploaded_file(file_path):
    try:
        # Read the CSV file
        df = pd.read_csv(file_path)
        
        # Convert DataFrame to list of dictionaries
        json_data = df.to_dict('records')
        
        return json_data
    except Exception as e:
        print(f"An error occurred while processing the file: {str(e)}")
        return None

# This part is for testing purposes and won't be executed in the Streamlit app
if __name__ == "__main__":
    # You can add test code here if needed
    pass
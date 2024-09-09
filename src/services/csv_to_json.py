import csv
import json
from typing import List, Dict, Any
import streamlit as st

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
def process_uploaded_file(uploaded_file):
    if uploaded_file is not None:
        try:
            # Read the content of the uploaded file
            csv_content = uploaded_file.getvalue().decode("utf-8")
            
            # Convert CSV to JSON
            json_data = convert_csv_to_json(csv_content)
            
            st.success("File successfully converted!")
            
            # You can choose to display the JSON data or save it to a file here
            st.json(json_data)
            
            return json_data
        
        except Exception as e:
            st.error(f"An error occurred while processing the file: {str(e)}")
            return None
    
    return None

# This part is for testing purposes and won't be executed in the Streamlit app
if __name__ == "__main__":
    # You can add test code here if needed
    pass
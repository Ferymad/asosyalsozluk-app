import streamlit as st
import pandas as pd
from services.csv_to_json import csv_to_json
from utils.file_handling import save_uploaded_file
from utils.data_validation import validate_csv_structure

def upload_csv():
    st.header("Upload your asosyalsozluk.com CSV file")
    
    uploaded_file = st.file_uploader("Choose a CSV file", type="csv")
    
    if uploaded_file is not None:
        try:
            # Save the uploaded file temporarily
            temp_file_path = save_uploaded_file(uploaded_file)
            
            # Validate the CSV structure
            if not validate_csv_structure(temp_file_path):
                st.error("The uploaded file does not have the expected structure. Please ensure it's a valid asosyalsozluk.com export.")
                return None
            
            # Read the CSV file
            df = pd.read_csv(temp_file_path)
            
            # Convert CSV to JSON
            json_data = csv_to_json(df)
            
            st.success("File successfully uploaded and converted!")
            
            return json_data
        
        except Exception as e:
            st.error(f"An error occurred while processing the file: {str(e)}")
            return None
    
    return None

def display_upload_status(json_data):
    if json_data:
        st.write(f"Number of entries: {len(json_data)}")
        st.json(json_data[0])  # Display the first entry as an example
    else:
        st.info("Please upload a CSV file to get started.")

# Main function to run the upload component
def run_upload_component():
    json_data = upload_csv()
    display_upload_status(json_data)
    return json_data
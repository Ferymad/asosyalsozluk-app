import streamlit as st
import json
import os
from services.csv_to_json import process_uploaded_file
from components.display_component import display_entries
from components.search_filter_component import run_search_filter_component
from components.visualization_component import run_visualization_component, prepare_data

# Initialize session state
if 'json_data' not in st.session_state:
    st.session_state.json_data = None

@st.cache_data
def process_data(file_path):
    json_data = process_uploaded_file(file_path)
    return json_data if json_data else None

def save_uploaded_file(uploaded_file):
    """Save the uploaded file to a temporary directory."""
    try:
        if not os.path.exists("temp"):
            os.makedirs("temp")
        with open(os.path.join("temp", uploaded_file.name), "wb") as f:
            f.write(uploaded_file.getbuffer())
        return os.path.join("temp", uploaded_file.name)
    except Exception as e:
        st.error(f"Error saving file: {e}")
        return None

# Main app logic
def main():
    st.title("Asosyal Sözlük Veri Analizi")

    uploaded_file = st.file_uploader("CSV dosyasını yükleyin", type="csv")

    if uploaded_file is not None:
        file_path = save_uploaded_file(uploaded_file)
        if file_path:
            json_data = process_data(file_path)
            if json_data:
                st.session_state.json_data = json_data
                df = prepare_data(json_data)
                
                run_search_filter_component(json_data)
                run_visualization_component(df)
                display_entries(json_data)
            else:
                st.error("Dosya işlenirken bir hata oluştu.")
        else:
            st.error("Dosya yüklenirken bir hata oluştu.")

if __name__ == "__main__":
    main()
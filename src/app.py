import streamlit as st
import json
import os
from services.csv_to_json import process_uploaded_file
from components.display_component import display_entries
from components.search_filter_component import run_search_filter_component
from components.visualization_component import run_visualization_component

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

def main():
    st.set_page_config(page_title="asosyalsozluk.com Arşiv Görüntüleyici", page_icon="📚", layout="wide")
    
    # Add reload button to sidebar
    if st.sidebar.button("Uygulamayı Yenile"):
        st.rerun()

    st.title("asosyalsozluk.com Arşiv Görüntüleyici")
    st.write("Eski asosyalsozluk.com girilerinizi görüntülemek ve keşfetmek için kullanın.")
    
    # File upload
    uploaded_file = st.file_uploader("CSV dosyası seç", type="csv")
    
    if uploaded_file is not None:
        if 'processed_data' not in st.session_state or st.session_state.processed_data is None:
            with st.spinner("Dosya işleniyor..."):
                file_path = save_uploaded_file(uploaded_file)
                if file_path:
                    processed_data = process_data(file_path)
                    if processed_data:
                        st.session_state.processed_data = processed_data
                        st.success("Dosya başarıyla yüklendi ve işlendi!")
                    else:
                        st.error("Dosya işlenirken bir hata oluştu.")
                else:
                    st.error("Dosya kaydedilirken bir hata oluştu.")
    
    if 'processed_data' in st.session_state and st.session_state.processed_data:
        filtered_entries = run_search_filter_component(st.session_state.processed_data)
        
        # Display entries as before
        display_entries(filtered_entries)
        
        # Run visualization component
        run_visualization_component(filtered_entries)
    
    # Footer
    st.markdown("---")
    st.markdown("Developed with ❤️ using Streamlit")
    st.markdown("Developer: [@asosyalarsivdev](https://t.me/asosyalarsivdev)")

if __name__ == "__main__":
    main()
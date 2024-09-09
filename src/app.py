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
    
    st.title("asosyalsozluk.com Arşiv Görüntüleyici")
    st.write("Eski asosyalsozluk.com girdilerinizi görüntülemek ve keşfetmek için kullanın.")
    
    # File upload
    uploaded_file = st.file_uploader("CSV dosyası seç", type="csv")
    
    if uploaded_file is not None:
        if st.session_state.json_data is None:
            with st.spinner("Dosya işleniyor..."):
                file_path = save_uploaded_file(uploaded_file)
                if file_path:
                    json_data = process_uploaded_file(file_path)
                    if json_data:
                        st.session_state.json_data = json_data
                        st.success("Dosya başarıyla yüklendi ve işlendi!")
                    else:
                        st.error("Dosya işlenirken bir hata oluştu.")
                else:
                    st.error("Dosya kaydedilirken bir hata oluştu.")
    
    if st.session_state.json_data:
        st.download_button(
            label="JSON İndir",
            data=st.session_state.json_data,
            file_name="converted_data.json",
            mime="application/json"
        )
        
        # Tabs for different views
        tab1, tab2 = st.tabs(["Girdiler", "Veri Analizi"])
        
        with tab1:
            # Apply search and filters
            filtered_entries = run_search_filter_component(st.session_state.json_data)
            
            # Display entries
            st.header("Girdiler")
            display_entries(json.dumps(filtered_entries))
        
        with tab2:
            # Run visualization component
            run_visualization_component(st.session_state.json_data)
    
    # Footer
    st.markdown("---")
    st.markdown("Developed with ❤️ using Streamlit")

if __name__ == "__main__":
    main()
import streamlit as st
import json
from typing import List, Dict, Any
import datetime

def render_entry(entry: Dict[str, Any]):
    """Render a single blog entry."""
    st.markdown(f"## {entry['baslik']}")
    st.markdown(f"*{entry['tarih']}*")
    st.markdown(entry['entiri'])
    st.markdown(f"**Skor:** {entry['skor']}")
    if entry['silinmis']:
        st.markdown("*Bu entry silinmiş.*")
    st.markdown("---")

def sort_entries(entries: List[Dict[str, Any]], sort_by: str, ascending: bool) -> List[Dict[str, Any]]:
    """Sort entries based on the given criteria."""
    if sort_by == 'tarih':
        return sorted(entries, key=lambda x: datetime.datetime.strptime(x['tarih'], "%Y-%m-%d %H:%M:%S"), reverse=not ascending)
    elif sort_by in ['skor', 'baslik']:
        return sorted(entries, key=lambda x: x[sort_by], reverse=not ascending)
    return entries

def filter_entries(entries: List[Dict[str, Any]], search_term: str, show_deleted: bool) -> List[Dict[str, Any]]:
    """Filter entries based on search term and deletion status."""
    filtered = [e for e in entries if search_term.lower() in e['baslik'].lower() or search_term.lower() in e['entiri'].lower()]
    if not show_deleted:
        filtered = [e for e in filtered if not e['silinmis']]
    return filtered

def display_entries(json_data: str):
    """Display blog entries with sorting, filtering, and pagination."""
    entries = json.loads(json_data)
    
    st.sidebar.header("Filtrele ve Sırala")
    
    # Sorting options
    sort_by = st.sidebar.selectbox("Sıralama kriteri:", ['tarih', 'skor', 'baslik'])
    ascending = st.sidebar.checkbox("Artan sıralama", value=False)
    
    # Filtering options
    search_term = st.sidebar.text_input("Arama:")
    show_deleted = st.sidebar.checkbox("Silinmiş entry'leri göster", value=True)
    
    # Apply sorting and filtering
    sorted_entries = sort_entries(entries, sort_by, ascending)
    filtered_entries = filter_entries(sorted_entries, search_term, show_deleted)
    
    # Pagination
    entries_per_page = 10
    page_number = st.number_input("Sayfa", min_value=1, max_value=(len(filtered_entries) - 1) // entries_per_page + 1, value=1)
    start_idx = (page_number - 1) * entries_per_page
    end_idx = start_idx + entries_per_page
    
    # Display entries
    for entry in filtered_entries[start_idx:end_idx]:
        render_entry(entry)
    
    # Display pagination info
    st.write(f"Sayfa {page_number} / {(len(filtered_entries) - 1) // entries_per_page + 1}")

# Example usage
if __name__ == "__main__":
    # This is for testing purposes
    with open("sample_data.json", "r", encoding="utf-8") as f:
        sample_json_data = f.read()
    display_entries(sample_json_data)
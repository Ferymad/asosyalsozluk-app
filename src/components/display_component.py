import streamlit as st
import json
from typing import List, Dict, Any
import datetime
from datetime import datetime

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

def format_date(date_string: str) -> str:
    try:
        date = datetime.strptime(date_string, "%Y-%m-%dT%H:%M:%S.%fZ")
        return date.strftime("%d.%m.%Y %H:%M:%S")
    except ValueError:
        return date_string  # Return original string if parsing fails

def display_entries(entries: List[Dict[str, Any]]):
    """Display the filtered entries in a format similar to the image."""
    st.write(f"Number of entries received for display: {len(entries)}")  # Debug statement

    if not entries:
        st.warning("No entries found matching the current filters.")
        return

    for entry in entries:
        col1, col2 = st.columns([1, 20])
        
        with col1:
            st.write(f"↑\n[{entry['skor']}]\n↓")
        
        with col2:
            st.markdown(f"### {entry['baslik']}")
            st.write(entry['entiri'])
            st.write(f"Date: {entry['tarih']}")
            if entry['silinmis']:
                st.write("(Deleted)")
        
        st.write("---")

# Example usage
if __name__ == "__main__":
    # This is for testing purposes
    sample_entries = [
        {
            "skor": 2,
            "baslik": "asosyal sözlük yardım hattı",
            "entiri": "Some content here...",
            "tarih": "03.10.2022 14:08:09"
        }
    ]
    display_entries(sample_entries)
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

def display_entries(entries: List[Dict[str, Any]]):
    """Display the filtered entries."""
    if not entries:
        st.warning("No entries found matching the current filters.")
        return

    st.write(f"Displaying {len(entries)} entries:")

    for entry in entries:
        st.markdown(f"**{entry['baslik']}**")
        st.write(f"Score: {entry['skor']}")
        st.write(f"Date: {entry['tarih']}")
        st.write(entry['entiri'])
        if entry['silinmis']:
            st.write("(Deleted)")
        st.markdown("---")

# Example usage
if __name__ == "__main__":
    # This is for testing purposes
    with open("sample_data.json", "r", encoding="utf-8") as f:
        sample_json_data = f.read()
    display_entries(json.loads(sample_json_data))
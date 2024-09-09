import streamlit as st
import json
from typing import List, Dict, Any
from datetime import datetime

def search_entries(entries: List[Dict[str, Any]], search_term: str) -> List[Dict[str, Any]]:
    """Perform full-text search on entries."""
    if not search_term:
        return entries
    return [
        entry for entry in entries
        if search_term.lower() in entry['baslik'].lower() or search_term.lower() in entry['entiri'].lower()
    ]

def filter_by_date(entries: List[Dict[str, Any]], start_date: datetime, end_date: datetime) -> List[Dict[str, Any]]:
    """Filter entries by date range."""
    return [
        entry for entry in entries
        if start_date <= datetime.strptime(entry['tarih'], "%Y-%m-%d %H:%M:%S") <= end_date
    ]

def filter_by_score(entries: List[Dict[str, Any]], min_score: int, max_score: int) -> List[Dict[str, Any]]:
    """Filter entries by score range."""
    return [
        entry for entry in entries
        if min_score <= entry['skor'] <= max_score
    ]

def filter_deleted(entries: List[Dict[str, Any]], show_deleted: bool) -> List[Dict[str, Any]]:
    """Filter entries based on deletion status."""
    if show_deleted:
        return entries
    return [entry for entry in entries if not entry['silinmis']]

def apply_search_and_filters(entries: List[Dict[str, Any]], filters: Dict[str, Any]) -> List[Dict[str, Any]]:
    """Apply all search and filter criteria to the entries."""
    filtered_entries = entries

    filtered_entries = search_entries(filtered_entries, filters['search_term'])
    filtered_entries = filter_by_date(filtered_entries, filters['start_date'], filters['end_date'])
    filtered_entries = filter_by_score(filtered_entries, filters['min_score'], filters['max_score'])
    filtered_entries = filter_deleted(filtered_entries, filters['show_deleted'])

    return filtered_entries

def search_filter_sidebar(entries: List[Dict[str, Any]]) -> Dict[str, Any]:
    """Create sidebar UI for search and filter options."""
    st.sidebar.header("Arama ve Filtreleme")

    search_term = st.sidebar.text_input("Arama:")

    st.sidebar.subheader("Tarih Aralığı")
    min_date = min(datetime.strptime(entry['tarih'], "%Y-%m-%d %H:%M:%S") for entry in entries)
    max_date = max(datetime.strptime(entry['tarih'], "%Y-%m-%d %H:%M:%S") for entry in entries)
    start_date = st.sidebar.date_input("Başlangıç Tarihi", min_date)
    end_date = st.sidebar.date_input("Bitiş Tarihi", max_date)

    st.sidebar.subheader("Skor Aralığı")
    min_score = min(entry['skor'] for entry in entries)
    max_score = max(entry['skor'] for entry in entries)
    score_range = st.sidebar.slider("Skor Aralığı", min_score, max_score, (min_score, max_score))

    show_deleted = st.sidebar.checkbox("Silinmiş entry'leri göster", value=True)

    return {
        'search_term': search_term,
        'start_date': datetime.combine(start_date, datetime.min.time()),
        'end_date': datetime.combine(end_date, datetime.max.time()),
        'min_score': score_range[0],
        'max_score': score_range[1],
        'show_deleted': show_deleted
    }

def run_search_filter_component(json_data: str) -> List[Dict[str, Any]]:
    """Main function to run the search and filter component."""
    entries = json.loads(json_data)
    filters = search_filter_sidebar(entries)

    
    filtered_entries = apply_search_and_filters(entries, filters)
    return filtered_entries

# Example usage
if __name__ == "__main__":
    # This is for testing purposes
    with open("sample_data.json", "r", encoding="utf-8") as f:
        sample_json_data = f.read()
    filtered_entries = run_search_filter_component(sample_json_data)
    st.write(f"Filtered entries: {len(filtered_entries)}")
    st.json(filtered_entries[:5])  # Display first 5 filtered entries
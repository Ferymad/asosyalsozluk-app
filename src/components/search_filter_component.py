import streamlit as st
import json
from typing import List, Dict, Any
from dateutil import parser
from datetime import datetime, timezone

def parse_date(date_string: str) -> datetime:
    """Parse a date string into a datetime object."""
    return parser.isoparse(date_string).replace(tzinfo=timezone.utc)

def search_entries(entries: List[Dict[str, Any]], search_term: str) -> List[Dict[str, Any]]:
    """Perform full-text search on entries."""
    if not search_term:
        return entries
    
    def safe_lower(value):
        """Safely convert a value to lowercase string."""
        if value is None:
            return ""
        return str(value).lower()

    return [
        entry for entry in entries
        if search_term.lower() in safe_lower(entry.get('baslik', '')) or 
           search_term.lower() in safe_lower(entry.get('entiri', ''))
    ]

def filter_by_date(entries: List[Dict[str, Any]], start_date: datetime, end_date: datetime) -> List[Dict[str, Any]]:
    """Filter entries by date range."""
    return [
        entry for entry in entries
        if start_date <= parse_date(entry['tarih']) <= end_date
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

def search_filter_sidebar(entries: List[Dict[str, Any]]) -> Dict[str, Any]:
    """Create a sidebar for search and filter options."""
    st.sidebar.header("Search and Filter")

    search_term = st.sidebar.text_input("Search entries")

    min_date = min(parse_date(entry['tarih']) for entry in entries)
    max_date = max(parse_date(entry['tarih']) for entry in entries)

    date_range = st.sidebar.date_input(
        "Date range",
        value=(min_date.date(), max_date.date()),
        min_value=min_date.date(),
        max_value=max_date.date()
    )

    show_deleted = st.sidebar.checkbox("Show deleted entries", value=True)

    return {
        "search_term": search_term,
        "start_date": datetime.combine(date_range[0], datetime.min.time()).replace(tzinfo=timezone.utc),
        "end_date": datetime.combine(date_range[1], datetime.max.time()).replace(tzinfo=timezone.utc),
        "show_deleted": show_deleted
    }

def run_search_filter_component(entries: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
    """Run the search and filter component."""
    if not isinstance(entries, list):
        st.error("The data is not in the expected format (list of entries).")
        return []

    filters = search_filter_sidebar(entries)

    filtered_entries = search_entries(entries, filters["search_term"])
    filtered_entries = filter_by_date(filtered_entries, filters["start_date"], filters["end_date"])
    filtered_entries = filter_deleted(filtered_entries, filters["show_deleted"])

    return filtered_entries

# Example usage
if __name__ == "__main__":
    # This is for testing purposes
    with open("sample_data.json", "r", encoding="utf-8") as f:
        sample_json_data = f.read()
    filtered_entries = run_search_filter_component(sample_json_data)
    st.write(f"Filtered entries: {len(filtered_entries)}")
    st.json(filtered_entries[:5])  # Display first 5 filtered entries
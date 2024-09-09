import streamlit as st
import json
from typing import List, Dict, Any
from dateutil import parser
from datetime import datetime, timezone
from components.display_component import display_entries
from datetime import timedelta
import math

def parse_date(date_string: str) -> datetime:
    """Parse an ISO 8601 date string into a datetime object."""
    return parser.isoparse(date_string)

def search_entries(entries, query):
    query = query.lower()
    
    def safe_lower(value):
        """Safely convert a value to lowercase string."""
        if value is None:
            return ""
        return str(value).lower()

    seen_entries = set()
    filtered_entries = []
    
    for entry in entries:
        if (query in safe_lower(entry.get('baslik', '')) or 
            query in safe_lower(entry.get('entiri', ''))):
            entry_id = entry.get('id', entry.get('tarih'))  # Use a unique identifier
            if entry_id not in seen_entries:
                seen_entries.add(entry_id)
                filtered_entries.append(entry)
    
    return filtered_entries

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
    """Create a sidebar for search and filter options, setting default date range based on entries."""
    if entries:
        # Extract dates from entries and parse them
        dates = [parser.isoparse(entry['tarih']) for entry in entries if 'tarih' in entry]
        min_date = min(dates).date() if dates else datetime.now().date()
        max_date = max(dates).date() if dates else datetime.now().date()
    else:
        # Default to last year if no entries are available
        today = datetime.now().date()
        min_date = today.replace(year=today.year - 1)
        max_date = today

    st.sidebar.header("Search and Filter")

    search_term = st.sidebar.text_input("Search entries")
    date_range = st.sidebar.date_input("Date range", value=(min_date, max_date))
    show_deleted = st.sidebar.checkbox("Show deleted entries", value=False)
    entries_per_page = st.sidebar.selectbox("Entries per page", options=[10, 20, 50, 100], index=0)

    return {
        "search_term": search_term,
        "start_date": datetime.combine(date_range[0], datetime.min.time()).replace(tzinfo=timezone.utc),
        "end_date": datetime.combine(date_range[1], datetime.max.time()).replace(tzinfo=timezone.utc),
        "show_deleted": show_deleted,
        "entries_per_page": entries_per_page
    }

def run_search_filter_component(entries):
    st.subheader("Arama ve Filtreleme")
    
    filter_options = search_filter_sidebar(entries)
    search_query = filter_options["search_term"]
    entries_per_page = filter_options.get("entries_per_page", 10)
    
    if 'page' not in st.session_state:
        st.session_state.page = 1
    
    st.write(f"Total entries before filtering: {len(entries)}")
    
    def filter_entry(entry):
        entry_date = parse_date(entry['tarih'])
        date_condition = filter_options["start_date"] <= entry_date <= filter_options["end_date"]
        deleted_condition = filter_options["show_deleted"] or not entry['silinmis']
        search_condition = (not search_query or 
                            search_query.lower() in entry['baslik'].lower() or 
                            search_query.lower() in entry['entiri'].lower())
        return date_condition and deleted_condition and search_condition
    
    filtered_entries = list(filter(filter_entry, entries))
    st.write(f"Entries after filtering: {len(filtered_entries)}")
    
    if not filtered_entries:
        st.warning("No entries found matching the current filters.")
        return
    
    # After filtering entries
    total_pages = math.ceil(len(filtered_entries) / entries_per_page)
    st.session_state.page = min(st.session_state.page, total_pages)
    
    start_idx = (st.session_state.page - 1) * entries_per_page
    end_idx = start_idx + entries_per_page
    page_entries = filtered_entries[start_idx:end_idx]
    
    # Display entries
    display_entries(page_entries)
    
    # Pagination controls
    col1, col2, col3 = st.columns([1,2,1])
    with col1:
        if st.button("Previous") and st.session_state.page > 1:
            st.session_state.page -= 1
    with col2:
        st.write(f"Page {st.session_state.page} of {total_pages}")
    with col3:
        if st.button("Next") and st.session_state.page < total_pages:
            st.session_state.page += 1

# Example usage
if __name__ == "__main__":
    # This is for testing purposes
    with open("sample_data.json", "r", encoding="utf-8") as f:
        sample_json_data = f.read()
    filtered_entries = run_search_filter_component(sample_json_data)
    st.write(f"Filtered entries: {len(filtered_entries)}")
    st.json(filtered_entries[:5])  # Display first 5 filtered entries
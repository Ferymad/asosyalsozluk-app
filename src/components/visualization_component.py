import streamlit as st
import pandas as pd
import plotly.graph_objs as go
import plotly.express as px
from typing import List, Dict, Any
from collections import Counter
import nltk
from nltk.corpus import stopwords
import math
import datetime

# Download NLTK data
nltk.download('stopwords', quiet=True)

def prepare_data(entries: List[Dict[str, Any]]) -> pd.DataFrame:
    """Prepare data for visualization."""
    df = pd.DataFrame(entries)
    df['tarih'] = pd.to_datetime(df['tarih'], errors='coerce')
    
    df = df.dropna(subset=['tarih'])
    
    df['yil'] = df['tarih'].dt.year
    df['ay'] = df['tarih'].dt.month
    
    df['skor'] = pd.to_numeric(df['skor'], errors='coerce')
    
    df['baslik'] = df['baslik'].astype(str)
    df['entiri'] = df['entiri'].astype(str)
    
    return df

@st.cache_data
def yearly_entry_count_chart(df: pd.DataFrame) -> go.Figure:
    """Create a bar chart showing yearly entry counts."""
    yearly_counts = df.groupby('yil').size().reset_index(name='count')
    
    fig = px.bar(
        yearly_counts,
        x='yil',
        y='count',
        title='Yıllık Girdi Sayısı'
    )
    fig.update_layout(
        xaxis_title='Yıl',
        yaxis_title='Girdi Sayısı',
        width=600,
        height=400
    )
    return fig

def word_frequency_chart(df: pd.DataFrame) -> go.Figure:
    """Create a bar chart of most frequent words."""
    stop_words = set(stopwords.words('turkish'))
    words = ' '.join(df['entiri']).lower().split()
    word_freq = Counter(word for word in words if word not in stop_words)
    top_words = dict(word_freq.most_common(20))
    
    fig = go.Figure(go.Bar(x=list(top_words.keys()), y=list(top_words.values())))
    fig.update_layout(
        title='En Sık Kullanılan Kelimeler',
        xaxis_title='Kelime',
        yaxis_title='Frekans',
        width=600,
        height=400
    )
    
    return fig

def monthly_entry_trend_chart(df: pd.DataFrame) -> go.Figure:
    """Create a line chart showing the trend of entry counts over time (by month)."""
    monthly_counts = df.groupby(df['tarih'].dt.to_period('M')).size().reset_index(name='count')
    monthly_counts['tarih'] = monthly_counts['tarih'].dt.to_timestamp()
    
    fig = px.line(
        monthly_counts,
        x='tarih',
        y='count',
        title='Aylık Girdi Sayısı Trendi'
    )
    fig.update_layout(
        xaxis_title='Tarih',
        yaxis_title='Girdi Sayısı',
        width=600,
        height=400
    )
    return fig

def run_visualization_component(entries: List[Dict[str, Any]]):
    df = prepare_data(entries)
    
    # Sidebar with user statistics
    st.sidebar.header("User Statistics")
    
    # Calculate user statistics
    karma_points = df['skor'].sum()
    days_active = (df['tarih'].max() - df['tarih'].min()).days
    total_entries = len(df)
    
    # Display user statistics in sidebar
    st.sidebar.metric("Karma Points", f"{karma_points:,}")
    st.sidebar.metric("Days Active", days_active)
    st.sidebar.metric("Total Entries", total_entries)
    
    # Check if 'bkz' column exists before calculating total comments
    if 'bkz' in df.columns:
        total_comments = df['bkz'].notna().sum()
        st.sidebar.metric("Total Comments", total_comments)
    
    # Optional: Add a user generation or level indicator
    st.sidebar.text("2. NESIL")  # Or calculate this based on some criteria

    # Main content area
    st.header("Asosyal Sözlük Data Analysis")
    
    # Basic statistics in the main area
    st.write(f"Total Entries: {total_entries}")
    st.write(f"Date Range: {df['tarih'].min().date()} - {df['tarih'].max().date()}")

    # Visualization options
    chart_type = st.selectbox(
        "Select Chart Type",
        ["Yearly Entry Count", "Monthly Entry Trend", "Word Frequency"]
    )

    # Display the selected chart
    if chart_type == "Yearly Entry Count":
        st.subheader("Yearly Entry Count")
        with st.spinner("Loading chart..."):
            st.plotly_chart(yearly_entry_count_chart(df))
    elif chart_type == "Monthly Entry Trend":
        st.subheader("Monthly Entry Trend")
        with st.spinner("Loading chart..."):
            st.plotly_chart(monthly_entry_trend_chart(df))
    elif chart_type == "Word Frequency":
        st.subheader("Most Frequent Words")
        with st.spinner("Loading chart..."):
            st.plotly_chart(word_frequency_chart(df))

# Example usage
if __name__ == "__main__":
    # This is for testing purposes
    import json
    with open("sample_data.json", "r", encoding="utf-8") as f:
        sample_json_data = json.load(f)
    run_visualization_component(sample_json_data)
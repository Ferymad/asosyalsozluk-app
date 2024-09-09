import streamlit as st
import pandas as pd
import altair as alt
from typing import List, Dict, Any
import plotly.graph_objs as go
from collections import Counter
import nltk
from nltk.corpus import stopwords

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
def entry_frequency_chart(df: pd.DataFrame) -> go.Figure:
    """Create an interactive chart showing entry frequency over time."""
    frequency = df.groupby(['yil', 'ay']).size().reset_index(name='count')
    
    if frequency.empty:
        return go.Figure().add_annotation(text="No data available", showarrow=False)

    frequency['date'] = pd.to_datetime(frequency['yil'].astype(str) + '-' + frequency['ay'].astype(str).str.zfill(2) + '-01')

    fig = go.Figure()
    fig.add_trace(go.Scatter(x=frequency['date'], y=frequency['count'], mode='lines'))
    fig.update_layout(
        title='Zaman İçinde Girdi Sıklığı',
        xaxis_title='Tarih',
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

def run_visualization_component(df: pd.DataFrame):
    st.header("Veri Görselleştirme")
    
    st.subheader("Zaman İçinde Girdi Sıklığı")
    st.plotly_chart(entry_frequency_chart(df))
    
    st.subheader("En Sık Kullanılan Kelimeler")
    st.plotly_chart(word_frequency_chart(df))

# Example usage
if __name__ == "__main__":
    # This is for testing purposes
    with open("sample_data.json", "r", encoding="utf-8") as f:
        sample_json_data = f.read()
    run_visualization_component(sample_json_data)
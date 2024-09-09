import streamlit as st
import pandas as pd
import altair as alt
from typing import List, Dict, Any
from datetime import datetime
from wordcloud import WordCloud
import matplotlib.pyplot as plt
from collections import Counter
import nltk
from nltk.corpus import stopwords

# Download NLTK data
nltk.download('stopwords', quiet=True)

def prepare_data(entries: List[Dict[str, Any]]) -> pd.DataFrame:
    """Prepare data for visualization."""
    df = pd.DataFrame(entries)
    df['tarih'] = pd.to_datetime(df['tarih'])
    df['yil'] = df['tarih'].dt.year
    df['ay'] = df['tarih'].dt.month
    return df

@st.cache_data
def entry_frequency_chart(df: pd.DataFrame) -> alt.Chart:
    """Create an interactive chart showing entry frequency over time."""
    frequency = df.groupby(['yil', 'ay']).size().reset_index(name='count')
    
    brush = alt.selection_interval(encodings=['x'])
    
    chart = alt.Chart(frequency).mark_line().encode(
        x=alt.X('yearmmonth(yil,ay):T', title='Tarih'),
        y=alt.Y('count:Q', title='Girdi Sayısı'),
        tooltip=['yearmmonth(yil,ay):T', 'count:Q']
    ).properties(
        title='Zaman İçinde Girdi Sıklığı',
        width=600,
        height=400
    ).add_selection(brush)
    
    return chart

@st.cache_data
def score_distribution_chart(df: pd.DataFrame) -> alt.Chart:
    """Create an interactive chart showing the distribution of entry scores."""
    brush = alt.selection_interval(encodings=['x'])
    
    chart = alt.Chart(df).mark_bar().encode(
        x=alt.X('skor:Q', bin=alt.Bin(maxbins=20), title='Skor'),
        y=alt.Y('count():Q', title='Girdi Sayısı'),
        color=alt.condition(brush, alt.value('steelblue'), alt.value('lightgray')),
        tooltip=['skor:Q', 'count():Q']
    ).properties(
        title='Skor Dağılımı',
        width=600,
        height=400
    ).add_selection(brush)
    
    return chart

@st.cache_data
def top_entries_chart(df: pd.DataFrame) -> alt.Chart:
    """Create an interactive chart showing top entries by score."""
    top_entries = df.nlargest(10, 'skor')
    
    chart = alt.Chart(top_entries).mark_bar().encode(
        x=alt.X('skor:Q', title='Skor'),
        y=alt.Y('baslik:N', sort='-x', title='Başlık'),
        color=alt.Color('skor:Q', scale=alt.Scale(scheme='viridis')),
        tooltip=['baslik', 'skor', 'tarih']
    ).properties(
        title='En Yüksek Skorlu 10 Girdi',
        width=600,
        height=400
    ).interactive()
    
    return chart

@st.cache_data
def generate_wordcloud(df: pd.DataFrame) -> plt.Figure:
    """Generate a word cloud from entry content."""
    stop_words = set(stopwords.words('turkish'))
    
    # Combine all entry content
    text = ' '.join(df['entiri'].astype(str))
    
    # Generate word cloud
    wordcloud = WordCloud(width=800, height=400, background_color='white', stopwords=stop_words).generate(text)
    
    # Create matplotlib figure
    fig, ax = plt.subplots(figsize=(10, 5))
    ax.imshow(wordcloud, interpolation='bilinear')
    ax.axis('off')
    
    return fig

def run_visualization_component(json_data: str):
    """Main function to run the visualization component."""
    entries = pd.read_json(json_data)
    df = prepare_data(entries)
    
    st.header("Veri Görselleştirme")
    
    st.subheader("Zaman İçinde Girdi Sıklığı")
    freq_chart = entry_frequency_chart(df)
    st.altair_chart(freq_chart, use_container_width=True)
    
    st.subheader("Skor Dağılımı")
    score_chart = score_distribution_chart(df)
    st.altair_chart(score_chart, use_container_width=True)
    
    st.subheader("En Yüksek Skorlu 10 Girdi")
    top_chart = top_entries_chart(df)
    st.altair_chart(top_chart, use_container_width=True)
    
    st.subheader("Kelime Bulutu")
    wordcloud_fig = generate_wordcloud(df)
    st.pyplot(wordcloud_fig)
    
    # Display filtered data based on chart interactions
    st.subheader("Filtrelenmiş Veriler")
    if score_chart.selection_brush.value:
        filtered_df = df[df['skor'].between(
            score_chart.selection_brush.value[0]['skor'][0],
            score_chart.selection_brush.value[0]['skor'][1]
        )]
        st.write(filtered_df[['baslik', 'skor', 'tarih']])

# Example usage
if __name__ == "__main__":
    # This is for testing purposes
    with open("sample_data.json", "r", encoding="utf-8") as f:
        sample_json_data = f.read()
    run_visualization_component(sample_json_data)
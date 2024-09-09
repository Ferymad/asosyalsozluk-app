import streamlit as st
import pandas as pd
import altair as alt
from typing import List, Dict, Any
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
    df['tarih'] = pd.to_datetime(df['tarih'], errors='coerce')
    
    df = df.dropna(subset=['tarih'])
    
    df['yil'] = df['tarih'].dt.year
    df['ay'] = df['tarih'].dt.month
    
    df['skor'] = pd.to_numeric(df['skor'], errors='coerce')
    
    df['baslik'] = df['baslik'].astype(str)
    df['entiri'] = df['entiri'].astype(str)
    
    return df

@st.cache_data
def entry_frequency_chart(df: pd.DataFrame) -> alt.Chart:
    """Create an interactive chart showing entry frequency over time."""
    frequency = df.groupby(['yil', 'ay']).size().reset_index(name='count')
    
    if frequency.empty:
        return alt.Chart().mark_text().encode(
            text=alt.value("No data available")
        )

    frequency['date'] = pd.to_datetime(frequency['yil'].astype(str) + '-' + frequency['ay'].astype(str).str.zfill(2) + '-01')

    chart = alt.Chart(frequency).mark_line().encode(
        x=alt.X('date:T', title='Tarih'),
        y=alt.Y('count:Q', title='Girdi Sayısı'),
        tooltip=['date:T', 'count:Q']
    ).properties(
        title='Zaman İçinde Girdi Sıklığı',
        width=600,
        height=400
    ).interactive()
    
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

@st.cache_data
def entries_over_time(df: pd.DataFrame) -> alt.Chart:
    """Create a line chart showing the number of entries over time."""
    df['date'] = pd.to_datetime(df['tarih']).dt.date
    entries_count = df.groupby('date').size().reset_index(name='count')
    
    chart = alt.Chart(entries_count).mark_line().encode(
        x=alt.X('date:T', title='Tarih'),
        y=alt.Y('count:Q', title='Girdi Sayısı'),
        tooltip=['date', 'count']
    ).properties(
        title='Zaman İçinde Girdi Sayısı',
        width=600,
        height=400
    ).interactive()
    
    return chart

@st.cache_data
def top_titles_chart(df: pd.DataFrame) -> alt.Chart:
    """Create a bar chart showing the top 10 titles with the most entries."""
    top_titles = df['baslik'].value_counts().nlargest(10).reset_index()
    top_titles.columns = ['baslik', 'count']
    
    chart = alt.Chart(top_titles).mark_bar().encode(
        x=alt.X('count:Q', title='Girdi Sayısı'),
        y=alt.Y('baslik:N', sort='-x', title='Başlık'),
        tooltip=['baslik', 'count']
    ).properties(
        title='En Çok Girdi Yapılan 10 Başlık',
        width=600,
        height=400
    ).interactive()
    
    return chart

@st.cache_data
def monthly_entry_distribution(df: pd.DataFrame) -> alt.Chart:
    """Create a bar chart showing the distribution of entries by month."""
    df['month'] = pd.to_datetime(df['tarih']).dt.month
    monthly_counts = df['month'].value_counts().sort_index().reset_index()
    monthly_counts.columns = ['month', 'count']
    
    chart = alt.Chart(monthly_counts).mark_bar().encode(
        x=alt.X('month:O', title='Ay', axis=alt.Axis(labelAngle=0)),
        y=alt.Y('count:Q', title='Girdi Sayısı'),
        tooltip=['month:O', 'count:Q']
    ).properties(
        title='Aylara Göre Girdi Dağılımı',
        width=600,
        height=400
    ).interactive()
    
    return chart

def run_visualization_component(entries: List[Dict[str, Any]]):
    """Run the visualization component."""
    if not entries:
        st.warning("Görselleştirme için veri bulunamadı.")
        return

    df = pd.DataFrame(entries)

    st.header("Veri Görselleştirme")

    st.subheader("Zaman İçinde Girdi Sayısı")
    entries_over_time_chart = entries_over_time(df)
    st.altair_chart(entries_over_time_chart, use_container_width=True)

    st.subheader("En Çok Girdi Yapılan Başlıklar")
    top_titles = top_titles_chart(df)
    st.altair_chart(top_titles, use_container_width=True)

    col1, col2 = st.columns(2)

    with col1:
        st.subheader("Aylara Göre Girdi Dağılımı")
        monthly_distribution = monthly_entry_distribution(df)
        st.altair_chart(monthly_distribution, use_container_width=True)

    with col2:
        st.subheader("Yıllara Göre Girdi Sayısı")
        df['year'] = pd.to_datetime(df['tarih']).dt.year
        yearly_chart = alt.Chart(df).mark_bar().encode(
            x='year:O',
            y='count()',
        ).properties(
            title='Yıllara Göre Girdi Sayısı',
            width=300,
            height=400
        ).interactive()
        st.altair_chart(yearly_chart, use_container_width=True)

    st.subheader("Girdi Uzunluğu Dağılımı")
    df['entry_length'] = df['entiri'].str.len()
    length_chart = alt.Chart(df).mark_bar().encode(
        x=alt.X('entry_length:Q', bin=True, title='Girdi Uzunluğu'),
        y='count()',
    ).properties(
        title='Girdi Uzunluğu Dağılımı',
        width=600,
        height=400
    ).interactive()
    st.altair_chart(length_chart, use_container_width=True)

    st.subheader("Kelime Bulutu")
    wordcloud_fig = generate_wordcloud(df)
    st.pyplot(wordcloud_fig)

# Example usage
if __name__ == "__main__":
    # This is for testing purposes
    with open("sample_data.json", "r", encoding="utf-8") as f:
        sample_json_data = f.read()
    run_visualization_component(sample_json_data)
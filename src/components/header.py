import streamlit as st


def header():
    # Streamlit app configuration
    st.set_page_config(
        page_title="StratifyAI",
        page_icon="🧠",
        layout="wide",
        initial_sidebar_state="auto",
    )
    
    # App title
    st.title("StratifyAI 🧠")

    st.markdown("""
    StratifyAI is an advanced AI-powered tool that analyzes YouTube video transcripts to extract key insights and strategies. Simply provide a YouTube video URL, and StratifyAI will fetch the transcript, process it, and deliver a comprehensive analysis. Whether you're a content creator, marketer, researcher, or solopreneur looking for insights, StratifyAI helps you unlock valuable information quickly and efficiently.
    """)
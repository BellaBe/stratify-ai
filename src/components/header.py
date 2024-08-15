import streamlit as st
from PIL import Image
import base64


def get_image_as_base64(image_path):
    with open(image_path, "rb") as img_file:
        return base64.b64encode(img_file.read()).decode("utf-8")


def header():
    icon = Image.open("assets/favicon.ico")
    st.set_page_config(
        page_title="StratifyAI",
        page_icon=icon,
        layout="wide",
        initial_sidebar_state="auto",
    )

    image_base64 = get_image_as_base64("assets/logo.svg")
    st.markdown(
        f"""
            <div style="display: flex; flex-flow: row nowrap; align-items: center; justify-content: flex-start;">
                <div style="flex: 0 1 auto;">
                    <h1 style="font-size: 2em; font-weight: bold; margin: 0;">StratifyAI</h1>
                </div>
                <div style="flex: 0 0 auto; margin-left: -20px;">
                    <img src="data:image/svg+xml;base64,{image_base64}" alt="StratifyAI Logo" style="width: 50px; height: auto;">
                </div>
            </div>
        """,
        unsafe_allow_html=True
    )

    st.markdown("""
    StratifyAI is an advanced AI-powered tool that analyzes YouTube video transcripts to extract key insights and strategies. Simply provide a YouTube video URL, and StratifyAI will fetch the transcript, process it, and deliver a comprehensive analysis. Whether you're a content creator, marketer, researcher, or solopreneur looking for insights, StratifyAI helps you unlock valuable information quickly and efficiently.
    """)

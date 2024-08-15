import streamlit as st
import re
import requests as rq
import xml.etree.ElementTree as ET
from urllib.parse import urlparse, parse_qs
from src.graph.chains.strategy_generator import StrategyGeneratorChain

URL_VIDEO_LIST_FORMAT = 'https://www.youtube.com/watch?v=&list={}'
URL_TRANSCRIPT_FORMAT = 'https://youtubetranscript.com/?server_vid2={}'


def count_tokens_simple(text):
    pattern = r'\b\w+\b|[^\w\s]'
    tokens = re.findall(pattern, text)
    return len(tokens)


def extract_video_id(url):
    st.session_state.video_url = url
    try:
        parsed_url = urlparse(url)
        if parsed_url.hostname not in ['www.youtube.com', 'youtube.com', 'm.youtube.com', 'youtu.be']:
            return None
        if parsed_url.hostname in ['www.youtube.com', 'youtube.com', 'm.youtube.com']:
            video_id = parse_qs(parsed_url.query).get('v')
            if video_id:
                return video_id[0]
        if parsed_url.hostname == 'youtu.be':
            video_id = parsed_url.path[1:]
            return video_id
    except Exception as e:
        print(f"Error parsing URL: {e}")
        return None
    return None


def get_transcript(video_id):
    transcript_url = URL_TRANSCRIPT_FORMAT.format(video_id)
    response = rq.get(transcript_url)
    xml_data = response.text
    root = ET.fromstring(xml_data)
    transcript = ' '.join([text.text for text in root.findall('.//text')])
    st.session_state.transcript = transcript
    return transcript


def handle_analyze_video():
    video_id = extract_video_id(st.session_state.video_url)
    transcript = get_transcript(video_id)
    num_tokens = count_tokens_simple(transcript)
    st.session_state.num_tokens = num_tokens
    st.session_state.video_id = video_id
    chain = StrategyGeneratorChain(
        st.session_state.loaded_model_values[3], st.session_state.loaded_model_values[1])
    analysis = chain.invoke({"transcript": transcript})
    st.session_state.analysis = analysis


def video():
    with st.form(key="video_url_form", clear_on_submit=True):
        st.text_input("Enter YouTube Video URL",
                      disabled=not st.session_state.model_set, key="video_url")
        st.form_submit_button(
            "Analyze Video", on_click=handle_analyze_video, disabled=not st.session_state.model_set)



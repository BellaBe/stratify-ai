import streamlit as st
from dotenv import load_dotenv
import re
import requests as rq
import xml.etree.ElementTree as ET
from urllib.parse import urlparse, parse_qs
from graph.chains.strategy_generator import StrategyGeneratorChain

load_dotenv()

URL_VIDEO_LIST_FORMAT = 'https://www.youtube.com/watch?v=&list={}'
URL_TRANSCRIPT_FORMAT = 'https://youtubetranscript.com/?server_vid2={}'


def extract_video_id(url):
    """
    Extracts the video ID from a YouTube URL.

    Parameters:
    url (str): The YouTube URL.

    Returns:
    str: The sanitized video ID or None if no valid ID is found.
    """
    try:
        # Parse the URL
        parsed_url = urlparse(url)
        
        # Check if the URL is a valid YouTube URL
        if parsed_url.hostname not in ['www.youtube.com', 'youtube.com', 'm.youtube.com', 'youtu.be']:
            return None
        
        # Extract the video ID from query parameters
        if parsed_url.hostname in ['www.youtube.com', 'youtube.com', 'm.youtube.com']:
            video_id = parse_qs(parsed_url.query).get('v')
            if video_id:
                return video_id[0]

        # Extract the video ID from path (for youtu.be short URLs)
        if parsed_url.hostname == 'youtu.be':
            video_id = parsed_url.path[1:]  # Remove the leading '/'
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
    return ' '.join([text.text for text in root.findall('.//text')])


def handle_submit_model():
    st.session_state.model_set = True
    st.session_state.loaded_model_values = (
        st.session_state.llm_name, st.session_state.api_key)
    
def handle_analyze_video():
    video_id = extract_video_id(st.session_state.video_url)
    transcript = get_transcript(video_id)
    print("TRASCRIPT", transcript)
    chain = StrategyGeneratorChain()
    analysis = chain.invoke({"transcript": transcript})
    st.session_state.analysis = analysis

        
def handle_change_model():
    st.session_state.model_set = False
    st.session_state.loaded_model_values = None
    
def mask_api_key(api_key):
    if len(api_key) > 6:
        return f"{api_key[:5]}{'*' * (len(api_key) - 35)}{api_key[-4:]}"
    else:
        return api_key


st.set_page_config(
    page_title="StratifyAI",
    page_icon="🧠",
    layout="centered",
    initial_sidebar_state="auto",
)


# App title
st.title("StratifyAI")

# Initialize session state variables
if "model_set" not in st.session_state:
    st.session_state.model_set = False

if "llm_name" not in st.session_state:
    # Set default value that exists in the selectbox options
    st.session_state.llm_name = "OpenAI GPT-3.5 Turbo"

if "api_key" not in st.session_state:
    st.session_state.api_key = ""

if "video_url" not in st.session_state:
    st.session_state.video_url = ""
    
if "analysis" not in st.session_state:
    st.session_state.analysis = None
    
# Model form (only one form for setting the model and API key)
if not st.session_state.model_set:
    with st.form(key='model_form'):
        col1, col2, col3 = st.columns(
            3, gap="medium", vertical_alignment="bottom")
        with col1:
            st.selectbox("Select LLM provider and model type", [
                         "OpenAI GPT-3.5 Turbo", "Groq LLaMA3 70b", "Groq Mixtral 8x7b"], key="llm_name")
        with col2:
            st.text_input("API Key", type="password",
                          placeholder="Ex: sk-2t... or gsk_mc12...", key="api_key")
        with col3:
            st.form_submit_button('Set model', on_click=handle_submit_model)
            
# Display model details and allow changing the model
else:
    with st.expander("Model details"):
        st.text(f"Model name: {st.session_state.loaded_model_values[0]}")
        st.text(
            f"API key: {mask_api_key(st.session_state.loaded_model_values[1])}")
        if st.button("Change Model", on_click=handle_change_model):
            st.success("Model settings cleared. Please set the model again.")
            

with st.form(key="video_url_form"):
    video_url = st.text_input("Enter YouTube Video URL", key="video_url")
    st.form_submit_button("Analyse Video", on_click=handle_analyze_video)

if st.session_state.analysis:
    st.write(st.session_state.analysis)

# # Buy Me a Coffee button
# st.markdown(
#     """
#     <a href="https://www.buymeacoffee.com/yourpage" target="_blank">
#         <button style="background-color:#FFDD00; border:none; color:black; padding:10px 20px; text-align:center; text-decoration:none; display:inline-block; font-size:16px; margin:4px 2px; cursor:pointer;">Buy Me a Coffee</button>
#     </a>
#     """,
#     unsafe_allow_html=True
# )

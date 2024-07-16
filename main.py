import streamlit as st
from dotenv import load_dotenv
import re
import json
import requests as rq
import xml.etree.ElementTree as ET
from urllib.parse import urlparse, parse_qs
from graph.chains.strategy_generator import StrategyGeneratorChain

# Load environment variables
load_dotenv()

# Constants for URL formats
URL_VIDEO_LIST_FORMAT = 'https://www.youtube.com/watch?v=&list={}'
URL_TRANSCRIPT_FORMAT = 'https://youtubetranscript.com/?server_vid2={}'

# Helper function to count tokens in text
def count_tokens_simple(text):
    pattern = r'\b\w+\b|[^\w\s]'
    tokens = re.findall(pattern, text)
    return len(tokens)

# Cache the model data loading for efficiency
@st.cache_data
def load_models_data(file_path):
    with open(file_path, 'r') as file:
        data = json.load(file)["models"]
        for model in data:
            model_display_name = model["name"].replace("-", " ").capitalize()
            if "gpt" in model["name"]:
                model_display_name = f"OpenAI {model_display_name}"
            else:
                model_display_name = f"Groq {model_display_name}"
            model["display_name"] = model_display_name 
    print("Data loaded", data)
    return data

# Helper function to extract video ID from a YouTube URL
def extract_video_id(url):
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

# Helper function to get transcript from a YouTube video ID
def get_transcript(video_id):
    transcript_url = URL_TRANSCRIPT_FORMAT.format(video_id)
    response = rq.get(transcript_url)
    xml_data = response.text
    root = ET.fromstring(xml_data)
    return ' '.join([text.text for text in root.findall('.//text')])

# Handle form submission to set model
def handle_submit_model():
    st.session_state.model_set = True
    for model in model_options:
        if model["display_name"] == st.session_state.llm_name:
            st.session_state.loaded_model_values = (model["display_name"], st.session_state.api_key, model["context_length"], model["name"])
            break

# Handle video analysis
def handle_analyze_video():
    video_id = extract_video_id(st.session_state.video_url)
    transcript = get_transcript(video_id)
    num_tokens = count_tokens_simple(transcript)
    st.session_state.num_tokens = num_tokens
    chain = StrategyGeneratorChain(st.session_state.loaded_model_values[3], st.session_state.loaded_model_values[1])
    analysis = chain.invoke({"transcript": transcript})
    st.session_state.analysis = analysis

# Handle model change/reset
def handle_change_model():
    st.session_state.model_set = False
    st.session_state.loaded_model_values = None

# Helper function to mask API key for display
def mask_api_key(api_key):
    if len(api_key) > 6:
        return f"{api_key[:5]}{'*' * (len(api_key) - 35)}{api_key[-4:]}"
    else:
        return api_key

# Streamlit app configuration
st.set_page_config(
    page_title="StratifyAI",
    page_icon="🧠",
    layout="wide",
    initial_sidebar_state="auto",
)

# App title
st.title("StratifyAI 🧠")

# Initialize session state variables
if "model_set" not in st.session_state:
    st.session_state.model_set = False

if "llm_name" not in st.session_state:
    st.session_state.llm_name = None

if "api_key" not in st.session_state:
    st.session_state.api_key = ""

if "video_url" not in st.session_state:
    st.session_state.video_url = ""

if "analysis" not in st.session_state:
    st.session_state.analysis = None

if "num_tokens" not in st.session_state:
    st.session_state.num_tokens = None

if "context_length" not in st.session_state:
    st.session_state.context_length = ""

# Load model options
model_options = load_models_data("data/models.json")
model_options_names = [model_option["display_name"] for model_option in model_options]

# Sidebar for model and API key input
with st.sidebar:
    st.header("Model Selection")
    if not st.session_state.model_set:
        with st.form(key='model_form', border=False):
            st.selectbox("Select LLM provider and model type", model_options_names, key="llm_name")
            st.text_input("API Key", type="password",
                          placeholder="Ex: sk-2t... or gsk_mc12...", key="api_key")
            st.form_submit_button('Set model', on_click=handle_submit_model)
    else:
        st.text(f"Model name: {st.session_state.loaded_model_values[0]}")
        st.text(f"Context length: {st.session_state.loaded_model_values[2]}")
        st.text(f"API key: {mask_api_key(st.session_state.loaded_model_values[1])}")
        if st.button("Reset Model", on_click=handle_change_model):
            st.success("Model settings cleared. Please set the model again.")

# Main content tabs
tab1, tabs2 = st.tabs(["Video Analysis", "Models overview"])

# Video Analysis tab
with tab1:
    with st.form(key="video_url_form"):
        st.text_input("Enter YouTube Video URL", key="video_url")
        st.form_submit_button("Analyze Video", on_click=handle_analyze_video)

    if st.session_state.analysis:
        if st.session_state.num_tokens:
            st.write(f"Number of tokens in the transcript: {st.session_state.num_tokens}")
        st.write(st.session_state.analysis)

# Models overview tab
with tabs2:
    st.dataframe(model_options)

# Buy Me a Coffee button (commented out)

# st.markdown(
#     """
#     <a href="https://www.buymeacoffee.com/yourpage" target="_blank">
#         <button style="background-color:#FFDD00; border:none; color:black; padding:10px 20px; text-align:center; text-decoration:none; display:inline-block; font-size:16px; margin:4px 2px; cursor:pointer;">Buy Me a Coffee</button>
#     </a>
#     """,
#     unsafe_allow_html=True
# )
import streamlit as st
import re
import json
import requests as rq
import xml.etree.ElementTree as ET
from urllib.parse import urlparse, parse_qs
from src.graph.chains.strategy_generator import StrategyGeneratorChain
from src.components.about import about
from src.components.header import header
from src.components.model import model
from src.components.use_cases import use_cases
from src.components.support import support

URL_VIDEO_LIST_FORMAT = 'https://www.youtube.com/watch?v=&list={}'
URL_TRANSCRIPT_FORMAT = 'https://youtubetranscript.com/?server_vid2={}'


def count_tokens_simple(text):
    pattern = r'\b\w+\b|[^\w\s]'
    tokens = re.findall(pattern, text)
    return len(tokens)

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
    return data


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


def get_transcript(video_id):
    transcript_url = URL_TRANSCRIPT_FORMAT.format(video_id)
    response = rq.get(transcript_url)
    xml_data = response.text
    root = ET.fromstring(xml_data)
    return ' '.join([text.text for text in root.findall('.//text')])


def handle_analyze_video():
    video_id = extract_video_id(st.session_state.video_url)
    transcript = get_transcript(video_id)
    num_tokens = count_tokens_simple(transcript)
    st.session_state.num_tokens = num_tokens
    chain = StrategyGeneratorChain(
        st.session_state.loaded_model_values[3], st.session_state.loaded_model_values[1])
    analysis = chain.invoke({"transcript": transcript})
    st.session_state.analysis = analysis
    st.session_state.thumb_feedback = None

header()

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

if "thumb_feedback" not in st.session_state:
    st.session_state.thumb_feedback = None

# Load model options
model_options = load_models_data("data/models.json")
model_options_names = [model_option["display_name"]
                       for model_option in model_options]

# sidebar(model_options, model_options_names)

model_menu_item = "Reset Model" if st.session_state.model_set else "Set Model"

# Main content tabs
tab1, tab2, tab3, tab4, tab5 = st.tabs(["Analyze", model_menu_item, "Use Cases & Benefits",  "About", "Support"])

# Video Analysis tab
with tab1:
    if not st.session_state.model_set:
        st.success("☝️ Please set the model to start analyzing videos")

    with st.form(key="video_url_form"):
        st.text_input("Enter YouTube Video URL",
                      disabled=not st.session_state.model_set, key="video_url")
        st.form_submit_button(
            "Analyze Video", on_click=handle_analyze_video, disabled=not st.session_state.model_set)

    if st.session_state.analysis:
        if st.session_state.num_tokens:
            st.write(
                f"Number of tokens in the transcript: {st.session_state.num_tokens}")

        # Add feedback text and thumbs up and thumbs down buttons
        st.write("Tell us if you liked the generated analysis:")
        col1, col2, col3= st.columns([1, 1, 1])
        with col1:
            if st.button("👍"):
                st.session_state.thumb_feedback = "up"
                st.success("Thank you for your feedback!")
        with col2:
            if st.button("👎"):
                st.session_state.thumb_feedback = "down"
                st.success("Thank you for your feedback!")
        with col3:
            st.download_button(
            label="Download Analysis",
            data=st.session_state.analysis,
            file_name='analysis.txt',
            mime='text/plain',
        )

        # Display analysis
        st.write(st.session_state.analysis)
        
with tab2:
    model(model_options, model_options_names)

with tab3:
    use_cases()

with tab4:
    about()
    
with tab5:
    support()
    


# Buy Me a Coffee button (commented out)

# st.markdown(
#     """
#     <a href="https://www.buymeacoffee.com/yourpage" target="_blank">
#         <button style="background-color:#FFDD00; border:none; color:black; padding:10px 20px; text-align:center; text-decoration:none; display:inline-block; font-size:16px; margin:4px 2px; cursor:pointer;">Buy Me a Coffee</button>
#     </a>
#     """,
#     unsafe_allow_html=True
# )

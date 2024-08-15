import streamlit as st
import json
# import urllib.parse

from src.components.about import about
from src.components.header import header
from src.components.model import model
from src.components.use_cases import use_cases
from src.components.support import support
from src.components.video import video


@st.cache_data
def load_models_data(file_path):
    with open(file_path, 'r') as file:
        data = json.load(file)["models"]
        for llm in data:
            model_display_name = llm["name"].replace("-", " ").capitalize()
            if "gpt" in llm["name"]:
                model_display_name = f"OpenAI {model_display_name}"
            else:
                model_display_name = f"Groq {model_display_name}"
            llm["display_name"] = model_display_name
    return data


header()

# Initialize session state variables
if "model_set" not in st.session_state:
    st.session_state.model_set = False

if "llm_name" not in st.session_state:
    st.session_state.llm_name = None

if "api_key" not in st.session_state:
    st.session_state.api_key = None

if "video_url" not in st.session_state:
    st.session_state.video_url = None

if "analysis" not in st.session_state:
    st.session_state.analysis = None

if "num_tokens" not in st.session_state:
    st.session_state.num_tokens = None

if "context_length" not in st.session_state:
    st.session_state.context_length = ""

if "transcript" not in st.session_state:
    st.session_state.transcript = None

if "video_id" not in st.session_state:
    st.session_state.video_id = None

# Load model options
model_options = load_models_data("data/models.json")
model_options_names = [model_option["display_name"]
                       for model_option in model_options]

# sidebar(model_options, model_options_names)

model_menu_item = "**Reset Model** 🔄" if st.session_state.model_set else "**Set Model** 🔄"

# Main content tabs
tab1, tab2, tab3, tab4, tab5 = st.tabs(
    ["**Analyze Video** 🔍", model_menu_item, "**Use cases & Benefits** 🎯",  "**About & Feedback** 📝", "**Support Us** :pray:"])

# Video Analysis tab
with tab1:
    if not st.session_state.model_set:
        st.success("☝️ Please set the model to start analyzing videos")

    video()

    if st.session_state.analysis:
        st.markdown(
            "<div style='display: flex; justify-content: start; gap: 20px; margin: 40px 0'>"
            "<div style='font-weight: bold'>Analysis concluded 🪄</div>"
            "<div>Video URL: <span style='font-weight: bold'>{}</span></div>"
            "<div>Approx Number of Tokens: <span style='font-weight: bold'>{}</span></div>"
            "</div>".format(
                st.session_state.video_url, st.session_state.num_tokens),
            unsafe_allow_html=True
        )

        int_tab1, int_tab2 = st.tabs(
            ["AI Generated Strategy", "Video Transcript"])

        with int_tab1:
            # encoded_analysis = urllib.parse.quote(st.session_state.analysis)

            # card_html = f"""
            # <div style='background-color: #f9f9f9; padding: 20px; border-radius: 10px; display: flex; align-items: start; justify-content: space-between;'>
            #     <div style='flex-grow: 1;'>
            #         {st.session_state.analysis}
            #     </div>
            #     <div style='margin-left: 20px;'>
            #         <a href="data:text/plain;charset=utf-8,{encoded_analysis}" download="analysis_{st.session_state.video_id}.txt" style='background-color: #4CAF50; color: white; padding: 10px 20px; text-align: center; text-decoration: none; display: inline-block; border-radius: 5px;'>
            #             Download
            #         </a>
            #     </div>
            # </div>
            # """
            # st.markdown(card_html, unsafe_allow_html=True)

            st.download_button(
                label="Download Analysis",
                data=st.session_state.analysis,
                file_name=f'analysis_{st.session_state.video_id}.txt',
                mime='text/plain',
            )

            st.write(st.session_state.analysis)

        with int_tab2:
            st.download_button(
                label="Download Transcript",
                data=st.session_state.transcript,
                file_name=f'transcript_{st.session_state.video_id}.txt',
                mime='text/plain',
            )
            st.write(st.session_state.transcript)

with tab2:
    model(model_options, model_options_names)

with tab3:
    use_cases()

with tab4:
    about()

with tab5:
    support()

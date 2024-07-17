import streamlit as st

def mask_api_key(api_key):
    if len(api_key) > 6:
        return f"{api_key[:5]}{'*' * (len(api_key) - 35)}{api_key[-4:]}"
    else:
        return api_key

def handle_change_model():
    st.session_state.model_set = False
    st.session_state.loaded_model_values = None
    
def handle_submit_model(model_options):
    st.session_state.model_set = True
    for model in model_options:
        if model["display_name"] == st.session_state.llm_name:
            st.session_state.loaded_model_values = (
                model["display_name"], st.session_state.api_key, model["context_length"], model["name"])
            break

def model(model_options, model_options_names):
        if not st.session_state.model_set:
            with st.form(key='model_form', border=False):
                st.selectbox("Select LLM provider and model type",
                            model_options_names, key="llm_name")
                st.text_input("API Key", type="password",
                            placeholder="Ex: sk-2t... or gsk_mc12...", key="api_key")
                st.form_submit_button('Set model', on_click=lambda: handle_submit_model(model_options))

            st.markdown(
                "If you need help to get an API key, for OpenAI models [click here](https://platform.openai.com/api-keys), for Groq models [click here](https://console.groq.com/keys)")
        else:
            st.header("Model Settings")
            st.text(f"Model name: {st.session_state.loaded_model_values[0]}")
            st.text(f"Context length: {st.session_state.loaded_model_values[2]}")
            st.text(
                f"API key: {mask_api_key(st.session_state.loaded_model_values[1])}")
            if st.button("Reset Model", on_click=handle_change_model):
                st.success("Model settings cleared. Please set the model again.")
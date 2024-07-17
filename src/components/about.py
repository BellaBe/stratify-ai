import streamlit as st

@st.cache_resource
def about():
    return st.markdown("""
        #### **Welcome to StratifyAI!**  
        
        StratifyAI is a cutting-edge software company dedicated to revolutionizing how businesses, educators, and individuals extract valuable insights from YouTube video content. Our flagship product leverages advanced AI technology to analyze video transcripts, identifying and extracting actionable strategies for various purposes.

        #### 🎯 **Our Mission**
        To empower users by transforming video content into clear, actionable strategies, enhancing decision-making, improving efficiency, and driving success.

        #### 🚀 **What StratifyAI Can Do for You**
        StratifyAI’s YouTube Video Strategy Extractor helps you by:
        - **Analyzing Video Transcripts:** Efficiently processing transcripts to identify strategic content, saving you hours of manual review.
        - **Generating Actionable Insights:** Converting detected strategies into clear, implementable steps.
        - **Automating Content Review:** Reducing manual effort and allowing you to focus on applying the insights gained.

    """
    )

import streamlit as st

def use_cases(): 
    col1, col2 = st.columns([1, 1])
    with col1:
        container = st.container(border=True)
        container.write("**Competitive Analysis:**")
        container.write("Extract and implement successful strategies from competitor videos to stay ahead in the market.")
    with col2:
        container = st.container(border=True)
        container.write("**Gain a competitive edge**")
        container.write("Leverage insights from industry leaders..")
    
    with col1:
        container = st.container(border=True)
        container.write("**Educational Improvement:**")
        container.write("Adopt effective teaching methods from successful educational videos to enhance instructional techniques.")
    with col2:
        container = st.container(border=True)
        container.write("**Improve teaching efficacy**")
        container.write("Get better student outcomes with proven strategies.")
        
    with col1:
        container = st.container(border=True)
        container.write("**Personal Development:**")
        container.write("Enhance skills and knowledge by applying strategies from various tutorial and instructional videos.")
    with col2:
        container = st.container(border=True)
        container.write("**Accelerate personal growth**")
        container.write("Develop skills and knowledge with actionable insights.")
   
    with col1:
        container = st.container(border=True)
        container.write("**Marketing Strategies:**")
        container.write("Analyze successful campaigns and strategies from industry influencers and competitors.")
    with col2:
        container = st.container(border=True)
        container.write("**Optimize marketing efforts**")
        container.write("Apply proven tactics and ideas to improve marketing.")
        
    with col1:
        container = st.container(border=True)
        container.write("**Research and Development:**")
        container.write("Extract methodologies and insights from expert presentations and educational content.")
    with col2:
        container = st.container(border=True)
        container.write("**Enhance research quality**")
        container.write("Integrate advanced strategies and techniques for innovation.")
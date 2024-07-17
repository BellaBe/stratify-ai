import streamlit as st

def support():
    st.header("Support Us")
    st.write("If you find our tool useful and would like to support further development, consider making a donation.")
    st.markdown("""
    <a href="https://donate.stripe.com/9AQeXqfdv3eD0qA3ce" target="_blank">
        <button style="background-color:#6772e5; border:none; color:white; padding:10px 20px; text-align:center; text-decoration:none; display:inline-block; font-size:16px; margin:4px 2px; cursor:pointer;">Donate via Stripe</button>
    </a>
    """, unsafe_allow_html=True)
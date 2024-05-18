from openai import OpenAI
import streamlit as st

st.set_page_config(
    page_title=f"Home",
    page_icon="👋",
    initial_sidebar_state="expanded",
)

st.title("Home")
st.subheader("Welcome to the Streamlit Chatbot!")
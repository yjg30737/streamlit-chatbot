from openai import OpenAI
import streamlit as st

# Set OpenAI API key from Streamlit secrets
CLIENT = OpenAI(api_key=st.secrets['OPENAI_API_KEY'])
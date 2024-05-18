from openai import OpenAI
import streamlit as st

# Set OpenAI API key from Streamlit secrets
CLIENT = OpenAI(api_key=st.secrets['OPENAI_API_KEY'])

TEXT_MODEL = ['gpt-4o', 'gpt-4-turbo', 'gpt-3.5-turbo']
DALLE_SIZE = ['256x256', '512x512', '1024x1024', '1024x1792', '1792x1024']
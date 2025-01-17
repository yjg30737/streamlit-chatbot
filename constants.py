import datetime
from openai import OpenAI, AssistantEventHandler
import streamlit as st

# Set OpenAI API key from Streamlit secrets
CLIENT = OpenAI(api_key=st.secrets['OPENAI_API_KEY'])

TEXT_MODEL = ['gpt-4o', 'gpt-4o-mini']
DALLE_SIZE = ['1024x1024', '1024x1792', '1792x1024']

def get_message_obj(role, content):
    return {"role": role, "content": content}
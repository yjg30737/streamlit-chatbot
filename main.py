from openai import OpenAI
import streamlit as st
from st_supabase_connection import SupabaseConnection
# More info:
# https://pypi.org/project/st-supabase-connection/

st.set_page_config(
    page_title=f"Home",
    page_icon="👋",
    initial_sidebar_state="expanded",
)


from openai import OpenAI
import streamlit as st
from st_supabase_connection import SupabaseConnection
from widget import chat_model_widget, init_chat, get_chat_history, process_chat
# More info:
# https://pypi.org/project/st-supabase-connection/

st.set_page_config(
    page_title=f"yjg30737's Streamlit Chatbot",
    page_icon="👋",
    initial_sidebar_state="expanded",
)

# Initialize connection.
conn = st.connection('supabase', type=SupabaseConnection)

# Login to Supabase.
# conn.auth.sign_in_with_password(dict(email=st.secrets['SUPABASE_USER_EMAIL'], password='this_password_is_insecure_and_should_be_updated'))

# Perform query.
rows = conn.query('*', table='mytable', ttl='10m').execute()

# Print results.
for row in rows.data:
    st.write(f"{row['name']} has a:{row['pet']}:")

model = chat_model_widget()

# init_chat

client = init_chat()
get_chat_history(conn)
process_chat(conn)
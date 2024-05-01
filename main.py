from openai import OpenAI
import streamlit as st
from st_supabase_connection import SupabaseConnection
# More info:
# https://pypi.org/project/st-supabase-connection/

st.set_page_config(
    page_title=f"yjg30737's Streamlit Chatbot",
    page_icon="👋",
    initial_sidebar_state="expanded",
)

# Initialize connection.
conn = st.connection('supabase', type=SupabaseConnection)

# Perform query.
rows = conn.query('*', table='mytable', ttl='10m').execute()

# Print results.
for row in rows.data:
    st.write(f"{row['name']} has a:{row['pet']}:")

st.sidebar.title("Settings")
st.session_state['openai_model'] = st.sidebar.selectbox(
    'Select a model',
    ['gpt-4-0125-preview', 'gpt-4', 'gpt-4-1106-preview', 'gpt-4-vision-preview',
     'gpt-3.5-turbo', 'gpt-3.5-turbo-16k'],
)

# Set OpenAI API key from Streamlit secrets
client = OpenAI(api_key=st.secrets['OPENAI_API_KEY'])

# Set a default model
if 'openai_model' not in st.session_state:
    st.session_state['openai_model'] = 'gpt-3.5-turbo'

# Initialize chat history
if 'messages' not in st.session_state:
    st.session_state.messages = [{'role': 'system', 'content': 'You are a helpful assistant.'}]

# Display chat messages from history on app rerun
for message in st.session_state.messages:
    with st.chat_message(message['role']):
        st.markdown(message['content'])

# React to user input
if prompt := st.chat_input('What is up?'):
    # Display user message in chat message container
    with st.chat_message('user'):
        st.markdown(prompt)
    # Add user message to chat history
    st.session_state.messages.append({'role': 'user', 'content': prompt})

    # Chatbot's response
    # Display assistant repsonse in chat message container
    with st.chat_message('assistant'):
        # OpenAI API response
        stream = client.chat.completions.create(
            model=st.session_state['openai_model'],
            messages=[
                {'role': m['role'], 'content': m['content']}
                for m in st.session_state.messages
            ],
            stream=True
        )
        response = st.write_stream(stream)
    # Add assistant response to chat history
    st.session_state.messages.append({'role': 'assistant', 'content': response})
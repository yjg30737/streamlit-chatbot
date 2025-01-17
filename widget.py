import base64
import time

import streamlit as st

from constants import CLIENT, DALLE_SIZE, TEXT_MODEL, get_message_obj


def image_settings_widget(default_obj):
    size = st.selectbox("Size", DALLE_SIZE, index=2)
    prompt = st.text_area("Prompt", default_obj["prompt"])
    negative_prompt = st.text_area("Negative Prompt", default_obj["negative_prompt"])
    button = st.button("Generate Image")
    return size, prompt, negative_prompt, button

def chat_model_widget():
    st.title("Settings")
    st.session_state['openai_model'] = st.selectbox(
        'Select a model',
        TEXT_MODEL,
    )
    return st.session_state['openai_model']


def set_sidebar(widget, *args, **kwargs):
    if not callable(widget):
        raise ValueError("The widget argument must be callable.")

    with st.sidebar:
        return widget(*args, **kwargs)

# init_chat
def init_chat():
    # Set a default model
    if 'openai_model' not in st.session_state:
        st.session_state['openai_model'] = 'gpt-3.5-turbo'

# get_chat_history
def get_chat_history(conn):
    chat_history = conn.table('chat').select('*').execute()
    if len(chat_history.data) > 0:
        st.session_state.messages = chat_history.data
    else:
        # Initialize chat history
        if 'messages' not in st.session_state:
            st.session_state.messages = [{'role': 'system', 'content': 'You are a helpful assistant.'}]

    # Display chat messages from history on app rerun
    for message in st.session_state.messages:
        with st.chat_message(message['role']):
            st.markdown(message['content'])

# process_chat
def process_chat(conn, type='chat'):
    # React to user input
    if prompt := st.chat_input('What is up?'):
        # Display user message in chat message container
        with st.chat_message('user'):
            st.markdown(prompt)
        request_obj = get_message_obj('user', prompt)
        # Add user message to chat history
        st.session_state.messages.append(request_obj)
        # Save to the db
        conn.table('chat').insert(request_obj).execute()

        # Chatbot's response
        # Display assistant response in chat message container
        with st.chat_message('assistant'):
            # OpenAI API response
            if type == 'chat':
                stream = CLIENT.chat.completions.create(
                    model=st.session_state['openai_model'],
                    messages=[
                        {'role': m['role'], 'content': m['content']}
                        for m in st.session_state.messages
                    ],
                    stream=True
                )
                response = st.write_stream(stream)
        response_obj = get_message_obj('assistant', response)
        # Add assistant response to chat history
        st.session_state.messages.append(response_obj)
        # Save to the db
        conn.table('chat').insert(response_obj).execute()

def image_result_widget(model, prompt, size):
    with st.spinner('Generating image…'):
        start_time = time.time()

        response = CLIENT.images.generate(
            model=model,
            prompt=prompt,
            n=1,
            size=size,
            response_format='b64_json',
        )
        for _ in response.data:
            image_data = _.b64_json
            image_data = base64.b64decode(image_data)
            st.image(image_data, use_column_width=True)
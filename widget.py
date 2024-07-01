import base64
import time

import streamlit as st

from constants import CLIENT, DALLE_SIZE, TEXT_MODEL, get_message_obj, send_message, EventHandler


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
def process_chat(conn, type='chat', instructions='', message_file_id=None, assistant_id=None, thread_id=None):
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
            # elif type == 'assistant':
            #     args = {
            #         'thread_id': thread_id,
            #         **request_obj
            #     }
            #
            #     if message_file_id:
            #         args['attachments'] = [
            #             {"file_id": message_file_id, "tools": [{"type": "file_search"}]}
            #         ]
            #
            #     CLIENT.beta.threads.messages.create(**args)
            #
            #     with CLIENT.beta.threads.runs.stream(
            #         thread_id=thread_id,
            #         assistant_id=assistant_id,
            #         instructions=instructions,
            #
            #     TypeError: EventHandler.__init__() takes 1 positional argument but 2 were given
            #
            #         event_handler=EventHandler(), <<< This one is the problem
            #     ) as stream:
            #
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

def assistant_widget(assistants):
    st.title("Assistant")
    # Show assistants table
    if assistants:
        st.session_state['assistant'] = st.selectbox(
            'Select an assistant',
            assistants, format_func=lambda x: x['name']
        )
    else:
        st.session_state['assistant'] = None
    return st.session_state['assistant']

def vector_store_widget(vector_stores):
    st.title("Vector Store")
    # Show vector store table
    if vector_stores:
        st.session_state['vector_store'] = st.selectbox(
            'Select a vector',
            vector_stores, format_func=lambda x: x['name']
        )
    else:
        st.session_state['vector_store'] = None
    return st.session_state['vector_store']

def file_widget(file_list):
    st.title("File")
    # Show file table
    if file_list:
        st.session_state['file'] = st.selectbox(
            'Select a file',
            file_list, format_func=lambda x: x['filename']
        )
    else:
        st.session_state['file'] = None
    return st.session_state['file']


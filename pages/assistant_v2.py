import streamlit as st
from st_supabase_connection import SupabaseConnection

from constants import get_assistants, get_vector_stores, get_vector_store_files, set_current_thread
from widget import init_chat, get_chat_history, process_chat
from widget import set_sidebar, assistant_widget, vector_store_widget, file_widget

assistants = get_assistants()

assistant = set_sidebar(assistant_widget, assistants)
if assistant:
    thread = set_current_thread(assistant['assistant_id'])
    vector_stores = get_vector_stores(assistant['assistant_id'])
    vector_store = set_sidebar(vector_store_widget, vector_stores)
    if vector_store:
        files = get_vector_store_files(vector_store['vector_store_id'])
        file = set_sidebar(file_widget, files)

        # Initialize connection.
        conn = st.connection('supabase', type=SupabaseConnection)

        client = init_chat()
        get_chat_history(conn)
        process_chat(conn, type='assistant',
                     message_file_id=file['file_id'],
                     assistant_id=assistant['assistant_id'],
                     thread_id=thread.id)
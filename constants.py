import datetime
from openai import OpenAI, AssistantEventHandler
import streamlit as st

# Set OpenAI API key from Streamlit secrets
CLIENT = OpenAI(api_key=st.secrets['OPENAI_API_KEY'])

TEXT_MODEL = ['gpt-4o', 'gpt-4-turbo', 'gpt-3.5-turbo']
DALLE_SIZE = ['256x256', '512x512', '1024x1024', '1024x1792', '1792x1024']

def timestamp_to_datetime(timestamp):
    return datetime.datetime.fromtimestamp(timestamp).strftime('%Y-%m-%d %H:%M:%S')

def get_message_obj(role, content):
    return {"role": role, "content": content}

def form_assistant_obj(assistant):
    """
    Forms a dictionary object representing an assistant.

    :param assistant: Assistant object from the API.
    :return: Dictionary representing the assistant.
    """
    obj = {
        "assistant_id": assistant.id,
        "name": assistant.name,
        "instructions": assistant.instructions,
        "tools": assistant.tools,
        "model": assistant.model,
        "created_at": timestamp_to_datetime(assistant.created_at),
    }
    return obj

def form_vectorstore_obj(vector):
    """
    Forms a dictionary object representing a vector store.

    :param vector: Vector store object from the API.
    :return: Dictionary representing the vector store.
    """
    obj = {
        "vector_store_id": vector.id,
        "name": vector.name,
        "created_at": timestamp_to_datetime(vector.created_at),
        "file_counts": vector.file_counts,
        "last_activate_at": timestamp_to_datetime(vector.last_active_at),
    }
    return obj


def form_files_obj(file):
    """
    Forms a dictionary object representing a file.

    :param file: File object from the API.
    :return: Dictionary representing the file.
    """
    obj = {
        "file_id": file.id,
        "filename": file.filename,
        "bytes": file.bytes,
        "created_at": timestamp_to_datetime(file.created_at),
    }
    return obj


def get_assistants(order='desc', limit=None):
    """
    Retrieves a list of assistants.

    :param order: Order of retrieval, either 'asc' or 'desc'.
    :param limit: Limit on the number of assistants to retrieve.
    :return: List of assistants.
    """
    if CLIENT is None:
        return None
    assistants = CLIENT.beta.assistants.list(order=order, limit=limit)
    assistants = [form_assistant_obj(assistant) for assistant in assistants]
    assistants = assistants
    return assistants


def create_assistant(args):
    """
    Creates a new assistant.

    :param args: Arguments for creating the assistant.
    :return: Dictionary representing the newly created assistant.
    """
    assistant = CLIENT.beta.assistants.create(
        **args
    )

    set_current_assistant(assistant.id)

    assistant = form_assistant_obj(assistant)

    return assistant


def set_current_assistant(assistant_id):
    """
    Sets the current assistant by ID.

    :param assistant_id: ID of the assistant to set as current.
    """
    assistant_id = assistant_id
    set_current_thread(assistant_id)


def delete_assistant(assistant_id):
    """
    Deletes an assistant by ID.

    :param assistant_id: ID of the assistant to delete.
    """
    CLIENT.beta.assistants.delete(assistant_id=assistant_id)


def set_current_thread(assistant_id, messages=None):
    """
    Sets the current thread for the assistant.

    :param messages: Optional initial messages for the thread.
    :return: Thread object.
    """
    if messages:
        thread = CLIENT.beta.threads.create(messages=messages)
    else:
        thread = CLIENT.beta.threads.create()
    thread_id = thread.id
    assistants = get_assistants()
    for assistant in assistants:
        if assistant["assistant_id"] == assistant_id:
            assistant["thread"] = thread_id
            break
    return thread


def send_message(conn,
                 message_str, instructions='', message_file=None, assistant_id=None, thread_id=None):
    """
    Sends a message to the assistant and handles streaming responses.

    :param message_str: The message content.
    :param instructions: Additional instructions for the assistant.
    :param message_file: Optional file to attach to the message.
    :param assistant_id: ID of the assistant to use.
    :param thread_id: ID of the thread to use.
    :yield: Streamed text responses.
    """
    user_obj = get_message_obj("user", message_str)
    st.session_state.messages.append(user_obj)
    conn.table('chat').insert(user_obj).execute()
    # _db_handler.append(Conversation, user_obj)

    args = {
        'thread_id': thread_id if thread_id else thread_id,
        'role': "user",
        'content': message_str
    }

    if message_file:
        args['attachments'] = [
            {"file_id": message_file.id, "tools": [{"type": "file_search"}]}
        ]

    CLIENT.beta.threads.messages.create(**args)
    # Chatbot's response (Assistant)
    # Display assistant response in chat message container
    with st.chat_message('assistant'):
        stream = CLIENT.beta.threads.runs.stream(
                thread_id=thread_id if thread_id else thread_id,
                assistant_id=assistant_id if assistant_id else assistant_id,
                instructions=instructions,
                event_handler=EventHandler(CLIENT),
        )
        response = st.write_stream(stream)
    response_obj = get_message_obj('assistant', response)
    # Add assistant response to chat history
    st.session_state.messages.append(response_obj)
    # Save to the db
    conn.table('chat').insert(response_obj).execute()


    # CLIENT.beta.threads.messages.create(**args)
    #
    # response = ''
    #
    # with CLIENT.beta.threads.runs.stream(
    #         thread_id=thread_id if thread_id else thread_id,
    #         assistant_id=assistant_id if assistant_id else assistant_id,
    #         instructions=instructions,
    #         event_handler=EventHandler(CLIENT),
    # ) as stream:
    #     for text in stream.text_deltas:
    #         response += text
    #         yield text
    #
    # ai_obj = get_message_obj("assistant", response)
    # _db_handler.append(Conversation, ai_obj)


def create_vector_store(args):
    """
    Creates a new vector store.

    :param args: Arguments for creating the vector store.
    :return: Dictionary representing the newly created vector store.
    """
    vector_store = CLIENT.beta.vector_stores.create(**args)
    vector_store = form_vectorstore_obj(vector_store)
    return vector_store


def upload_files_to_vector_store(vector_store_id, file_paths):
    """
    Uploads local files to the vector store.

    :param vector_store_id: ID of the vector store.
    :param file_paths: List of file paths to upload.
    :return: Dictionary representing the uploaded files.
    """
    file_streams = [open(path, "rb") for path in file_paths]
    file_batch = CLIENT.beta.vector_stores.file_batches.upload_and_poll(
        vector_store_id=vector_store_id, files=file_streams
    )

    result_obj = form_files_obj(file_batch)

    return result_obj


def delete_vector_store(vector_store_id):
    """
    Deletes a vector store by ID.

    :param vector_store_id: ID of the vector store to delete.
    """
    CLIENT.beta.vector_stores.delete(vector_store_id=vector_store_id)


def delete_files_from_vector_store(vector_store_id, file_id):
    """
    Deletes a file from the vector store.

    :param vector_store_id: ID of the vector store.
    :param file_id: ID of the file to delete.
    """
    CLIENT.beta.vector_stores.files.delete(vector_store_id=vector_store_id, file_id=file_id)


def update_assistant(tool_resources, assistant_id=None):
    """
    Updates an assistant's tool resources.

    :param tool_resources: Tool resources to update.
    :param assistant_id: Optional assistant ID.
    :return: Updated assistant object.
    """
    assistant = CLIENT.beta.assistants.update(
        assistant_id=assistant_id if assistant_id else assistant_id,
        tool_resources=tool_resources
    )
    return assistant


def delete_file(file_id):
    """
    Deletes a file from OpenAI files storage. It deletes the file in every vector store.

    :param file_id: ID of the file to delete.
    """
    CLIENT.files.delete(file_id=file_id)


def get_vector_stores(assistant_id=None):
    """
    Retrieves vector stores in the assistant.

    :param assistant_id: Optional assistant ID.
    :return: List of vector stores.
    """
    vs_obj_lst = []

    assistant_id = assistant_id if assistant_id else assistant_id

    tool_resources = CLIENT.beta.assistants.retrieve(assistant_id=assistant_id).dict()['tool_resources']
    if tool_resources:
        file_search = tool_resources['file_search']
        if file_search:
            vs_ids = file_search['vector_store_ids']
            for vs_id in vs_ids:
                vs_instance = CLIENT.beta.vector_stores.retrieve(vector_store_id=vs_id)
                vs_obj_lst.append(form_vectorstore_obj(vs_instance))

    return vs_obj_lst


def get_vector_store_files(vector_store_id):
    """
    Retrieves files in a vector store.

    :param vector_store_id: ID of the vector store.
    :return: List of files in the vector store.
    """
    files_lst = []

    vector_store_files = CLIENT.beta.vector_stores.files.list(vector_store_id=vector_store_id)
    for file in vector_store_files:
        file = CLIENT.files.retrieve(file_id=file.id)
        files_lst.append(form_files_obj(file))

    return files_lst


def clear_messages(self):
    """
    Clears all messages from the conversation database.
    """
    # _db_handler.delete(Conversation, None)
    pass


# Declaration as an inner class
class EventHandler(AssistantEventHandler):
    """
    Event handler class for handling assistant events.
    """

    def __init__(client):
        """
        Initializes the EventHandler.

        :param client: The client instance.
        """
        super().__init__()
        CLIENT = client

    def on_text_created(text) -> None:
        """
        Handles the event when text is created.

        :param text: The created text.
        """
        print(f"\nassistant onTextCreated > ", end="", flush=True)

    def on_text_delta(delta, snapshot):
        """
        Handles the event when there is a text delta.

        :param delta: The text delta.
        :param snapshot: The snapshot of the current state.
        """
        print(delta.value, end="", flush=True)

    def on_tool_call_created(tool_call):
        """
        Handles the event when a tool call is created.

        :param tool_call: The created tool call.
        """
        print(f"\nassistant onToolCallCreated > {tool_call.type}\n", flush=True)

    def on_tool_call_delta(delta, snapshot):
        """
        Handles the event when there is a tool call delta.

        :param delta: The tool call delta.
        :param snapshot: The snapshot of the current state.
        """
        if delta.type == 'code_interpreter':
            pass
        elif delta.type == 'file_search':
            print(f"\nassistant > {delta.type}\n", flush=True)

    def on_message_done(message) -> None:
        """
        Handles the event when a message is done.

        :param message: The completed message.
        """
        print('Message done')
        message_content = message.content[0].text
        annotations = message_content.annotations
        citations = []
        for index, annotation in enumerate(annotations):
            message_content.value = message_content.value.replace(
                annotation.text, f"[{index}]"
            )
            if file_citation := getattr(annotation, "file_citation", None):
                cited_file = CLIENT.files.retrieve(file_citation.file_id)
                citations.append(f"[{index}] {cited_file.filename}")

        print(message_content.value)
        print("\n".join(citations))
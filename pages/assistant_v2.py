from constants import get_assistants, get_vector_stores, get_vector_store_files
from widget import set_sidebar, assistant_widget, vector_store_widget, file_widget

assistants = get_assistants()

assistant = set_sidebar(assistant_widget, assistants)
if assistant:
    vector_stores = get_vector_stores(assistant['assistant_id'])
    vector_store = set_sidebar(vector_store_widget, vector_stores)
    if vector_store:
        files = get_vector_store_files(vector_store['vector_store_id'])
        file = set_sidebar(file_widget, files)

#
# set_sidebar(vector_store_widget, )
# set_sidebar(file_widget, )
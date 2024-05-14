# streamlit-chatbot
ChatGPT-like Streamlit chatbot & Simple image generator (DALLE3) OpenAI
Using supabase as database.

## Requirements
* streamlit
* openai
* st-supabase-connection

## How to Install
1. git clone ~
2. pip install -r requirements.txt
3. streamlit hello
4. Make .streamlit directory and put secrets.toml into it and copy below:
```toml
# .streamlit/secrets.toml
OPENAI_API_KEY=

[connections.supabase]
SUPABASE_URL = 
SUPABASE_KEY = 
```
5. streamlit run main.py

## Documentation
It is good practice to read following docs and articles to know the basic of using and making streamlit app.

These help me a lot to develop streamlit application.

### For this application
* <a href="https://docs.streamlit.io/get-started">Get Started</a>
* <a href="https://docs.streamlit.io/develop/tutorials/databases/supabase">Connect Streamlit to Supabase</a>

### For making Streamlit application
* <a href="https://docs.streamlit.io/develop/api-reference">API Reference (Elements and widgets)</a>
* <a href="https://docs.streamlit.io/develop/api-reference/connections/secrets.toml">Make and manage "secrets.toml" file for configuration</a>

### For making your chatbot and your image generator
* <a href="https://docs.streamlit.io/develop/tutorials/llms/build-conversational-apps">Build a basic LLM chat app</a>
* <a href="https://medium.com/@arjunaraneta/creating-an-image-generator-with-streamlit-and-replicate-api-hint-its-pretty-easy-a995ff3d1d0a">Creating an image generator with streamlit and replicate api by arjunaraneta</a> 

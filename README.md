# streamlit-chatbot
[![](https://dcbadge.vercel.app/api/server/cHekprskVE)](https://discord.gg/cHekprskVE)

ChatGPT-like Streamlit chatbot & Simple image generator (DALLE3) OpenAI
Using supabase as database.

## Requirements
* streamlit
* openai
* st-supabase-connection

## How to Install
Type below:

```
>>> git clone [THE_REPO_URL]
>>> pip install -r requirements.txt
>>> streamlit hello
```

Then, make .streamlit directory and put secrets.toml into it and copy below:

```toml
# .streamlit/secrets.toml
OPENAI_API_KEY=

[connections.supabase]
SUPABASE_URL = 
SUPABASE_KEY = 
```

Finally, type `streamlit run main.py` to show the result. Browser will pop up and you can play it.

## Preview
https://youtu.be/8pHC8mKl3VI

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

## Troubleshooting
If this error shows:

```
httpcore.ConnectError: [Errno 11001] getaddrinfo failed
```

That means you need to restore your database. Go to the supabase dashboard to restore it, then it will work like a charm as usual!

If you don't use Supabase a couple of days, you can't connect with it because it suspends the project. Of course, if you are using the Supabase in free, as i am.

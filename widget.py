import streamlit as st

def widget(default_obj):
    size = st.selectbox("Size", ['256x256', '512x512', '1024x1024', '1024x1792', '1792x1024'], index=2)
    prompt = st.text_area("Prompt", default_obj["prompt"])
    negative_prompt = st.text_area("Negative Prompt", default_obj["negative_prompt"])
    button = st.button("Generate Image")
    return size, prompt, negative_prompt, button
import streamlit as st
from widget import image_settings_widget, image_result_widget, set_sidebar

st.set_page_config(
    page_title=f"yjg30737's Streamlit Image Generator",
    page_icon="👋",
    initial_sidebar_state="expanded",
)

st.title("Image Generator")

model = 'dall-e-3'

default_obj = {
    'size': '1024x1024',
    "prompt": "Astronaut in a jungle, cold color palette, muted colors, detailed, 8k",
    "negative_prompt": "ugly, deformed, noisy, blurry, distorted"
}

size, prompt, negative_prompt, button = set_sidebar(image_settings_widget, default_obj)
if button:
    image_result_widget(model, prompt, size)
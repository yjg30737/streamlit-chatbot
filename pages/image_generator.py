import streamlit as st
from openai import OpenAI
import time
import base64
from widget import widget

st.set_page_config(
    page_title=f"yjg30737's Streamlit Image Generator",
    page_icon="👋",
    initial_sidebar_state="expanded",
)

st.title("Image Generator")

model = 'dall-e-3'

# Set OpenAI API key from Streamlit secrets
client = OpenAI(api_key=st.secrets['OPENAI_API_KEY'])

default_obj = {
    'size': '1024x1024',
    "prompt": "Astronaut in a jungle, cold color palette, muted colors, detailed, 8k",
    "negative_prompt": "ugly, deformed, noisy, blurry, distorted"
}

size, prompt, negative_prompt, button = widget(default_obj)
if button:
    with st.spinner('Generating image…'):
        start_time = time.time()

        response = client.images.generate(
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
import streamlit as st
import requests
from PIL import Image
import io
import os
import uuid
import atexit
import shutil

@atexit.register
def cleanup_temp_dir():
    temp_dir = "temp"
    if os.path.exists(temp_dir):
        shutil.rmtree(temp_dir)

st.set_page_config(page_title="AI Shopping Assistant", layout="wide")
st.title("AI Shopping Assistant")

FASTAPI_URL = "http://localhost:8600/chat"

if "chat_history" not in st.session_state:
    st.session_state.chat_history = [{
        "role": "assistant",
        "text": """
    Hi there! I'm your AI-powered shopping assistant

    Here’s what I can help you with:

    - Describe what you're looking for, and I’ll recommend the most relevant products  
    - Upload a product image to find visually similar items
    - Or just have a casual conversation with me!
    

    Let me know how I can help you today!
    """,
        "recommendations": None,
        "image": None
    }]

if "history_prompt" not in st.session_state:
    st.session_state.history_prompt = ""
if "upload_key" not in st.session_state:
    st.session_state.upload_key = str(uuid.uuid4())
with st.sidebar:
    st.sidebar.header("🔍 Want to search by image?")
    st.sidebar.caption("Upload a product photo to get similar recommendations.")
    uploaded_image = st.file_uploader(
        "Choose an image",
        type=["jpg", "jpeg", "png"],
        key=st.session_state.get("upload_key", "default_upload")
    )

user_input = st.chat_input("Type your message...")

if user_input or uploaded_image:
    image_data = None
    image_path = ""

    if uploaded_image:
        image_bytes = uploaded_image.read()
        image_data = Image.open(io.BytesIO(image_bytes))

        os.makedirs("temp", exist_ok=True)
        image_path = f"temp/{uuid.uuid4()}.png"
        with open(image_path, "wb") as f:
            f.write(image_bytes)

    st.session_state.chat_history.append({
        "role": "user",
        "text": user_input,
        "recommendations": None,
        "image": image_data
    })

    st.session_state.history_prompt += f"User: {user_input}\n"
    try:
        response = requests.post(FASTAPI_URL, json={
            "text": user_input,
            "image_path": image_path,
            "history_prompt": st.session_state.history_prompt
        })
        res_json = response.json()
        reply_text = res_json.get("text")
        recommendations = res_json.get("recommendations")
        reply_image_url = res_json.get("image_url")
        st.session_state.history_prompt += f"Assistant: {reply_text}\n"

    except Exception as e:
        reply_text = f"Error: {e}"
        reply_image_url = None
        recommendations = None

    st.session_state.chat_history.append({
        "role": "assistant",
        "text": reply_text,
        "recommendations": recommendations,
        "image": None
    })
    st.session_state.upload_key = str(uuid.uuid4())
    st.rerun()

for msg in st.session_state.chat_history:
    with st.chat_message(msg["role"]):
        if msg["text"]:
            st.markdown(msg["text"])
        if msg.get("recommendations"):
            for item in msg["recommendations"]:
                st.markdown(f"**[{item['name']}]({item['link']})**")
                st.image(item["image_path"], width=100)
        if msg["image"]:
            if isinstance(msg["image"], str):
                st.image(msg["image"], width=100)
            else:
                st.image(msg["image"], width=100)















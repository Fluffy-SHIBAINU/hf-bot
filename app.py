import streamlit as st
import requests
import os
import time

st.set_page_config(page_title="🧠 HF Chatbot", layout="centered")
st.title("🤖 Hugging Face Chatbot (Multi-Model)")

# Hugging Face token
HF_TOKEN = st.secrets.get("hf_token") or os.getenv("HF_TOKEN")
if not HF_TOKEN:
    st.warning("⚠️ Please set your Hugging Face token in Streamlit secrets or as an environment variable (HF_TOKEN)")
    st.stop()

# Model choices
MODELS = {
    "Flan-T5 Small": "google/flan-t5-small",
    "Mistral 7B Instruct": "mistralai/Mistral-7B-Instruct-v0.1",
    "Phi-2": "microsoft/phi-2"
}

# Sidebar
with st.sidebar:
    st.header("⚙️ Settings")
    model_choice = st.selectbox("🧠 Model", list(MODELS.keys()))
    clear = st.button("🧹 Clear Chat")

API_URL = f"https://api-inference.huggingface.co/models/{MODELS[model_choice]}"
headers = {"Authorization": f"Bearer {HF_TOKEN}"}

# API call
def query(inputs):
    response = requests.post(API_URL, headers=headers, json={"inputs": inputs})
    try:
        return response.json()
    except:
        return [{"generated_text": "[Error in response]"}]

# Session state
if "messages" not in st.session_state or clear:
    st.session_state.messages = []

if "user_input" not in st.session_state:
    st.session_state.user_input = ""

# Input field
user_input = st.text_input("You:", value=st.session_state.user_input, key="user_input")

if user_input and not st.session_state.get("input_sent", False):
    # Mark as submitted to prevent repeat
    st.session_state.input_sent = True

    # Context
    context = " ".join([msg for sender, msg in st.session_state.messages[-4:] if sender == "You"])
    full_input = context + " " + user_input if context else user_input

    with st.spinner("Thinking..."):
        result = query(full_input)
        reply = result[0].get("generated_text", "[No response]") if isinstance(result, list) else str(result)

    # Save messages
    st.session_state.messages.append(("You", user_input))
    st.session_state.messages.append(("Bot", reply))

    # Clear input
    st.session_state.user_input = ""

# Cleanup submit flag after render
if "input_sent" in st.session_state:
    del st.session_state.input_sent

# Render messages
st.divider()
for sender, msg in st.session_state.messages[::-1]:
    with st.chat_message("user" if sender == "You" else "assistant"):
        if sender == "Bot":
            response_placeholder = st.empty()
            streamed = ""
            for word in msg.split():
                streamed += word + " "
                response_placeholder.markdown(streamed)
                time.sleep(0.03)
        else:
            st.markdown(msg)

import streamlit as st
import requests
import os
import time

st.set_page_config(page_title="🧠 HF Chatbot", layout="centered")
st.title("🤖 Hugging Face Chatbot (Multi-Model)")

HF_TOKEN = st.secrets.get("hf_token") or os.getenv("HF_TOKEN")
if not HF_TOKEN:
    st.warning("⚠️ Please set your Hugging Face token in Streamlit secrets or as an environment variable (HF_TOKEN)")
    st.stop()

MODELS = {
    "Flan-T5 Small": "google/flan-t5-small",
    "Mistral 7B Instruct": "mistralai/Mistral-7B-Instruct-v0.1",
    "Phi-2": "microsoft/phi-2"
}

with st.sidebar:
    st.header("⚙️ Settings")
    model_choice = st.selectbox("🧠 Model", list(MODELS.keys()))
    if st.button("🧹 Clear Chat"):
        st.session_state.messages = []

API_URL = f"https://api-inference.huggingface.co/models/{MODELS[model_choice]}"
headers = {"Authorization": f"Bearer {HF_TOKEN}"}

def query_huggingface(prompt):
    response = requests.post(API_URL, headers=headers, json={"inputs": prompt})
    try:
        return response.json()
    except:
        return [{"generated_text": "[Error in response]"}]

# Chat state
if "messages" not in st.session_state:
    st.session_state.messages = []

# 💬 Render chat history (before input)
st.divider()
for sender, msg in st.session_state.messages:
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

# 📝 Input below the chat
with st.form("chat_form", clear_on_submit=True):
    user_input = st.text_input("You:")
    submitted = st.form_submit_button("Send")

if submitted and user_input:
    # Append user input first
    st.session_state.messages.append(("You", user_input))

    # ⛔️ Avoid repeating user_input — build context from previous only
    context = " ".join(
        [msg for sender, msg in st.session_state.messages[-6:-2] if sender == "You"]
    )
    prompt = context.strip()

    with st.spinner("Thinking..."):
        result = query_huggingface(prompt if prompt else user_input)
        reply = result[0].get("generated_text", "[No response]") if isinstance(result, list) else str(result)

    st.session_state.messages.append(("Bot", reply))

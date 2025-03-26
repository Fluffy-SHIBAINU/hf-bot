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

# 세션 메시지 초기화
if "messages" not in st.session_state:
    st.session_state.messages = []

# 입력 폼 (채팅 아래쪽에 위치)
with st.form("chat_form", clear_on_submit=True):
    user_input = st.text_input("You:")
    submitted = st.form_submit_button("Send")

# 이전 메시지 출력 (최신이 아래로)
for sender, msg in st.session_state.messages:
    with st.chat_message("user" if sender == "You" else "assistant"):
        st.markdown(msg)

# 새 메시지 처리
if submitted and user_input:
    # 1. 유저 메시지 즉시 렌더링
    with st.chat_message("user"):
        st.markdown(user_input)

    # 2. 메시지 세션에 추가
    st.session_state.messages.append(("You", user_input))

    # 3. context 만들기 (최근 대화 3개)
    context = " ".join([msg for sender, msg in st.session_state.messages[-6:] if sender == "You"])
    prompt = context.strip() or user_input

    # 4. API 호출
    with st.chat_message("assistant"):
        with st.spinner("Thinking..."):
            result = query_huggingface(prompt)
            reply = result[0].get("generated_text", "[No response]") if isinstance(result, list) else str(result)

        # 5. 스트리밍 출력
        response_placeholder = st.empty()
        streamed = ""
        for word in reply.split():
            streamed += word + " "
            response_placeholder.markdown(streamed)
            time.sleep(0.03)

    # 6. 응답 저장
    st.session_state.messages.append(("Bot", reply))

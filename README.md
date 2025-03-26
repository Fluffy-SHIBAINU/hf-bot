# 🤖 Hugging Face Chatbot (Complete)

Multi-model chatbot powered by Hugging Face Inference API with chat UI features:
- Bubble-style message UI
- Streaming-like bot responses
- Clear chat history button

## 🧠 Supported Models
- google/flan-t5-small
- mistralai/Mistral-7B-Instruct-v0.1
- microsoft/phi-2

## 🔧 Setup
Create a Hugging Face token at: https://huggingface.co/settings/tokens  
Add to Streamlit secrets as `hf_token`

## 🚀 Local Run
```bash
pip install -r requirements.txt
streamlit run app.py
```

## 🌐 Deploy
Upload to Streamlit Cloud and set your secret token.
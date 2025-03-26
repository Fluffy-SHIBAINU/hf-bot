# 🤖 Hugging Face Chatbot (Complete)


<img width="1474" alt="image" src="https://github.com/user-attachments/assets/0c19a285-4ea1-4013-aed4-6270d6de49cd" />

https://hf-bot.streamlit.app/

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

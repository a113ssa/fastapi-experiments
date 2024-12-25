import os

import requests
import streamlit as st
from dotenv import load_dotenv

load_dotenv()

st.title("Chatbot")

if "messages" not in st.session_state:
    st.session_state.messages = []

for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])


if prompt := st.chat_input("Write your prompt in this field"):
    st.session_state.messages.append({"role": "user", "content": prompt})

    with st.chat_message("user"):
        st.text(prompt)

    with st.chat_message("assistant"):
        response = requests.get(
            f"{os.getenv('API_URL', 'http://localhost:8000')}/generate/text?prompt={prompt}",
            timeout=60,
        ).text

        st.text(response)

    st.session_state.messages.append(
        {"role": "assistant", "content": "Here is your answer"}
    )

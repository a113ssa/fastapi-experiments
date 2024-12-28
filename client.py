import os

import requests
import streamlit as st
from dotenv import load_dotenv

load_dotenv()

st.title("Chatbot")

if "text_chosen" not in st.session_state:
    st.session_state.text_chosen = False

if "audio_chosen" not in st.session_state:
    st.session_state.audio_chosen = False


def text_clicked():
    st.session_state.text_chosen = True
    st.session_state.audio_chosen = False


def audio_clicked():
    st.session_state.text_chosen = False
    st.session_state.audio_chosen = True


if "messages" not in st.session_state:
    st.session_state.messages = []

for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])
        content = message["content"]

        if isinstance(content, bytes):
            st.audio(content)
        else:
            st.markdown(content)

st.button("Text bot", on_click=text_clicked)
st.button("Audio bot", on_click=audio_clicked)

if st.session_state.text_chosen:
    if prompt := st.chat_input("Write your prompt to generate text answer"):
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

if st.session_state.audio_chosen:
    if prompt := st.chat_input("Write your prompt to generate audio"):
        with st.chat_message("assistant"):
            response = requests.get(
                f"{os.getenv('API_URL', 'http://localhost:8000')}/generate/audio?prompt={prompt}",
                timeout=60,
            ).content

            st.text("Here is your audio")
            st.audio(response)

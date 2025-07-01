import streamlit as st
import requests

st.title("TailorTalk Booking Assistant")

if "messages" not in st.session_state:
    st.session_state.messages = []

user_input = st.text_input("Ask the assistant:")

if user_input:
    st.session_state.messages.append(("You", user_input))
    response = requests.post("http://localhost:8000/chat/", json={"message": user_input})
    assistant_reply = response.json()["reply"]
    st.session_state.messages.append(("Assistant", assistant_reply))

for speaker, msg in st.session_state.messages:
    st.markdown(f"**{speaker}:** {msg}")

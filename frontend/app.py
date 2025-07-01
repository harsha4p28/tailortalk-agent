import streamlit as st
import requests

st.title("TailorTalk Booking Assistant")

if "messages" not in st.session_state:
    st.session_state.messages = []

user_input = st.text_input("Ask the assistant:")

if user_input:
    st.session_state.messages.append(("You", user_input))
    response = requests.post(
        "https://tailortalk-backend.up.railway.app/chat/",
        json={"message": user_input}
    )

    try:
        response_json = response.json()
        st.write("Debug Response JSON:", response_json)  
        assistant_reply = response_json["reply"]
    except Exception as e:
        st.error(f"Error parsing response: {e}")
        st.write("Full response text:", response.text)  
        assistant_reply = "Something went wrong."

    st.session_state.messages.append(("Assistant", assistant_reply))
    
for speaker, msg in st.session_state.messages:
    st.markdown(f"**{speaker}:** {msg}")

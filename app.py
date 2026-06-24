import streamlit as st

st.title("🤖 Chatbot Ridcha Data")

question = st.text_input("Pose ta question")

if question:
    st.write("Tu as demandé :", question)
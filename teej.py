
import streamlit as st

# Title of the app
st.title("Hello Streamlit 👋")

# Text input
name = st.text_input("Enter your name:")

# Button
if st.button("Say Hello"):
    st.write(f"Hello, {name}! Welcome to Streamlit 🚀")

# Slider
age = st.slider("Select your age:", 1, 100, 25)
st.write(f"Your age is {age}")

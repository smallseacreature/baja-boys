import streamlit as st

st.title("Simple B2Twin App")

# Add some text
st.write("Welcome to the B2Twin Hackathon app!")

# Add a simple input widget
user_input = st.text_input("Enter your name:")

# Display dynamic content based on input
if user_input:
    st.write(f"Hello, {user_input}! Ready to analyze Biosphere 2 data?")

# Add a button
if st.button("Click me!"):
    st.write("Button was clicked!")
    st.balloons()
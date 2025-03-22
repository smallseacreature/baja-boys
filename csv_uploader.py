import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split
from ollama import Ollama
import streamlit as st
import requests

# Load the AI model
model = Ollama.load_model('path/to/model')

# Create a CSV uploader function
def upload_csv(file):
    df = pd.read_csv(file)
    # Clean and preprocess the data as needed
    return df

# Define the uploader function
def upload_to_ai(file):
    df = upload_csv(file)
    # Use the streamlit library to create a file uploader widget
    st.file_uploader("Upload CSV file", type=["csv"])
    # Use the requests library to send a POST request to the AI model's API endpoint
    url = "https://api.example.com/ai-model"
    files = {'file': file}
    response = requests.post(url, files=files)
    # Pass the preprocessed data to the AI model for inference or training
    predictions = model.predict(df)
    return predictions

# Create a Streamlit app
st.title("CSV Uploader to AI Model")
st.file_uploader("Upload CSV file", type=["csv"], key="csv_file")
if st.button("Upload"):
    file = st.session_state.csv_file
    predictions = upload_to_ai(file)
    st.write(predictions)
import streamlit as st
import pandas as pd

uploaded_file = st.file_uploader("Choose a CSV file", type="csv")

if uploaded_file is not None:
    # Read the file
    df = pd.read_csv(uploaded_file)
    st.write(df)
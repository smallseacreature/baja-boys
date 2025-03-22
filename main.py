import streamlit as st
import pandas as pd
import requests
import json

st.title("B2Twin Data Analyzer")
st.write("Upload Biosphere 2 sensor data for analysis with Mistral")

# File uploader widget
uploaded_file = st.file_uploader("Choose a CSV file", type="csv")

if uploaded_file is not None:
    # Read the CSV file
    df = pd.read_csv(uploaded_file)
    
    # Display the data
    st.subheader("Data Preview:")
    st.dataframe(df.head())
    
    # Get basic stats
    st.subheader("Data Statistics:")
    st.dataframe(df.describe())
    
    # Prepare data for the model
    # Convert a sample of the data to string to avoid overwhelming the model
    data_sample = df.head(20).to_string()
    
    # Button to analyze data
    if st.button("Analyze with Mistral"):
        with st.spinner("Analyzing data with Mistral..."):
            try:
                # Create prompt for Mistral
                prompt = f"""
                I'm sharing sensor data from Biosphere 2 with you. 
                Please analyze this data and tell me:
                1. What kind of measurements these appear to be
                2. Any patterns or anomalies you notice
                3. What scientific insights we might gain from this data
                4. How this data might help understand Earth's ecosystems or prepare for space travel
                
                Here's the data sample:
                {data_sample}
                
                Please provide a thoughtful analysis focusing on the environmental implications.
                """
                
                # Send request to local Ollama instance
                response = requests.post(
                    "http://localhost:11434/api/generate",
                    json={
                        "model": "mistral",  # or whatever model name you've pulled
                        "prompt": prompt,
                        "stream": False
                    }
                )
                
                # Process response
                if response.status_code == 200:
                    result = response.json()
                    st.subheader("Mistral's Analysis:")
                    st.write(result["response"])
                else:
                    st.error(f"Error: Received status code {response.status_code}")
                    st.write(response.text)
            
            except Exception as e:
                st.error(f"Error connecting to Ollama: {e}")
                st.info("Make sure Ollama is running and the Mistral model is installed.")
                st.info("To install Mistral: Run 'ollama pull mistral' in your terminal.")
    
    # Option to download columns as separate CSVs
    st.subheader("Download Individual Columns")
    col = st.selectbox("Select a column to download:", df.columns)
    if st.button(f"Download {col} data"):
        csv = df[col].to_csv(index=False)
        st.download_button(
            label=f"Download {col} as CSV",
            data=csv,
            file_name=f"{col}.csv",
            mime="text/csv"
        )
else:
    st.info("Please upload a CSV file to begin analysis.")

# Add information about the model
st.sidebar.title("About")
st.sidebar.info(
    "This app uses Mistral via Ollama to analyze Biosphere 2 sensor data. "
    "The analysis helps understand Earth's ecosystems and prepare for space travel."
)
st.sidebar.title("Instructions")
st.sidebar.write(
    "1. Upload a CSV file with Biosphere 2 sensor data\n"
    "2. Review the data preview and statistics\n"
    "3. Click 'Analyze with Mistral' to get AI interpretation\n"
    "4. Optionally download individual columns for focused analysis"
)
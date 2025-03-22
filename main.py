import streamlit as st
import pandas as pd
import requests
import json
import io

st.title("CSV Data Analyzer with Mistral AI")
st.write("Upload a CSV file to get AI-powered insights about your data.")

# File uploader widget
uploaded_file = st.file_uploader("Choose a CSV file", type="csv")

# Function to send data to Ollama
def query_mistral(prompt):
    response = requests.post(
        "http://localhost:11434/api/generate",
        json={
            "model": "mistral",
            "prompt": prompt,
            "stream": False
        }
    )
    return json.loads(response.text)["response"]

# Process the file when uploaded
if uploaded_file is not None:
    # Display a success message
    st.success("File successfully uploaded!")
    
    # Read the CSV file
    df = pd.read_csv(uploaded_file)
    
    # Display file preview
    st.subheader("Data Preview")
    st.write(df.head())
    
    # Display basic statistics
    st.subheader("Basic Statistics")
    st.write(df.describe())
    
    # Get column names
    columns = df.columns.tolist()
    
    # Information about the dataset to send to the model
    info = {
        "filename": uploaded_file.name,
        "shape": df.shape,
        "columns": columns,
        "data_types": df.dtypes.to_dict(),
        "head": df.head().to_csv(index=False),
        "describe": df.describe().to_csv()
    }
    
    # Convert to a string representation for the AI
    prompt = f"""
    Analyze the following CSV data and provide insights:
    
    Filename: {info['filename']}
    Number of rows: {info['shape'][0]}
    Number of columns: {info['shape'][1]}
    
    Column names and data types:
    {json.dumps(info['data_types'], indent=2, default=str)}
    
    Sample data (first 5 rows):
    {info['head']}
    
    Statistical summary:
    {info['describe']}
    
    Please provide:
    1. A brief overview of what this dataset contains
    2. Key observations about the data
    3. Potential patterns or trends you notice
    4. Suggestions for further analysis or visualization
    5. Any data quality issues that should be addressed
    """
    
    # Show a spinner while waiting for the AI response
    with st.spinner("Analyzing data with Mistral AI..."):
        try:
            analysis = query_mistral(prompt)
            
            # Display the AI analysis
            st.subheader("AI Analysis")
            st.markdown(analysis)
            
        except Exception as e:
            st.error(f"Error querying Mistral AI: {str(e)}")
            st.info("Make sure Ollama is running with the Mistral model loaded. Run 'ollama run mistral' in your terminal.")
else:
    st.info("Please upload a CSV file to begin analysis.")

# Add some helpful information at the bottom
st.markdown("---")
st.write("This app uses the Mistral model via Ollama to analyze CSV files. Make sure you have Ollama running with the Mistral model installed.")
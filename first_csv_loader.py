# Create a modified version of your app (main_workaround.py)
import streamlit as st
import pandas as pd
import requests
import json
import io

st.title("CSV Data Analyzer with Mistral AI")

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
    st.success("File successfully uploaded!")
    
    # Read the CSV file
    df = pd.read_csv(uploaded_file)
    
    # Display file preview without using st.write for DataFrames
    st.subheader("Data Preview")
    
    # Convert DataFrame to HTML and display that instead
    # This avoids the pyarrow dependency issue
    st.markdown(df.head().to_html(), unsafe_allow_html=True)
    
    # Display basic statistics as text/markdown
    st.subheader("Basic Statistics")
    st.markdown(f"**Shape**: {df.shape[0]} rows, {df.shape[1]} columns")
    st.markdown(f"**Columns**: {', '.join(df.columns.tolist())}")
    
    # Convert describe() to markdown
    st.markdown("**Summary Statistics:**")
    st.markdown(df.describe().to_markdown())
    
    # Information about the dataset to send to the model
    info = {
        "filename": uploaded_file.name,
        "shape": df.shape,
        "columns": df.columns.tolist(),
        "data_types": {str(k): str(v) for k, v in df.dtypes.items()},
        "head": df.head().values.tolist(),
        "column_names": df.columns.tolist(),
        "describe": df.describe().to_dict()
    }
    
    # Convert to a string representation for the AI
    prompt = f"""
    Analyze the following CSV data and provide insights:
    
    Filename: {info['filename']}
    Number of rows: {info['shape'][0]}
    Number of columns: {info['shape'][1]}
    
    Column names: {', '.join(info['columns'])}
    
    Data types:
    {json.dumps(info['data_types'], indent=2)}
    
    Sample data (first 5 rows):
    {json.dumps(info['head'], indent=2)}
    
    Statistical summary:
    {json.dumps(info['describe'], indent=2)}
    
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
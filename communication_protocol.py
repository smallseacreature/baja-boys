# streamlit_app.py
import streamlit as st
import pandas as pd
import requests
import json
import threading
from ai_comms import AICommsProtocol
from app import run_flask_server
import time

# Start Flask server in a separate thread
server_thread = threading.Thread(target=run_flask_server)
server_thread.daemon = True
server_thread.start()

# Give the server a moment to start
time.sleep(1)

# Initialize communication protocol
comms = AICommsProtocol(team_id="baja_boys")

# Query Mistral function
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

# Streamlit App
st.title("B2Twin Hackathon - AI Communication Protocol")
st.write("Upload a CSV file and collaborate with other AIs")

# Initialize session state
if 'peers' not in st.session_state:
    st.session_state.peers = {}
    st.session_state.conversation_history = {}
    st.session_state.df = None

# File upload section
uploaded_file = st.file_uploader("Choose a CSV file", type="csv")

if uploaded_file is not None:
    try:
        # Read the CSV file
        df = pd.read_csv(uploaded_file)
        st.session_state.df = df
        
        # Display file preview
        st.subheader("Data Preview")
        st.markdown(df.head().to_html(), unsafe_allow_html=True)
        
        # Basic statistics
        st.subheader("Basic Statistics")
        st.markdown(f"**Shape**: {df.shape[0]} rows, {df.shape[1]} columns")
        st.markdown(f"**Columns**: {', '.join(df.columns.tolist())}")
        
        # Local analysis with Mistral
        with st.expander("Local AI Analysis"):
            if st.button("Analyze with Local AI"):
                with st.spinner("Analyzing with Mistral..."):
                    # Format prompt for analysis
                    info = {
                        "filename": uploaded_file.name,
                        "shape": df.shape,
                        "columns": df.columns.tolist(),
                        "data_types": {str(k): str(v) for k, v in df.dtypes.items()},
                        "head": df.head().values.tolist(),
                        "column_names": df.columns.tolist(),
                        "describe": df.describe().to_dict()
                    }
                    
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
                    
                    analysis = query_mistral(prompt)
                    st.markdown(analysis)
    except Exception as e:
        st.error(f"Error reading CSV: {str(e)}")

# AI Communication section
st.header("AI Communication Protocol")

# Discover peers
with st.expander("Discover Peer AIs"):
    if st.button("Scan Network for Peers")
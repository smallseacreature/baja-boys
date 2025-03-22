import os
import pandas as pd
import ollama

# Path to the folder containing CSV files
folder_path = "/Users/connor/dev/hackArizona/B2Twin-Hackathon/data"

# Read all CSV files in the folder
csv_data = []
for file in os.listdir(folder_path):
    if file.endswith(".csv"):
        file_path = os.path.join(folder_path, file)
        df = pd.read_csv(file_path)
        csv_data.append(f"### File: {file}\n{df.head().to_string()}")  # Show first few rows

# Combine all CSV summaries
data_summary = "\n\n".join(csv_data)

# Send data to Mistral for analysis
response = ollama.chat(model="mistral", messages=[
    {"role": "user", "content": f"Here is some data from multiple CSV files:\n{data_summary}\nCan you summarize key insights?"}
])

print(response["message"]["content"])

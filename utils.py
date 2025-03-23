from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.chrome import ChromeDriverManager
import time
from selenium.webdriver.support.ui import Select
from selenium.webdriver.chrome.options import Options
import os
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
import shutil

# Specify the path to the folder where you want to save the files
download_folder = "/Users/connor/dev/hackArizona/Biosphere-Ocean-Data" # Change this to your desired folder

# Set Chrome options to specify the download folder
chrome_options = Options()
chrome_options.add_argument("--headless")  # Optional: if you want to run headlessly
chrome_options.add_argument("--no-sandbox")  # Optional: helps prevent errors in some environments
chrome_options.add_argument("--disable-dev-shm-usage")  # Optional

# Set the download directory preference
prefs = {
    "download.default_directory": download_folder,
    "download.prompt_for_download": False,  # Prevents the browser from asking where to save files
    "download.directory_upgrade": True,
    "safebrowsing.enabled": True  # Optional: prevent Chrome from blocking downloads
}

chrome_options.add_experimental_option("prefs", prefs)

    

USERNAME = "hackathon"
PASSWORD = "99](uM6"

# Function to initialize a WebDriver instance
def get_driver():
    options = webdriver.ChromeOptions()
    service = Service(ChromeDriverManager().install())
    options.add_argument("--headless")  # Run without opening browser (optional)
    driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)
    return driver

def move_files():
    

    # Paths to the source (Downloads) and destination folders
    downloads_folder = os.path.expanduser('/Users/connor/Downloads')  # Default path to Downloads folder
    destination_folder = '/Users/connor/dev/hackArizona/Biosphere-Ocean-Data'  # Replace with your desired destination folder path

    # Make sure the destination folder exists
    if not os.path.exists(destination_folder):
        os.makedirs(destination_folder)

    # List all files in the Downloads folder
    for filename in os.listdir(downloads_folder):
        print("checkin "+str(filename))
        if filename.endswith('.csv'):  # Check if the file is a CSV file
            source_path = os.path.join(downloads_folder, filename)
            destination_path = os.path.join(destination_folder, filename)

            # Move the file to the destination folder
            shutil.move(source_path, destination_folder)
            print(f'Moved: {filename}')

def delete_folder_contents(folder_path):
    # Iterate through all the files and folders in the directory
    for filename in os.listdir(folder_path):
        file_path = os.path.join(folder_path, filename)
        
        # If it's a file, delete it
        if os.path.isfile(file_path):
            os.remove(file_path)
            print(f"Deleted file: {file_path}")
        # If it's a directory, remove it (and its contents)
        elif os.path.isdir(file_path):
            shutil.rmtree(file_path)
            print(f"Deleted folder: {file_path}")




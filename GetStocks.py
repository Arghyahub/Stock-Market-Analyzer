import requests
from dotenv import load_dotenv
import os

load_dotenv()

file_id = os.getenv('DRIVE')
download_link = f"https://drive.google.com/uc?id={file_id}"
response = requests.get(download_link)

if response.status_code == 200:
    with open('stocks.txt', 'wb') as file:
        file.write(response.content)
        print("Stock write success")
else:
    print("Failed to download the file.")
    exit()


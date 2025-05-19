# sync.py

import os
import requests

RD_TOKEN = os.getenv("RD_TOKEN")
DEST_DIR = "/downloads"

HEADERS = {
    "Authorization": f"Bearer {RD_TOKEN}"
}

def list_files():
    response = requests.get("https://api.real-debrid.com/rest/1.0/streams", headers=HEADERS)
    response.raise_for_status()
    return response.json()

def get_file_info(stream_id):
    response = requests.get(f"https://api.real-debrid.com/rest/1.0/streaming/transcode/{stream_id}", headers=HEADERS)
    response.raise_for_status()
    return response.json()

def download_file(file_info):
    filen

import os
import requests

RD_TOKEN = os.getenv("RD_TOKEN")
if not RD_TOKEN:
    raise ValueError("Please set RD_TOKEN environment variable with your Real-Debrid API token.")

DEST_DIR = "/downloads"
os.makedirs(DEST_DIR, exist_ok=True)

HEADERS = {
    "Authorization": f"Bearer {RD_TOKEN}"
}

def list_downloads():
    url = "https://api.real-debrid.com/rest/1.0/downloads"
    resp = requests.get(url, headers=HEADERS)
    resp.raise_for_status()
    return resp.json()

def download_single_file(filename, url):
    if not url:
        print(f"⚠️ No download link for {filename}")
        return

    dest_path = os.path.join(DEST_DIR, filename)
    if os.path.exists(dest_path):
        print(f"✅ Already downloaded: {filename}")
        return

    print(f"⬇️ Downloading {filename} ...")
    with requests.get(url, stream=True) as r:
        r.raise_for_status()
        with open(dest_path, "wb") as f:
            for chunk in r.iter_content(chunk_size=8192):
                f.write(chunk)
    print(f"✔️ Saved to {dest_path}")

def process_download_item(item):
    # If item is a list, process each element
    if isinstance(item, list):
        for subitem in item:
            process_download_item(subitem)
    # If item is a dict, check if it has 'files' (a list)
    elif isinstance(item, dict):
        if "files" in item and isinstance(item["files"], list):
            for file_entry in item["files"]:
                process_download_item(file_entry)
        else:
            filename = item.get("filename", "unknown")
            url = item.get("link")
            download_single_file(filename, url)
    else:
        print(f"⚠️ Skipping unknown item type: {type(item)}")

def main():
    print("🔄 Syncing Real-Debrid cloud files...")
    downloads = list_downloads()
    process_download_item(downloads)

if __name__ == "__main__":
    main()

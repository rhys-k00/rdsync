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

def download_file(download):
    # If 'files' key exists, it's a multi-file package
    if "files" in download:
        for file_entry in download["files"]:
            download_file(file_entry)
    else:
        filename = download.get("filename", "unknown")
        url = download.get("link")
        download_single_file(filename, url)

def main():
    print("🔄 Syncing Real-Debrid downloads...")
    downloads = list_downloads()
    for download in downloads:
        try:
            download_file(download)
        except Exception as e:
            # If filename key exists, show it, else show ID or generic info
            file_id = download.get("id", "unknown id")
            print(f"❌ Error downloading {file_id}: {e}")

if __name__ == "__main__":
    main()

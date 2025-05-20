import os
import requests

# Your Real-Debrid API token from environment variable
RD_TOKEN = os.getenv("RD_TOKEN")
if not RD_TOKEN:
    raise ValueError("Please set RD_TOKEN environment variable with your Real-Debrid API token.")

# Where to save downloads
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

def download_file(download):
    # If download is a list, recursively download each item
    if isinstance(download, list):
        for item in download:
            download_file(item)
        return

    filename = download.get("filename", "unknown")
    url = download.get("link")

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

def main():
    print("🔄 Syncing Real-Debrid downloads...")
    downloads = list_downloads()

    for download in downloads:
        try:
            download_file(download)
        except Exception as e:
            # Use repr(download) to help debug which item caused error
            print(f"❌ Error downloading {repr(download)}: {e}")

if __name__ == "__main__":
    main()

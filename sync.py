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

def download_single_file(filename, url):
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
    # If download itself is a list, handle each element recursively
    if isinstance(download, list):
        for d in download:
            download_file(d)
        return

    filename = download.get("filename", "unknown")
    link = download.get("link")

    if not link:
        print(f"⚠️ No download link for {filename}")
        return

    # If link is a list of URLs, download each one with suffixes
    if isinstance(link, list):
        for idx, single_link in enumerate(link, start=1):
            file_suffix = f"_{idx}" if len(link) > 1 else ""
            dest_filename = f"{filename}{file_suffix}"
            download_single_file(dest_filename, single_link)
    else:
        download_single_file(filename, link)

def main():
    print("🔄 Syncing Real-Debrid downloads...")
    downloads = list_downloads()

    for idx, download in enumerate(downloads):
        print(f"\n--- Download {idx} type: {type(download)} ---")
        if isinstance(download, list):
            print("It's a list! Content sample:", download[:2])
        else:
            print("It's a dict! Keys:", list(download.keys()))

        try:
            download_file(download)
        except Exception as e:
            # Defensive fallback to print something meaningful
            name = download if isinstance(download, str) else download.get("filename", "unknown")
            print(f"❌ Error downloading {name}: {e}")

if __name__ == "__main__":
    main()

import os
import requests

# Your Real-Debrid API token from environment variable
RD_TOKEN = os.getenv("RD_TOKEN")
if not RD_TOKEN:
    raise ValueError("Please set RD_TOKEN environment variable with your Real-Debrid API token.")

# Change this to the mount point on your HDD
DEST_DIR = "/media/downloads"
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

    for item in downloads:
        if isinstance(item, dict):
            if "files" in item and isinstance(item["files"], list):
                for file in item["files"]:
                    if isinstance(file, dict):
                        try:
                            download_file(file)
                        except Exception as e:
                            print(f"❌ Error downloading {file.get('filename', 'unknown')}: {e}")
                    else:
                        print(f"⚠️ Unexpected file format inside package: {file}")
            else:
                try:
                    download_file(item)
                except Exception as e:
                    print(f"❌ Error downloading {item.get('filename', 'unknown')}: {e}")
        else:
            print(f"⚠️ Skipping unexpected item type: {type(item)}")

if __name__ == "__main__":
    main()

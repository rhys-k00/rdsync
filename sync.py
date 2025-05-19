import os
import requests

RD_TOKEN = os.getenv("RD_TOKEN")
DEST_DIR = "/downloads"

HEADERS = {
    "Authorization": f"Bearer {RD_TOKEN}"
}

def list_files():
    # Correct endpoint to list downloaded files on Real-Debrid
    response = requests.get("https://api.real-debrid.com/rest/1.0/downloads", headers=HEADERS)
    response.raise_for_status()
    return response.json()

def get_file_info(download_id):
    # Updated endpoint to get info about a specific download
    response = requests.get(f"https://api.real-debrid.com/rest/1.0/downloads/{download_id}", headers=HEADERS)
    response.raise_for_status()
    return response.json()

def download_file(file_info):
    filename = file_info.get("filename") or "unknown"
    # Use 'link' key from RD's download info for direct download URL
    url = file_info.get("link")

    if not url:
        print(f"⚠️ No URL for {filename}")
        return

    dest_path = os.path.join(DEST_DIR, filename)
    if os.path.exists(dest_path):
        print(f"✅ Already downloaded: {filename}")
        return

    print(f"⬇️ Downloading: {filename}")
    with requests.get(url, stream=True) as r:
        r.raise_for_status()
        with open(dest_path, "wb") as f:
            for chunk in r.iter_content(chunk_size=8192):
                f.write(chunk)
    print(f"✔️ Saved to: {dest_path}")

def main():
    print("🔄 Syncing Real-Debrid cloud files...")
    downloads = list_files()

    for download in downloads:
        download_id = download.get("id")
        if not download_id:
            continue
        try:
            file_info = get_file_info(download_id)
            download_file(file_info)
        except Exception as e:
            print(f"❌ Error with download {download_id}: {e}")

if __name__ == "__main__":
    main()

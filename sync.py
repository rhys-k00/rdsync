def download_file(file_info):
    # if file_info is a list, download each file inside
    if isinstance(file_info, list):
        for fi in file_info:
            download_file(fi)
        return

    filename = file_info.get("filename", "unknown")
    url = file_info.get("streamingUrl") or file_info.get("download")

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
    files = list_files()

    for f in files:
        download_id = f.get("id")
        if not download_id:
            continue
        try:
            file_info = get_file_info(download_id)
            download_file(file_info)
        except Exception as e:
            print(f"❌ Error with download {download_id}: {e}")

import os
import requests
import subprocess
import sys

RD_TOKEN = os.getenv("RD_TOKEN")
if not RD_TOKEN:
    raise ValueError("Please set RD_TOKEN environment variable with your Real-Debrid API token.")

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

def is_already_handled(filename):
    """Return True if original or converted file exists."""
    original_path = os.path.join(DEST_DIR, filename)
    base, _ = os.path.splitext(filename)
    converted_filename = f"{base}_720p.mp4"
    converted_path = os.path.join(DEST_DIR, converted_filename)
    return os.path.exists(original_path) or os.path.exists(converted_path)

def convert_to_720p(input_path):
    base, _ = os.path.splitext(input_path)
    output_path = base + "_720p.mp4"

    if os.path.exists(output_path):
        print(f"✅ Conversion already exists: {os.path.basename(output_path)}")
        return True

    print(f"🎞️ Converting to 720p: {os.path.basename(input_path)}")
    command = [
        "ffmpeg",
        "-i", input_path,
        "-vf", "scale=w=1280:h=720:force_original_aspect_ratio=decrease",
        "-preset", "ultrafast",
        "-crf", "28",
        "-c:a", "copy",
        output_path
    ]

    try:
        subprocess.run(command, check=True, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
        print(f"✅ Conversion done: {os.path.basename(output_path)}")
        return True
    except subprocess.CalledProcessError:
        print(f"❌ Conversion failed: {os.path.basename(input_path)}")
        return False

def download_file(download):
    filename = download.get("filename", "unknown")
    url = download.get("download") or download.get("link")

    if not url:
        print(f"⚠️ No download link for {filename}")
        return

    if is_already_handled(filename):
        print(f"✅ Already downloaded or converted: {filename}")
        return

    dest_path = os.path.join(DEST_DIR, filename)

    print(f"⬇️ Downloading {filename} ...")
    try:
        with requests.get(url, stream=True) as r:
            r.raise_for_status()
            with open(dest_path, "wb") as f:
                for chunk in r.iter_content(chunk_size=8192):
                    f.write(chunk)
        print(f"✔️ Saved to {dest_path}")
    except Exception as e:
        print(f"❌ Failed to download {filename}: {e}")
        return

    # Convert after successful download
    success = convert_to_720p(dest_path)

    # Delete original only if conversion succeeded
    if success:
        try:
            os.remove(dest_path)
            print(f"🗑️ Deleted original file: {filename}")
        except Exception as e:
            print(f"⚠️ Failed to delete original file {filename}: {e}")
    else:
        print(f"⚠️ Leaving original file {filename} to retry conversion later or manual fix.")

def main():
    print("🔄 Syncing Real-Debrid downloads...")
    try:
        downloads = list_downloads()
    except requests.HTTPError as e:
        print(f"❌ HTTP error while listing downloads: {e}")
        return
    except Exception as e:
        print(f"❌ Unexpected error while listing downloads: {e}")
        return

    if not downloads:
        print("No downloads found.")
        return

    for download in downloads:
        try:
            download_file(download)
        except Exception as e:
            print(f"❌ Error processing {download.get('filename', 'unknown')}: {e}")

if __name__ == "__main__":
    main()

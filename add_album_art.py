import os
import requests
import re
from mutagen.mp3 import MP3
from mutagen.id3 import ID3, APIC

BASE_DIR = "Disneyland_Audio"
ALBUM_ART_DIR = "AlbumArt"
ALBUM_ART_URL = "http://soundsofdisneyland.com/AlbumArt/"
ALBUM_DATA_URL = "http://soundsofdisneyland.com/sodlr/albumData.js"

def sanitize_filename(name):
    """Removes problematic characters from filenames."""
    return "".join(c if c.isalnum() or c in " _-()" else "_" for c in name).strip()

def fetch_album_data():
    """Scrape album data from the JavaScript file to extract album-art mappings."""
    print("🔍 Fetching album data...")
    album_map = {}

    try:
        response = requests.get(ALBUM_DATA_URL)
        if response.status_code != 200:
            print("❌ Failed to fetch album data!")
            return {}

        # Extract JSON-like album data from JavaScript
        js_text = response.text
        matches = re.findall(r'poster:\s*"([^"]+)",\s*album:\s*"([^"]+)"', js_text)

        for poster, album in matches:
            safe_album = sanitize_filename(album)
            album_map[safe_album] = poster.replace("AlbumArt/", "")

        print(f"✅ Found {len(album_map)} album-art mappings.")
    except Exception as e:
        print(f"❌ Error fetching album data: {e}")

    return album_map

def download_album_art(album_map):
    """Download album art based on extracted album metadata."""
    os.makedirs(ALBUM_ART_DIR, exist_ok=True)

    for album, art_filename in album_map.items():
        safe_album = sanitize_filename(album)
        image_filename = os.path.join(ALBUM_ART_DIR, f"{safe_album}.jpg")

        print(f"🖼️ Saving {image_filename} for album: {album}")  # Debugging print

        # Check if image already exists
        if os.path.exists(image_filename):
            continue

        # Download album art
        try:
            response = requests.get(ALBUM_ART_URL + art_filename)
            if response.status_code == 200:
                with open(image_filename, "wb") as img_file:
                    img_file.write(response.content)
                print(f"✔ Downloaded album art: {image_filename}")
            else:
                print(f"❌ Failed to download: {art_filename}")
        except Exception as e:
            print(f"❌ Error downloading {art_filename}: {e}")

def remove_existing_album_art(mp3_path):
    """Removes all embedded album art (APIC tags) from an MP3 file."""
    try:
        audio = MP3(mp3_path, ID3=ID3)
        if audio.tags is None:
            return  # No tags to remove

        apic_keys = [key for key in audio.tags.keys() if key.startswith("APIC")]
        if apic_keys:
            for key in apic_keys:
                del audio.tags[key]
            audio.save()
            print(f"🗑 Removed existing album art from {mp3_path}")

    except Exception as e:
        print(f"❌ Error removing album art from {mp3_path}: {e}")

def embed_album_art():
    """Remove old album art and embed new album art into MP3 files based on album folder names."""
    for folder in os.listdir(BASE_DIR):
        folder_path = os.path.join(BASE_DIR, folder)
        if not os.path.isdir(folder_path):
            continue

        # Find album art
        safe_album = sanitize_filename(folder)
        image_path = os.path.join(ALBUM_ART_DIR, f"{safe_album}.jpg")

        if not os.path.exists(image_path):
            print(f"⚠ No album art found for {folder}")
            continue

        for file in os.listdir(folder_path):
            if file.endswith(".mp3"):
                file_path = os.path.join(folder_path, file)
                
                # Remove existing album art before embedding
                remove_existing_album_art(file_path)

                try:
                    audio = MP3(file_path, ID3=ID3)
                    if audio.tags is None:
                        audio.tags = ID3()

                    # Embed new album art
                    with open(image_path, "rb") as img_file:
                        audio.tags.add(APIC(
                            encoding=3,
                            mime="image/jpeg",
                            type=3,
                            desc="Cover",
                            data=img_file.read()
                        ))
                    
                    audio.save()
                    print(f"✔ Embedded album art into {file_path}")

                except Exception as e:
                    print(f"❌ Error embedding art for {file}: {e}")

if __name__ == "__main__":
    album_map = fetch_album_data()
    if album_map:
        download_album_art(album_map)
        embed_album_art()
        print("✅ Album art processing complete!")

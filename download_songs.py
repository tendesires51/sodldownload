import os
import requests
import shutil
import threading
from urllib.parse import unquote
from tqdm import tqdm
from concurrent.futures import ThreadPoolExecutor
from pydub import AudioSegment
from mutagen.easyid3 import EasyID3
from mutagen.mp4 import MP4
from mutagen.id3 import ID3, TIT2, TPE1, TALB, TRCK, TCON, TDRC

# URLs
JS_FILE_URL = "http://soundsofdisneyland.com/sodlr/albumData.js"

# Base directory
BASE_DIR = "Disneyland_Audio"
os.makedirs(BASE_DIR, exist_ok=True)

# Lock for progress bar updates
lock = threading.Lock()

### 1️⃣ Download and Process a Single File ###
def download_and_process(url, album, progress_bar):
    """Downloads a song, converts it if needed, and ensures it's in the correct folder."""
    album_folder = os.path.join(BASE_DIR, sanitize_filename(album))
    os.makedirs(album_folder, exist_ok=True)

    filename = sanitize_filename(url.split("/")[-1])
    file_path = os.path.join(album_folder, filename)

    if os.path.exists(file_path):
        with lock:
            tqdm.write(f"Already downloaded: {file_path}")
            progress_bar.update(1)
        return

    with lock:
        tqdm.write(f"Downloading: {url}")

    response = requests.get(url, stream=True)
    if response.status_code == 200:
        with open(file_path, "wb") as file:
            for chunk in response.iter_content(1024):
                file.write(chunk)

        with lock:
            tqdm.write(f"Saved: {file_path}")

        # Convert if necessary
        if file_path.lower().endswith(".m4a"):
            file_path = convert_m4a_to_mp3(file_path)

        # Move if needed
        if file_path:
            move_file_by_metadata(file_path)

    with lock:
        progress_bar.update(1)

### 2️⃣ Convert M4A to MP3 ###
def convert_m4a_to_mp3(file_path):
    """Converts an M4A file to MP3 while preserving metadata."""
    try:
        audio = MP4(file_path)
        tags = audio.tags

        sound = AudioSegment.from_file(file_path, format="m4a")
        mp3_path = file_path.rsplit(".", 1)[0] + ".mp3"

        sound.export(mp3_path, format="mp3", bitrate="320k")

        mp3_tags = ID3()
        if "\xa9nam" in tags: mp3_tags["TIT2"] = TIT2(encoding=3, text=tags["\xa9nam"][0])
        if "\xa9ART" in tags: mp3_tags["TPE1"] = TPE1(encoding=3, text=tags["\xa9ART"][0])
        if "\xa9alb" in tags: mp3_tags["TALB"] = TALB(encoding=3, text=tags["\xa9alb"][0])
        if "trkn" in tags: mp3_tags["TRCK"] = TRCK(encoding=3, text=str(tags["trkn"][0][0]))
        if "\xa9gen" in tags: mp3_tags["TCON"] = TCON(encoding=3, text=tags["\xa9gen"][0])
        if "\xa9day" in tags: mp3_tags["TDRC"] = TDRC(encoding=3, text=tags["\xa9day"][0])

        mp3_tags.save(mp3_path)

        os.remove(file_path)
        with lock:
            tqdm.write(f"Converted: {file_path} → {mp3_path}")
        return mp3_path
    except Exception as e:
        with lock:
            tqdm.write(f"Error converting {file_path}: {e}")
        return file_path  

### 3️⃣ Get Album Metadata ###
def get_album_metadata(file_path):
    """Extracts album metadata from an MP3 file."""
    try:
        if file_path.lower().endswith(".mp3"):
            audio = EasyID3(file_path)
            return audio.get("album", [None])[0]
    except:
        return None

### 4️⃣ Move File If Needed ###
def move_file_by_metadata(file_path):
    """Moves the file to its correct album folder based on metadata."""
    album_name = get_album_metadata(file_path)

    if album_name:
        album_folder = os.path.join(BASE_DIR, sanitize_filename(album_name.strip()))
        os.makedirs(album_folder, exist_ok=True)

        current_folder = os.path.dirname(file_path)
        if os.path.basename(current_folder) != os.path.basename(album_folder):
            new_path = os.path.join(album_folder, os.path.basename(file_path))
            shutil.move(file_path, new_path)
            with lock:
                tqdm.write(f"Moved: {os.path.basename(file_path)} → {album_name}/")
            return new_path

    return file_path  

### Helper Functions ###
def fetch_album_data():
    """Download albumData.js and extract MP3/M4A URLs along with album names."""
    response = requests.get(JS_FILE_URL)

    if response.status_code != 200:
        return []

    mp3_files = []
    current_album = "Miscellaneous"

    for line in response.text.splitlines():
        line = line.strip()

        if line.startswith('album:'):
            current_album = line.split(':', 1)[1].strip().strip('",')
            current_album = " ".join(current_album.split())  
            if not current_album:
                current_album = "Miscellaneous"

        if line.startswith('mp3:'):
            mp3_path = line.split(':', 1)[1].strip().strip('",')
            full_url = f"http://soundsofdisneyland.com/{unquote(mp3_path)}"

            album_name = current_album if current_album else "Miscellaneous"
            album_name = album_name.strip()  

            mp3_files.append((full_url, album_name))

    return mp3_files

def sanitize_filename(name):
    """Remove invalid characters from filenames, but keep valid extensions."""
    if not name:
        name = "Miscellaneous"

    if "." in name:
        base, ext = name.rsplit(".", 1)
        ext = "." + ext
    else:
        base, ext = name, ""

    base = "".join(c if c.isalnum() or c in " -_()" else "_" for c in base).strip()

    return base + ext

### 🚀 Run Everything 🚀 ###
if __name__ == "__main__":
    mp3_files = fetch_album_data()

    if mp3_files:
        print(f"Downloading {len(mp3_files)} songs...\n")
        
        # Initialize tqdm progress bar
        with tqdm(total=len(mp3_files), desc="Downloading Songs", unit="song", leave=True) as progress_bar:
            # Use ThreadPoolExecutor to download multiple songs at once
            with ThreadPoolExecutor(max_workers=5) as executor:  # Adjust workers as needed
                futures = [executor.submit(download_and_process, mp3_url, album_name, progress_bar) for mp3_url, album_name in mp3_files]
                for future in futures:
                    future.result()  # Wait for all downloads to finish

    print("\nAll tasks completed! 🎵")

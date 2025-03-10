import os
import re
from mutagen.mp3 import MP3
from mutagen.id3 import ID3

BASE_DIR = "Disneyland_Audio"  # Change if needed

def normalize_text(text):
    """Removes underscores, periods, apostrophes, ampersands, colons, and extra spaces for comparison."""
    return re.sub(r"[_\.\'&:!]", " ", text).strip()

def check_metadata():
    """Scan MP3 files and check for missing metadata and folder mismatches."""
    for folder in os.listdir(BASE_DIR):
        folder_path = os.path.join(BASE_DIR, folder)
        if not os.path.isdir(folder_path):
            continue

        normalized_folder = normalize_text(folder)

        for file in os.listdir(folder_path):
            if file.endswith(".mp3"):
                file_path = os.path.join(folder_path, file)
                try:
                    audio = MP3(file_path, ID3=ID3)

                    # Extract metadata fields with fallbacks
                    title = audio.tags.get("TIT2", ["(No Title)"])[0]
                    album = audio.tags.get("TALB", ["(No Album)"])[0]
                    artist = audio.tags.get("TPE1", ["(No Artist)"])[0]
                    album_artist = audio.tags.get("TPE2", ["(No Album Artist)"])[0]

                    normalized_album = normalize_text(album)

                    # Check for missing album metadata
                    if album == "(No Album)":
                        print(f"{file} is missing album metadata!")

                    # Check if album tag matches the folder name (ignoring formatting differences)
                    if normalized_album != normalized_folder:
                        print(f"{file} has incorrect album tag! (Tag: {album}, Folder: {folder})")

                except Exception as e:
                    print(f"Error reading {file}: {e}")

if __name__ == "__main__":
    print("Checking metadata...")
    check_metadata()
input("\nTask completed! Press Enter to exit...")

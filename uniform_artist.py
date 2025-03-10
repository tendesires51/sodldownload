import os
from mutagen.mp3 import MP3
from mutagen.id3 import ID3, TPE2
from tqdm import tqdm

# Base directory for Disneyland music
BASE_DIR = "Disneyland_Audio"

### 1️⃣ Update Album Artist Field ###
def update_album_artist():
    """Set the Album Artist field to 'Disney' for all MP3 files."""
    for folder in os.listdir(BASE_DIR):
        folder_path = os.path.join(BASE_DIR, folder)
        if not os.path.isdir(folder_path):
            continue  # Skip if it's not a folder

        for file in tqdm(os.listdir(folder_path), desc=f"Updating {folder}"):
            if file.endswith(".mp3"):
                file_path = os.path.join(folder_path, file)
                set_album_artist(file_path)

### 2️⃣ Modify MP3 Metadata ###
def set_album_artist(mp3_file):
    """Change the Album Artist tag to 'Disney' in an MP3 file."""
    try:
        audio = MP3(mp3_file, ID3=ID3)

        if "TPE2" in audio and audio["TPE2"].text[0] == "Disney":
            return  # Skip if it's already set

        audio.tags.add(TPE2(encoding=3, text="Disney"))
        audio.save()
        tqdm.write(f"Updated: {mp3_file}")
    except Exception as e:
        tqdm.write(f"Error updating {mp3_file}: {e}")

### Run Everything ###
if __name__ == "__main__":
    print("Updating all MP3 files with Album Artist: Disney...")
    update_album_artist()
    print("\nAll files updated!")
input("\nTask completed! Press Enter to exit...")

import os
from mutagen.mp3 import MP3
from mutagen.id3 import ID3

# Base directory where your Disneyland_Audio files are stored
BASE_DIR = "E:\\Disneyland\\Disneyland_Audio"

# List of albums to remove
ALBUMS_TO_REMOVE = ["Holiday", "Haunted Mansion Holiday"]

def remove_unwanted_tracks():
    print("Scanning for Holiday tracks...")

    for folder in os.listdir(BASE_DIR):
        folder_path = os.path.join(BASE_DIR, folder)

        if not os.path.isdir(folder_path):
            continue  # Skip if it's not a folder

        for file in os.listdir(folder_path):
            if file.endswith(".mp3"):
                file_path = os.path.join(folder_path, file)
                try:
                    audio = MP3(file_path, ID3=ID3)
                    album = audio.tags.get("TALB", ["Unknown"])[0]

                    if album in ALBUMS_TO_REMOVE:
                        print(f"Deleting: {file} (Album: {album})")
                        os.remove(file_path)
                
                except Exception as e:
                    print(f"Error reading {file}: {e}")

    print("Cleanup complete!")

if __name__ == "__main__":
    remove_unwanted_tracks()
print("Task completed!")

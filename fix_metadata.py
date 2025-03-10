import os
import re
import shutil
from mutagen.mp3 import MP3
from mutagen.id3 import ID3, TALB, TIT2, TPE1, TPE2

BASE_DIR = "Disneyland_Audio"

def normalize_text(text):
    """Removes underscores, periods, apostrophes, ampersands, colons, and extra spaces for comparison."""
    return re.sub(r"[_\.\'&:!]", " ", text).strip()

def fix_metadata():
    """Fix missing metadata, ensure ID3v2.3 compatibility, and move misfiled tracks."""
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

                    # Ensure ID3 tags exist
                    if audio.tags is None:
                        audio.tags = ID3()

                    # Set missing metadata
                    if "TALB" not in audio:
                        audio.tags.add(TALB(encoding=3, text=folder))  # Set album from folder name
                    if "TIT2" not in audio:
                        audio.tags.add(TIT2(encoding=3, text=file))  # Set title from filename
                    if "TPE1" not in audio:
                        audio.tags.add(TPE1(encoding=3, text="Walt Disney"))  # Default artist
                    if "TPE2" not in audio:
                        audio.tags.add(TPE2(encoding=3, text="Disney"))  # Set album artist

                    album = audio.tags.get("TALB", [folder])[0]  # Fallback to folder name if missing
                    normalized_album = normalize_text(album)

                    # Move file to correct album folder if necessary
                    if normalized_album != normalized_folder:
                        correct_folder_path = os.path.join(BASE_DIR, album)
                        os.makedirs(correct_folder_path, exist_ok=True)  # Ensure correct folder exists

                        new_path = os.path.join(correct_folder_path, file)
                        shutil.move(file_path, new_path)
                        print(f"Moved: {file} -> {album}/")

                    audio.save()
                    print(f"Fixed: {file_path}")

                except Exception as e:
                    print(f"Error fixing {file}: {e}")

if __name__ == "__main__":
    print("Fixing metadata and organizing files...")
    fix_metadata()
input("\nTask completed! Press Enter to exit...")

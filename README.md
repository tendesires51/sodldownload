# Sounds of Disneyland Audio Manager

A collection of Python scripts for **downloading, organizing, and managing Sounds of Disneyland audio files**. This project automates tasks such as **downloading songs, fixing metadata, organizing files, and adding album art**.

## 🚀 Features
- **Download Songs**: Fetches Disneyland music files from the web.
- **Check Metadata**: Scans MP3 files for missing or incorrect metadata.
- **Fix Metadata**: Automatically corrects metadata and moves files to the right folders.
- **Uniform Artist**: Standardizes artist names for consistency.
- **Add Album Art**: Inserts album covers into MP3 files.
- **Remove Holiday Tracks**: Deletes seasonal tracks from your collection.
- **Modern PyQt6 GUI**: A sleek **Graphical User Interface** (GUI) to easily run these scripts.

---

## 🛠 Installation

### **1️⃣ Install Dependencies**
Make sure you have Python **3.10+** installed. Then install all required packages:

`
pip install -r requirements.txt
`

### **2️⃣ Run the GUI**
To use the graphical interface, simply run:

`
python gui.py
`

Alternatively, you can execute any script manually, e.g.:

`
python download_songs.py
`

---

## 📂 Scripts Overview

### **1️⃣ Download Songs (`download_songs.py`)**
- Fetches and saves Disneyland audio files.
- Converts `.m4a` files to `.mp3` if needed.
- Moves tracks to the correct folders based on metadata.

### **2️⃣ Check Metadata (`check_metadata.py`)**
- Scans all MP3 files.
- Detects **missing album names, track numbers, or incorrect metadata**.

### **3️⃣ Fix Metadata (`fix_metadata.py`)**
- Corrects missing metadata tags (Title, Artist, Album, etc.).
- Moves files into the correct album folder based on their metadata.

### **4️⃣ Uniform Artist (`uniform_artist.py`)**
- Ensures all artist names are consistent.

### **5️⃣ Add Album Art (`add_album_art.py`)**
- Inserts album covers into MP3 files.
- Uses existing images or downloads them automatically.

### **6️⃣ Remove Holiday Tracks (`remove_holiday_tracks.py`)**
- Finds and deletes **seasonal** tracks because they have weird metadata issues.
- Helps keep your collection clean.

---

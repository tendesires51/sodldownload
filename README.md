# Sounds of Disneyland - Automated Download & Metadata Fixing

This collection of scripts downloads, organizes, and fixes metadata for all tracks from Sounds of Disneyland.  
Follow the steps below in the correct order to ensure everything works properly.

---

## 0. PREREQUISITES (Install Before Running)
- Install **Python** (latest version)
- Install required Python libraries:  
  ```
  pip install -r requirements.txt
  ```
- Install **FFmpeg** and add it to your system **PATH**:  
  1. Download from [FFmpeg Builds](https://www.gyan.dev/ffmpeg/builds/)
  2. Extract and copy the `"bin"` folder path (e.g., `C:\ffmpeg\bin`)
  3. Add it to your system **PATH** environment variable  

- Ensure a **stable internet connection** (scripts download a large number of files)

---

## 1. DOWNLOAD SONGS
**Run:**  
```
python download_songs.py
```
**What it does:**  
- Fetches album data from the website  
- Downloads all MP3/M4A files  
- Converts M4A to MP3 automatically  
- Organizes files into correct album folders  

---

## 2. CHECK METADATA
**Run:**  
```
python check_metadata.py
```
**What it does:**  
- Scans all downloaded MP3 files  
- Lists missing or incorrect metadata fields  
- Ensures files have correct album and artist tags  

---

## 3. FIX METADATA
**Run:**  
```
python fix_metadata.py
```
**What it does:**  
- Fills in missing metadata fields (title, album, track number, etc.)  
- Ensures all tags are properly formatted  
- Prevents issues with blank metadata in media players  

---

## 4. UNIFORM ARTIST FIELD
**Run:**  
```
python uniform_artist.py
```
**What it does:**  
- Updates the **"ALBUM ARTIST"** field for all songs to **"Disney"**  
- Preserves the individual **"ARTIST"** field for composers  
- Ensures consistency across all tracks  

---

## 5. ADD ALBUM ART
**Run:**  
```
python add_album_art.py
```
**What it does:**  
- Fetches correct album art based on website data  
- Downloads and organizes album covers  
- Removes any existing (incorrect) album art  
- Embeds the correct album art into each MP3 file  

---

## 6. CHECK METADATA AGAIN
**Run:**  
```
python check_metadata.py
```
**What it does:**  
- Verifies all metadata is now correctly formatted  
- Confirms that album art is properly embedded  
- Ensures no tracks are missing important tags  

---

## 7. (OPTIONAL) REMOVE HOLIDAY ALBUMS
**Run:**  
```
python remove_holiday_tracks.py
```
**What it does:**  
- The albums **"Holiday"** and **"Haunted Mansion Holiday"** are incorrectly formatted in the source data  
- This causes some tracks to be mislabeled, affecting their organization  
- If you prefer, this script will **remove all tracks** from these albums  
- Only use this if you do not want these albums in your collection  

---

## ALL DONE!  
At this point, all songs should be **fully organized, properly tagged, and ready for use** in any media player.

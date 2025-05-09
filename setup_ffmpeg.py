import os
import sys
import zipfile
import urllib.request
import shutil
from config import FFMPEG_PATH

def download_ffmpeg():
    """Download and set up FFmpeg"""
    ffmpeg_dir = os.path.dirname(os.path.dirname(FFMPEG_PATH))
    bin_dir = os.path.dirname(FFMPEG_PATH)
    
    # Create directories if they don't exist
    os.makedirs(ffmpeg_dir, exist_ok=True)
    os.makedirs(bin_dir, exist_ok=True)
    
    # FFmpeg download URL (using gyan.dev build which is reliable)
    ffmpeg_url = "https://www.gyan.dev/ffmpeg/builds/ffmpeg-release-essentials.zip"
    zip_path = os.path.join(ffmpeg_dir, "ffmpeg.zip")
    
    print("Downloading FFmpeg...")
    try:
        # Download the zip file
        urllib.request.urlretrieve(ffmpeg_url, zip_path)
        
        print("Extracting FFmpeg...")
        with zipfile.ZipFile(zip_path, 'r') as zip_ref:
            # Extract only the necessary executables
            for file in zip_ref.namelist():
                if file.endswith(('.exe', '.dll')) and '/bin/' in file:
                    # Extract the file
                    source = zip_ref.extract(file, ffmpeg_dir)
                    # Move it to the bin directory
                    dest = os.path.join(bin_dir, os.path.basename(file))
                    shutil.move(source, dest)
        
        # Clean up
        os.remove(zip_path)
        print("FFmpeg has been successfully installed!")
        return True
        
    except Exception as e:
        print(f"Error downloading FFmpeg: {e}")
        print("\nPlease download FFmpeg manually from https://www.ffmpeg.org/download.html")
        print(f"and place the executables in: {bin_dir}")
        return False

if __name__ == "__main__":
    if not os.path.exists(FFMPEG_PATH):
        print("FFmpeg not found. Attempting to download...")
        download_ffmpeg()
    else:
        print("FFmpeg is already installed.") 
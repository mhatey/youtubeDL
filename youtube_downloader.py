#!/usr/bin/env python3
import sys
import os
import yt_dlp
from config import FFMPEG_PATH, FFPROBE_PATH

def download_video(url, output_path=None):
    """
    Download a YouTube video from the given URL
    
    Args:
        url (str): YouTube video URL
        output_path (str, optional): Directory to save the video. Defaults to current directory.
    """
    try:
        # Set output directory
        output_dir = output_path if output_path else os.getcwd()
        
        # Configure yt-dlp options
        ydl_opts = {
            'format': 'best',  # Download best quality
            'outtmpl': os.path.join(output_dir, '%(title)s.%(ext)s'),
            'noplaylist': True,  # Only download single video, not playlist
            'progress_hooks': [progress_hook],
            'ffmpeg_location': os.path.dirname(FFMPEG_PATH),
        }
        
        # Download the video
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            info = ydl.extract_info(url, download=False)
            title = info.get('title', 'Video')
            resolution = info.get('resolution', 'unknown')
            filesize_mb = info.get('filesize', 0) / (1024 * 1024)
            
            # Display download information
            print(f"Downloading: {title}")
            print(f"Resolution: {resolution}")
            print(f"Estimated file size: {filesize_mb:.2f} MB")
            
            # Perform the actual download
            ydl.download([url])
            
        print(f"Download complete! Saved to: {output_dir}")
        return True
    except Exception as e:
        print(f"Error downloading video: {e}")
        print("\nTroubleshooting tips:")
        print("1. Make sure the video URL is valid and accessible")
        print("2. Check your internet connection")
        print("3. Try updating yt-dlp: pip install --upgrade yt-dlp")
        return False

def download_audio(url, output_path=None):
    """
    Download a YouTube video as MP3 audio from the given URL
    
    Args:
        url (str): YouTube video URL
        output_path (str, optional): Directory to save the audio. Defaults to current directory.
    """
    try:
        # Set output directory
        output_dir = output_path if output_path else os.getcwd()
        
        # Configure yt-dlp options for MP3 download
        ydl_opts = {
            'format': 'bestaudio/best',
            'postprocessors': [{
                'key': 'FFmpegExtractAudio',
                'preferredcodec': 'mp3',
                'preferredquality': '192',
            }],
            'outtmpl': os.path.join(output_dir, '%(title)s.%(ext)s'),
            'noplaylist': True,
            'progress_hooks': [progress_hook],
            'ffmpeg_location': os.path.dirname(FFMPEG_PATH),
        }
        
        # Download the audio
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            info = ydl.extract_info(url, download=False)
            title = info.get('title', 'Audio')
            
            # Display download information
            print(f"Downloading audio: {title}")
            print(f"Format: MP3 (192kbps)")
            
            # Perform the actual download
            ydl.download([url])
            
        print(f"Download complete! Saved to: {output_dir}")
        return True
    except Exception as e:
        print(f"Error downloading audio: {e}")
        print("\nTroubleshooting tips:")
        print("1. Make sure the video URL is valid and accessible")
        print("2. Check your internet connection")
        print("3. Make sure FFmpeg is properly configured")
        print("4. Try updating yt-dlp: pip install --upgrade yt-dlp")
        return False

def progress_hook(d):
    """
    Display download progress
    """
    if d['status'] == 'downloading':
        percent = d.get('_percent_str', 'unknown')
        speed = d.get('_speed_str', 'unknown')
        eta = d.get('_eta_str', 'unknown')
        print(f"\rProgress: {percent} Speed: {speed} ETA: {eta}", end='')
    elif d['status'] == 'finished':
        print("\nDownload finished, now processing file...")

def main():
    # Check if URL is provided as command line argument
    if len(sys.argv) > 1:
        url = sys.argv[1]
        output_path = sys.argv[2] if len(sys.argv) > 2 else None
        download_type = sys.argv[3].lower() if len(sys.argv) > 3 else "video"
        
        if download_type == "audio" or download_type == "mp3":
            download_audio(url, output_path)
        else:
            download_video(url, output_path)
    else:
        # Interactive mode
        print("YouTube Downloader")
        print("------------------------")
        url = input("Enter YouTube URL: ")
        output_path = input("Enter output directory (leave blank for current directory): ")
        output_path = output_path if output_path.strip() else None
        
        download_type = input("Download as (video/audio): ").lower()
        if download_type == "audio" or download_type == "mp3":
            download_audio(url, output_path)
        else:
            download_video(url, output_path)

if __name__ == "__main__":
    main() 
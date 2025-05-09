from flask import Flask, render_template, request, send_file, url_for, redirect
import os
import yt_dlp
import uuid
import threading
import re
import time
from datetime import datetime
from config import FFMPEG_PATH, FFPROBE_PATH

app = Flask(__name__)

# Store download status
downloads = {}

def strip_ansi_codes(s):
    """Remove ANSI escape codes from a string."""
    return re.sub(r'\x1b\[[0-9;]*[a-zA-Z]', '', s)

def get_download_dir():
    """Get or create download directory"""
    download_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)), "downloads")
    os.makedirs(download_dir, exist_ok=True)
    return download_dir

def clean_old_downloads():
    """Remove downloads older than 1 hour"""
    download_dir = get_download_dir()
    current_time = time.time()
    for filename in os.listdir(download_dir):
        file_path = os.path.join(download_dir, filename)
        # Check if older than 1 hour (3600 seconds)
        if os.path.isfile(file_path) and current_time - os.path.getmtime(file_path) > 3600:
            try:
                os.remove(file_path)
            except:
                pass

def download_video_task(url, download_id, download_type="video"):
    """Background task to download a video or audio"""
    download_dir = get_download_dir()
    
    # Configure yt-dlp options
    if download_type == "audio":
        ydl_opts = {
            'format': 'bestaudio/best',
            'postprocessors': [{
                'key': 'FFmpegExtractAudio',
                'preferredcodec': 'mp3',
                'preferredquality': '192',
            }],
            'outtmpl': os.path.join(download_dir, f'{download_id}_%(title)s.%(ext)s'),
            'noplaylist': True,
            'progress_hooks': [lambda d: progress_hook(d, download_id)],
            'ffmpeg_location': os.path.dirname(FFMPEG_PATH),
        }
    else:
        ydl_opts = {
            'format': 'best',  # Download best quality
            'outtmpl': os.path.join(download_dir, f'{download_id}_%(title)s.%(ext)s'),
            'noplaylist': True,  # Only download single video, not playlist
            'progress_hooks': [lambda d: progress_hook(d, download_id)],
            'ffmpeg_location': os.path.dirname(FFMPEG_PATH),
        }
    
    try:
        downloads[download_id]['status'] = 'extracting'
        
        # Extract info first
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            info = ydl.extract_info(url, download=False)
            title = info.get('title', 'Media')
            downloads[download_id]['title'] = title
            downloads[download_id]['start_time'] = datetime.now()
            downloads[download_id]['type'] = download_type
            
            # Start actual download
            downloads[download_id]['status'] = 'downloading'
            ydl.download([url])
            
        # Find the downloaded file
        for filename in os.listdir(download_dir):
            if filename.startswith(f"{download_id}_"):
                file_path = os.path.join(download_dir, filename)
                downloads[download_id]['filename'] = filename
                downloads[download_id]['file_path'] = file_path
                downloads[download_id]['status'] = 'complete'
                return
                
    except Exception as e:
        downloads[download_id]['status'] = 'error'
        downloads[download_id]['error'] = strip_ansi_codes(str(e))

def progress_hook(d, download_id):
    """Update download progress"""
    if download_id in downloads:
        if d['status'] == 'downloading':
            downloads[download_id]['status'] = 'downloading'
            downloads[download_id]['progress'] = d.get('_percent_str', '0%')
            downloads[download_id]['speed'] = d.get('_speed_str', 'unknown')
            downloads[download_id]['eta'] = d.get('_eta_str', 'unknown')
        elif d['status'] == 'finished':
            downloads[download_id]['status'] = 'processing'

# Add current year context to all templates
@app.context_processor
def inject_current_year():
    return {'current_year': datetime.now().year}

@app.route('/')
def index():
    # Clean old downloads periodically
    threading.Thread(target=clean_old_downloads).start()
    return render_template('index.html')

@app.route('/download', methods=['POST'])
def download():
    url = request.form.get('url')
    download_type = request.form.get('download_type', 'video')
    
    if not url:
        return redirect(url_for('index'))
    
    # Generate unique ID for this download
    download_id = str(uuid.uuid4())
    
    # Initialize download status
    downloads[download_id] = {
        'url': url,
        'status': 'queued',
        'progress': '0%',
        'speed': 'N/A',
        'eta': 'N/A',
        'title': 'Extracting media info...',
        'type': download_type
    }
    
    # Start download in background
    threading.Thread(target=download_video_task, args=(url, download_id, download_type)).start()
    
    return redirect(url_for('status', download_id=download_id))

@app.route('/status/<download_id>')
def status(download_id):
    if download_id not in downloads:
        return redirect(url_for('index'))
    
    download_info = downloads[download_id]
    return render_template('status.html', download=download_info, download_id=download_id)

@app.route('/check_status/<download_id>')
def check_status(download_id):
    """API endpoint to check download status"""
    if download_id not in downloads:
        return {'status': 'not_found'}
    return downloads[download_id]

@app.route('/get_file/<download_id>')
def get_file(download_id):
    """Download the file"""
    if download_id not in downloads or downloads[download_id]['status'] != 'complete':
        return redirect(url_for('status', download_id=download_id))
    
    file_path = downloads[download_id]['file_path']
    return send_file(file_path, as_attachment=True)

if __name__ == '__main__':
    # Make sure download directory exists
    get_download_dir()
    
    # Create ffmpeg directory if it doesn't exist
    ffmpeg_dir = os.path.dirname(FFMPEG_PATH)
    if not os.path.exists(ffmpeg_dir):
        os.makedirs(os.path.dirname(ffmpeg_dir), exist_ok=True)
        os.makedirs(ffmpeg_dir, exist_ok=True)
    
    # Check if FFmpeg exists
    if not os.path.exists(FFMPEG_PATH):
        print("FFmpeg not found. Please download FFmpeg and place it in the 'ffmpeg/bin' directory.")
        print("Download FFmpeg from: https://www.ffmpeg.org/download.html")
        print(f"Expected path: {FFMPEG_PATH}")
    
    app.run(debug=True, host='0.0.0.0', port=5000) 
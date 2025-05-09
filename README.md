# YouTube Downloader

A Python web application that enables users to download YouTube videos or MP3 audio for offline use. Built with Flask and yt-dlp, this project offers a simple and responsive interface to quickly fetch and save YouTube content.

## Features

- **Easy-to-Use Web Interface** - Simply paste a YouTube URL and download begins with a single click
- **Video and MP3 Download Options** - Choose to download as video or extract audio as MP3
- **Real-Time Progress Tracking** - Monitor download progress, speed, and estimated time remaining
- **Best Quality Downloads** - Automatically selects the highest quality available format
- **Responsive Design** - Works seamlessly on mobile, tablet, and desktop devices
- **Automatic Cleanup** - Downloaded files are removed after one hour to save disk space
- **Command Line Support** - Can also be used directly from the terminal without the web interface

## Installation

1. **Clone the Repository**
   ```bash
   git clone https://github.com/mhatey/youtubeDL.git
   cd youtube_downloader
   ```

2. **Install Required Dependencies**
   ```bash
   pip install -r requirements.txt
   ```
   
   This will install:
   - yt-dlp - For downloading and processing YouTube videos
   - Flask - For the web interface

3. **Set Up FFmpeg** (Required for MP3 extraction)
   ```bash
   python setup_ffmpeg.py
   ```
   This script will automatically:
   - Download the latest FFmpeg release
   - Extract the necessary files
   - Set up the correct paths
   - No manual PATH configuration needed!

## Usage

### Web Interface

1. **Start the Web Server**
   ```bash
   python app.py
   ```

2. **Access the Application**
   - Open your browser and navigate to http://localhost:5000
   - Paste a YouTube video URL in the input field
   - Select your preferred format (Video or MP3 Audio)
   - Click "Download"
   - Wait for the download to complete
   - Click the download button to save the file to your device

### Command Line Interface

You can also use the downloader directly from the command line:

```bash
python youtube_downloader.py [youtube_url] [optional_output_directory] [video|audio]
```

**Examples:**
```bash
# Download video to current directory
python youtube_downloader.py https://www.youtube.com/watch?v=dQw4w9WgXcQ

# Download as MP3 audio to current directory
python youtube_downloader.py https://www.youtube.com/watch?v=dQw4w9WgXcQ . audio

# Download to specific directory
python youtube_downloader.py https://www.youtube.com/watch?v=dQw4w9WgXcQ /path/to/downloads video
```

## Troubleshooting

If you encounter issues:

1. Make sure the YouTube URL is valid and accessible
2. Check your internet connection
3. If FFmpeg setup fails:
   - Run `python setup_ffmpeg.py` again
   - If it still fails, download FFmpeg manually from https://www.ffmpeg.org/download.html
   - Place the downloaded files in the `ffmpeg/bin` directory of this project
4. Try updating yt-dlp: `pip install --upgrade yt-dlp`
5. Ensure you have sufficient disk space for the download
6. Some videos may be restricted and not downloadable

## Technical Details

- **Backend**: Flask web framework with threading for non-blocking downloads
- **Download Engine**: yt-dlp library for retrieving YouTube content
- **Audio Extraction**: FFmpeg for converting video to MP3 format
- **Front-end**: Bootstrap 5 for responsive design with FontAwesome icons
- **Storage**: Local file system with automatic cleanup of old files

## Legal Disclaimer

- This tool is for **personal and educational use only**
- Only download videos that you have the right to download
- Downloading copyrighted content without permission may violate YouTube's Terms of Service and copyright laws
- The developers of this project assume no liability for misuse of this tool

## License

This project is released under the MIT License. See the LICENSE file for details.

## Contributing

Contributions are welcome! If you'd like to improve this project:

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Submit a pull request

---

**Note:** This project is not affiliated with YouTube or Google in any way.
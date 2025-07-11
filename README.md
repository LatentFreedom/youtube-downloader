# YouTube Downloader

A Python-based YouTube video and audio downloader using yt-dlp for reliable downloads.

## Features

- Download single videos or entire playlists
- Multiple quality options (360p, 480p, 720p, 1080p, 4K)
- Audio-only downloads (MP3 format)
- Automatic duplicate detection (skips already downloaded files)
- Format listing to see available qualities
- Codec information checking

## Installation

### 1. Create virtual environment
```bash
python3 -m venv env
```

### 2. Activate virtual environment
```bash
source env/bin/activate
```

### 3. Install dependencies
```bash
pip install --upgrade pip
pip install -r requirements.txt
```

### 4. Install ffmpeg (required for video processing)
**macOS:**
```bash
brew install ffmpeg
```

**Ubuntu/Debian:**
```bash
sudo apt install ffmpeg
```

**Windows:**
Download from https://ffmpeg.org/download.html

## Usage

### Basic Commands

**Download video (best quality):**
```bash
python app.py -u "https://www.youtube.com/watch?v=VIDEO_ID"
```

**Download audio only:**
```bash
python app.py -u "https://www.youtube.com/watch?v=VIDEO_ID" -a
```

**Download with specific quality:**
```bash
python app.py -u "https://www.youtube.com/watch?v=VIDEO_ID" -q 720p
```

**Download playlist:**
```bash
python app.py -u "https://www.youtube.com/playlist?list=PLAYLIST_ID" -p
```

**List available formats:**
```bash
python app.py -u "https://www.youtube.com/watch?v=VIDEO_ID" -l
```

**Check codec info of downloaded file:**
```bash
python app.py -c "filename.mp4"
```

### Command Line Options

```
usage: app.py [-h] [-u URL] [-a] [-p] [-o OUTPUTPATH] [-q QUALITY] [-l] [-c CHECK_FILENAME]

options:
  -h, --help            show this help message and exit
  -u URL, --url URL     YouTube URL
  -a, --audio           Download audio only (MP3)
  -p, --playlist        Download entire playlist
  -o OUTPUTPATH, --output OUTPUTPATH
                        Custom output directory
  -q QUALITY, --quality QUALITY
                        Video quality (best, worst, 360p, 480p, 720p, 1080p, 4k)
  -l, --list-formats    List available formats for video
  -c CHECK_FILENAME, --check-codec CHECK_FILENAME
                        Check codec info for downloaded video
```

### Quality Options

- `best`: Highest available quality (recommended)
- `worst`: Lowest quality
- `360p`: 360p resolution
- `480p`: 480p resolution  
- `720p`: 720p resolution
- `1080p`: 1080p resolution
- `4k`: 4K resolution (if available)

### Output Directories

By default, files are saved to:
- Videos: `~/software/scrapers/youtube-downloader/videos/`
- Audio: `~/software/scrapers/youtube-downloader/audio/`

Use `-o` to specify a custom output directory.

## Examples

**Download best quality video:**
```bash
python app.py -u "https://www.youtube.com/watch?v=dQw4w9WgXcQ"
```

**Download 1080p video:**
```bash
python app.py -u "https://www.youtube.com/watch?v=dQw4w9WgXcQ" -q 1080p
```

**Download audio from playlist:**
```bash
python app.py -u "https://www.youtube.com/playlist?list=PLxxx" -p -a
```

**Check what formats are available:**
```bash
python app.py -u "https://www.youtube.com/watch?v=dQw4w9WgXcQ" -l
```

**Check codec of downloaded file:**
```bash
python app.py -c "Rick Astley - Never Gonna Give You Up.mp4"
```

## Troubleshooting

**"Command not found: yt-dlp"**
- Make sure you're in the virtual environment: `source env/bin/activate`
- Install requirements: `pip install -r requirements.txt`

**"ffprobe command not found"**
- Install ffmpeg: `brew install ffmpeg` (macOS) or `sudo apt install ffmpeg` (Ubuntu)

**Video won't play in QuickTime**
- The program downloads standard MP4 files with H.264 video and AAC audio
- If issues persist, try downloading with `-q best` for maximum compatibility

**Download fails**
- Check your internet connection
- Verify the YouTube URL is valid
- Try listing formats first with `-l` to see what's available
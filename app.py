from flask import Flask, request, jsonify, send_file
from flask_cors import CORS
import os
import yt_dlp
import glob

app = Flask(__name__)
CORS(app)

DOWNLOAD_DIR = os.path.join(os.getcwd(), "downloads")
COOKIES_FILE = os.path.join(os.getcwd(), "cookies.txt")  # Path to cookies file

if not os.path.exists(DOWNLOAD_DIR):
    os.makedirs(DOWNLOAD_DIR)

@app.route('/')
def home():
    return jsonify({'message': 'Welcome to the YouTube Downloader API'})

@app.route('/download', methods=['POST'])
def download_video():
    if not os.path.exists(COOKIES_FILE):
        return jsonify({'error': 'Cookies file not found'}), 400

    data = request.json
    video_url = data.get('url')
    resolution = data.get('resolution', 'best')
    format_type = data.get('format', 'mp4')

    if not video_url:
        return jsonify({'error': 'YouTube URL is required'}), 400
    
    print(f"Downloading {video_url} with cookies from {COOKIES_FILE}")

    if format_type == 'mp3':
        ydl_opts = {
            'format': 'bestaudio/best',
            'outtmpl': f"{DOWNLOAD_DIR}/%(title)s.%(ext)s",
            'postprocessors': [{
                'key': 'FFmpegExtractAudio',
                'preferredcodec': 'mp3',
                'preferredquality': '192',
            }],
            'ffmpeg_location': '/usr/bin/ffmpeg',
            'cookiefile': COOKIES_FILE,  # Use cookies file
        }
    else:
        ydl_opts = {
            'format': f'bestvideo[height<={resolution}]+bestaudio/best',
            'outtmpl': f"{DOWNLOAD_DIR}/%(title)s.%(ext)s",
            'merge_output_format': format_type,
            'ffmpeg_location': '/usr/bin/ffmpeg',
            'cookiefile': COOKIES_FILE,  # Use cookies file
        }

    try:
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            ydl.download([video_url])

        downloaded_files = glob.glob(os.path.join(DOWNLOAD_DIR, f"*.{format_type}"))
        if format_type == 'mp3':
            downloaded_files += glob.glob(os.path.join(DOWNLOAD_DIR, "*.mp3"))
        if downloaded_files:
            file_path = downloaded_files[0]
            file_name = os.path.basename(file_path)
            return jsonify({'file_name': file_name}), 200
        else:
            return jsonify({'error': 'File not found after download'}), 500

    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/download-file/<file_name>', methods=['GET'])
def serve_file(file_name):
    file_path = os.path.join(DOWNLOAD_DIR, file_name)
    if os.path.exists(file_path):
        return send_file(file_path, as_attachment=True, download_name=file_name)
    else:
        return jsonify({'error': 'File not found'}), 404

if __name__ == '__main__':
    app.run(debug=False)

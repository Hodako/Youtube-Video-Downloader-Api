from flask import Flask, request, jsonify, send_file
from flask_cors import CORS
import os
import yt_dlp
import glob

app = Flask(__name__)
CORS(app)

DOWNLOAD_DIR = os.path.join(os.getcwd(), "downloads")
if not os.path.exists(DOWNLOAD_DIR):
    os.makedirs(DOWNLOAD_DIR)

# Path to the cookies file (make sure to update this path to where you saved your cookies.txt)
COOKIES_FILE_PATH = os.path.join(os.getcwd(), 'cookies.txt')

@app.route('/')
def home():
    return jsonify({'message': 'Welcome to the YouTube Downloader API'})

@app.route('/download', methods=['POST'])
def download_video():
    data = request.json
    video_url = data.get('url')
    resolution = data.get('resolution', 'best')
    format_type = data.get('format', 'mp4')

    if not video_url:
        return jsonify({'error': 'YouTube URL is required'}), 400

    if format_type == 'mp3':
        ydl_opts = {
            'format': 'bestaudio/best',
            'outtmpl': f"{DOWNLOAD_DIR}/%(title)s.%(ext)s",
            'postprocessors': [
                {
                    'key': 'FFmpegExtractAudio',
                    'preferredcodec': 'mp3',
                    'preferredquality': '192',
                }
            ],
            'ffmpeg_location': '/usr/bin/ffmpeg',
            'cookies': COOKIES_FILE_PATH,  # Pass the cookies file path here
        }
    else:
        ydl_opts = {
            'format': f'bestvideo[height<={resolution}]+bestaudio/best',
            'outtmpl': f"{DOWNLOAD_DIR}/%(title)s.%(ext)s",
            'merge_output_format': format_type,
            'ffmpeg_location': '/usr/bin/ffmpeg',
            'cookies': COOKIES_FILE_PATH,  # Pass the cookies file path here
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

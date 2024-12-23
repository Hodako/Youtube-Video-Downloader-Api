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

COOKIES_DIR = os.path.join(os.getcwd(), "cookies")
if not os.path.exists(COOKIES_DIR):
    os.makedirs(COOKIES_DIR)


@app.route('/')
def home():
    return jsonify({'message': 'Welcome to the YouTube Downloader API'})


@app.route('/upload-cookies', methods=['POST'])
def upload_cookies():
    """Endpoint to upload a cookies file in Mozilla/Netscape format."""
    if 'file' not in request.files:
        return jsonify({'error': 'No file part in the request'}), 400

    file = request.files['file']
    if file.filename == '':
        return jsonify({'error': 'No selected file'}), 400

    if file:
        cookies_path = os.path.join(COOKIES_DIR, file.filename)
        file.save(cookies_path)
        return jsonify({'message': 'Cookies file uploaded successfully', 'cookies_path': cookies_path}), 200


@app.route('/download', methods=['POST'])
def download_video():
    """Download video with support for browser cookies."""
    data = request.form
    video_url = data.get('url')
    resolution = data.get('resolution', 'best')
    format_type = data.get('format', 'mp4')
    cookies_path = data.get('cookies_path')  # User-uploaded cookies path

    if not video_url:
        return jsonify({'error': 'YouTube URL is required'}), 400

    # Set yt-dlp options
    ydl_opts = {
        'format': f'bestvideo[height<={resolution}]+bestaudio/best',
        'outtmpl': f"{DOWNLOAD_DIR}/%(title)s.%(ext)s",
        'merge_output_format': format_type,
        'ffmpeg_location': '/usr/bin/ffmpeg',
    }

    # Add cookies handling
    if cookies_path and os.path.exists(cookies_path):
        ydl_opts['cookies'] = cookies_path  # Use uploaded cookies
    else:
        ydl_opts['cookiesfrombrowser'] = 'chrome'  # Use browser cookies

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

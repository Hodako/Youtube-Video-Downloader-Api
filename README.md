<h>YouTube Downloader with Video Preview</h>

This project is a web-based YouTube downloader that allows users to preview videos using the YouTube IFrame Player API and download them in their desired format and resolution.

Features

Video Preview: Preview the selected YouTube video before downloading.

Download Options: Choose video resolution (e.g., 144p, 720p, 1080p) or download as MP3.

User-Friendly Interface: Responsive design using Bootstrap and intuitive controls.

Backend Integration: Works with a Python Flask API for downloading YouTube videos.


Technologies Used

Frontend

HTML5, CSS3, JavaScript

Bootstrap for styling

Font Awesome for icons

YouTube IFrame Player API for video previews


Backend

Python Flask for the API

yt-dlp for video/audio downloading

Flask-CORS for handling cross-origin requests



---

Installation and Setup

Prerequisites

1. Python 3.7 or higher


2. Node.js (optional, for serving static files)


3. yt-dlp installed (pip install yt-dlp)


4. FFmpeg installed and added to your system's PATH


5. Valid browser cookies to handle YouTube authentication




---

Backend Setup

1. Clone the repository:

git clone https://github.com/your-username/youtube-downloader.git
cd youtube-downloader


2. Install Python dependencies:

pip install flask flask-cors yt-dlp


3. Run the Flask API:

python app.py



The API will run at http://localhost:5000.


---

Frontend Setup

1. Open the index.html file in a web browser.


2. Ensure the API is running and accessible.




---

Usage

1. Enter the YouTube video URL in the input field.


2. Click Preview Video to load the video for playback.


3. Select the desired resolution and format (MP4 or MP3).


4. Click Download to download the video or audio file.




---

API Endpoints

1. GET /

Returns a welcome message.

2. POST /download

Request body:

{
  "url": "YouTube video URL",
  "resolution": "Resolution (e.g., 720)",
  "format": "mp4 or mp3"
}

Response:

{
  "file_name": "Downloaded file name"
}

3. GET /download-file/<file_name>

Serves the downloaded file to the user.


---

Acknowledgements

yt-dlp for simplifying YouTube downloads.

Bootstrap for the frontend design.

YouTube IFrame API for video embedding.



---

License

This project is licensed under the MIT License. See the LICENSE file for details.


---

Disclaimer

This tool is for personal use only. Ensure compliance with YouTube's Terms of Service when downloading videos.


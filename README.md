# 🎬 YouTube Video Downloader API

This is a **simple API built with FastAPI** that uses the [`yt-dlp`](https://github.com/yt-dlp/yt-dlp) library to download YouTube videos. It was created to be used by a React Native mobile app as a way to practice frontend and backend integration.

## ✨ What It Does

* Receives a **YouTube video ID**.
* Uses `yt-dlp` to **download the video in MP4 format**.
* Generates a temporary link so the app can download the video.
* The link is valid for 10 minutes, after which the video is automatically deleted from the server.

## 🔗 Main Endpoints

* `POST /download`: starts downloading a video based on its ID and returns a download link.
* `GET /video/{id}`: serves the video if the link is still valid.

## 📲 Related Project (Frontend)

This backend was developed to be consumed by a React Native mobile app, which you can check out here:

🔗 [daily-diet-app (branch youtube-video-downloader)](https://github.com/newthiagoassisk8/daily-diet-app/tree/youtube-video-downloader)

> **PS:** Yes, the repo name is going through an identity crisis — *it has nothing to do with dieting*.

---

## 🚀 Running the Project

To run this project, make sure you're using **Python 3.11** and have a **virtual environment** activated.

After installing the required dependencies, run the following command:

```bash
uvicorn main:app --host 0.0.0.0 --port 8006
```

This command starts the application using `uvicorn`, making it accessible on all network interfaces (`0.0.0.0`) on port `8006`.

> 💡 Tip: to create and activate a virtual environment, use the commands below:

```bash
python3.11 -m venv venv
source venv/bin/activate  # On Linux/macOS
venv\Scripts\activate     # On Windows
```

Built for learning and experimenting with FastAPI, yt-dlp, and mobile app integration. 🚀

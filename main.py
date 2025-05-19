from fastapi import FastAPI, HTTPException, Request
from fastapi.responses import FileResponse
from pydantic import BaseModel
from datetime import datetime, timedelta
import yt_dlp
import uuid
import os
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()
# TODO: subir isso no docker
# Middleware CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Substitua por domínios específicos em produção
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

DOWNLOAD_DIR = "downloads"
os.makedirs(DOWNLOAD_DIR, exist_ok=True)

video_store = {}
EXPIRATION_MINUTES = 10

class VideoRequest(BaseModel):
    id: str

@app.post("/download")
async def download_video(data: VideoRequest, request: Request):
    video_id_youtube = data.id
    video_url = f"https://www.youtube.com/watch?v={video_id_youtube}"
    local_id = str(uuid.uuid4())

    try:
        with yt_dlp.YoutubeDL({'quiet': True}) as ydl:
            info = ydl.extract_info(video_url, download=False)
            title = info.get("title", local_id).replace(" ", "_")
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Erro ao obter título do vídeo: {str(e)}")

    filename = f"{title}_{local_id}.mp4"
    output_path = os.path.join(DOWNLOAD_DIR, filename)

    ydl_opts = {
        "outtmpl": output_path,
        "format": "bestvideo+bestaudio/best",
        "merge_output_format": "mp4",
        "quiet": True
    }

    try:
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            ydl.download([video_url])
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Erro ao baixar vídeo: {str(e)}")

    video_store[local_id] = {
        "path": output_path,
        "expires_at": datetime.utcnow() + timedelta(minutes=EXPIRATION_MINUTES),
        "filename": filename
    }


    download_url = f"{request.base_url}video/{local_id}"

    return {
        "download_url": download_url,
        "expires_in_minutes": EXPIRATION_MINUTES,
        "title": title
    }

@app.get("/video/{local_id}")
async def get_video(local_id: str):
    video_data = video_store.get(local_id)
    if not video_data:
        raise HTTPException(status_code=404, detail="Vídeo não encontrado ou expirado")

    if datetime.utcnow() > video_data["expires_at"]:
        if os.path.exists(video_data["path"]):
            os.remove(video_data["path"])
        del video_store[local_id]
        raise HTTPException(status_code=410, detail="Link expirado")

    return FileResponse(
        path=video_data["path"],
        media_type="video/mp4",
        filename=video_data["filename"],
        headers={
            "Content-Disposition": f"attachment; filename={video_data['filename']}"
        }
    )

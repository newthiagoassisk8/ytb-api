from fastapi import FastAPI, HTTPException, Request
from fastapi.responses import FileResponse
from pydantic import BaseModel
from datetime import datetime, timedelta
import yt_dlp
import uuid
import os
from fastapi.middleware.cors import CORSMiddleware
import asyncio
from humanize import intword, naturaltime

app = FastAPI()
# TODO: subir isso no docker ss
# Middleware CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

DOWNLOAD_DIR = "downloads"
os.makedirs(DOWNLOAD_DIR, exist_ok=True)

video_store = {}
EXPIRATION_MINUTES = 10

# NOVO: lista de agendamentos em memória
scheduled_downloads = []

class VideoRequest(BaseModel):
    id: str


class ScheduleRequest(BaseModel):
    url: str
    schedule: datetime


async def trigger_download(video_id_youtube: str):
    video_url = f"https://www.youtube.com/watch?v={video_id_youtube}"
    local_id = str(uuid.uuid4())

    try:
        with yt_dlp.YoutubeDL({'quiet': True}) as ydl:
            info = ydl.extract_info(video_url, download=False)
            title = info.get("title", local_id).replace(" ", "_")
    except Exception as e:
        print(f"[Erro título] {e}")
        return

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
        print(f"[Erro download] {e}")
        return

    video_store[local_id] = {
        "path": output_path,
        "expires_at": datetime.utcnow() + timedelta(minutes=EXPIRATION_MINUTES),
        "filename": filename
    }

    print(f"[Download concluído] {filename}")


async def scheduler_loop():
    while True:
        now = datetime.utcnow()
        due_downloads = [d for d in scheduled_downloads if d.schedule <= now]

        for download in due_downloads:
            await trigger_download(download.url)

        scheduled_downloads[:] = [d for d in scheduled_downloads if d.schedule > now]

        await asyncio.sleep(10)


@app.on_event("startup")
async def startup_event():
    asyncio.create_task(scheduler_loop())

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


@app.post("/schedule")
async def schedule_video(data: ScheduleRequest):
    if data.schedule <= datetime.utcnow():
        raise HTTPException(status_code=400, detail="Agendamento deve ser no futuro")
    scheduled_downloads.append(data)
    return {"message": f"Download agendado para {data.schedule}"}

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

@app.get("/video-info/{video_id}")
async def get_video_info(video_id: str):

    url = f"https://www.youtube.com/watch?v={video_id}"

    ydl_opts = {
        "quiet": True,
        "skip_download": True,
        "force_generic_extractor": False,
    }

    try:
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            info = ydl.extract_info(url, download=False)

        # Formata data
        upload_date_str = info.get("upload_date")
        if upload_date_str:
            upload_date = datetime.strptime(upload_date_str, "%Y%m%d")
            created_at = naturaltime(datetime.now() - upload_date)
        else:
            created_at = "data desconhecida"

        # Formata views
        view_count = info.get("view_count", 0)
        formatted_views = f"{intword(view_count)} views"

        return {
            "src": info.get("thumbnail"),
            "title": info.get("title"),
            "channel": info.get("uploader"),
            "views": formatted_views,
            "createdAt": created_at,
        }

    except Exception as e:
        raise HTTPException(status_code=400, detail=f"Erro ao buscar informações do vídeo: {str(e)}")

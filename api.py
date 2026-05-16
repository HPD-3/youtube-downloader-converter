from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import FileResponse
import os
from os.path import basename, exists
from pydantic import BaseModel
from typing import List, Optional
import youtube_downloader
import file_converter

class DownloadRequest(BaseModel):
    url: str
    resolution: Optional[str] = "360"


class DownloadVideosRequest(BaseModel):
    urls: List[str]
    resolution: Optional[str] = "360"


class PlaylistRequest(BaseModel):
    url: str
    resolution: Optional[str] = "360"


class ConvertRequest(BaseModel):
    filename: str


app = FastAPI(title="YouTube Downloader Converter API")

allowed_origins = [
    origin.strip()
    for origin in os.getenv(
        "CORS_ORIGINS",
        "https://webconverter-c3376.web.app,http://localhost:3000,http://localhost:5173",
    ).split(",")
    if origin.strip()
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=allowed_origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
    expose_headers=["Content-Disposition", "X-Download-Filename"],
)


@app.get("/health")
def health():
    return {"status": "ok"}


@app.post("/download/video")
def download_video(req: DownloadRequest):
    try:
        filename = youtube_downloader.download_video(req.url, req.resolution)
        return {"filename": filename}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.post("/download/videos")
def download_videos(req: DownloadVideosRequest):
    try:
        filenames = []
        for url in req.urls:
            filenames.append(youtube_downloader.download_video(url, req.resolution))
        return {"filenames": filenames}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.post("/download/playlist")
def download_playlist(req: PlaylistRequest):
    try:
        youtube_downloader.download_playlist(req.url, req.resolution)
        return {"message": "Playlist download started/completed"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.post("/convert/mp3")
def convert_to_mp3(req: ConvertRequest):
    try:
        mp3_filename = file_converter.convert_to_mp3(req.filename)
        return {"mp3_filename": basename(mp3_filename)}
    except RuntimeError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.post("/download/convert")
def download_and_convert(req: DownloadRequest):
    try:
        fname = youtube_downloader.download_video(req.url, req.resolution)
        mp3_filename = file_converter.convert_to_mp3(fname)
        return {"filename": fname, "mp3": mp3_filename}
    except RuntimeError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.post("/download/video/file")
def download_video_file(req: DownloadRequest):
    try:
        fname = youtube_downloader.download_video(req.url, req.resolution)
        if not os.path.exists(fname):
            raise HTTPException(status_code=500, detail="Downloaded file not found")
        download_name = os.path.basename(fname)
        return FileResponse(
            path=fname,
            media_type="video/mp4",
            filename=download_name,
            headers={"X-Download-Filename": download_name},
        )
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.post("/download/convert/file")
def download_and_convert_file(req: DownloadRequest):
    try:
        fname = youtube_downloader.download_video(req.url, req.resolution)
        mp3 = file_converter.convert_to_mp3(fname)
        if not exists(mp3):
            raise HTTPException(status_code=500, detail="Converted file not found")
        download_name = basename(mp3)
        return FileResponse(
            path=mp3,
            media_type="audio/mpeg",
            filename=download_name,
            headers={"X-Download-Filename": download_name},
        )
    except RuntimeError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.post("/convert/file")
def convert_and_return_file(req: ConvertRequest):
    try:
        if not os.path.exists(req.filename):
            raise HTTPException(status_code=400, detail="Source file not found")
        mp3 = file_converter.convert_to_mp3(req.filename)
        if not os.path.exists(mp3):
            raise HTTPException(status_code=500, detail="Converted file not found")
        download_name = os.path.basename(mp3)
        return FileResponse(
            path=mp3,
            media_type="audio/mpeg",
            filename=download_name,
            headers={"X-Download-Filename": download_name},
        )
    except RuntimeError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


if __name__ == "__main__":
    import uvicorn

    uvicorn.run("api:app", host="0.0.0.0", port=8000, reload=True)

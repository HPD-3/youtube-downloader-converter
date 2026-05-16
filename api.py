from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import FileResponse
import os
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
        file_converter.convert_to_mp3(req.filename)
        return {"mp3_filename": req.filename[:-4] + ".mp3"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.post("/download/convert")
def download_and_convert(req: DownloadRequest):
    try:
        fname = youtube_downloader.download_video(req.url, req.resolution)
        file_converter.convert_to_mp3(fname)
        return {"filename": fname, "mp3": fname[:-4] + ".mp3"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.post("/download/video/file")
def download_video_file(req: DownloadRequest):
    try:
        fname = youtube_downloader.download_video(req.url, req.resolution)
        if not os.path.exists(fname):
            raise HTTPException(status_code=500, detail="Downloaded file not found")
        return FileResponse(path=fname, media_type="video/mp4", filename=os.path.basename(fname))
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.post("/download/convert/file")
def download_and_convert_file(req: DownloadRequest):
    try:
        fname = youtube_downloader.download_video(req.url, req.resolution)
        mp3 = fname[:-4] + ".mp3"
        file_converter.convert_to_mp3(fname)
        if not os.path.exists(mp3):
            raise HTTPException(status_code=500, detail="Converted file not found")
        return FileResponse(path=mp3, media_type="audio/mpeg", filename=os.path.basename(mp3))
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.post("/convert/file")
def convert_and_return_file(req: ConvertRequest):
    try:
        if not os.path.exists(req.filename):
            raise HTTPException(status_code=400, detail="Source file not found")
        mp3 = req.filename[:-4] + ".mp3"
        file_converter.convert_to_mp3(req.filename)
        if not os.path.exists(mp3):
            raise HTTPException(status_code=500, detail="Converted file not found")
        return FileResponse(path=mp3, media_type="audio/mpeg", filename=os.path.basename(mp3))
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


if __name__ == "__main__":
    import uvicorn

    uvicorn.run("api:app", host="0.0.0.0", port=8000, reload=True)

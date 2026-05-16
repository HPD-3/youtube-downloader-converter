from fastapi import FastAPI, HTTPException
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


if __name__ == "__main__":
    import uvicorn

    uvicorn.run("api:app", host="0.0.0.0", port=8000, reload=True)

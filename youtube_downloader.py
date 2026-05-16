try:
    from yt_dlp import YoutubeDL
except ImportError as exc:
    raise ImportError(
        "yt-dlp is required to download videos. Install it with 'pip install yt-dlp'."
    ) from exc


def _resolution_height(resolution):
    if resolution in ["low", "360", "360p"]:
        return 360
    if resolution in ["medium", "720", "720p", "hd"]:
        return 720
    if resolution in ["high", "1080", "1080p", "fullhd", "full_hd", "full hd"]:
        return 1080
    if resolution in ["very high", "2160", "2160p", "4K", "4k"]:
        return 2160
    return 360


def _download(url, resolution, playlist=False):
    downloaded_filename = None

    def capture_downloaded_filename(data):
        nonlocal downloaded_filename
        if data.get("status") == "finished":
            downloaded_filename = data.get("filepath") or data.get("filename")

    options = {
        "format": f"best[height<={_resolution_height(resolution)}][ext=mp4]/best[ext=mp4]/best",
        "noplaylist": not playlist,
        "outtmpl": "%(title)s.%(ext)s",
        "quiet": True,
        "progress_hooks": [capture_downloaded_filename],
    }

    with YoutubeDL(options) as downloader:
        downloader.download([url])

    if not downloaded_filename:
        raise RuntimeError("Could not determine the downloaded file name.")

    return downloaded_filename


def download_video(url, resolution):
    return _download(url, resolution)


def download_videos(urls, resolution):
    for url in urls:
        download_video(url, resolution)


def download_playlist(url, resolution):
    _download(url, resolution, playlist=True)


def input_links():
    print("Enter the links of the videos (end by entering 'STOP'):")

    links = []
    link = ""

    while link != "STOP" and link != "stop":
        link = input()
        links.append(link)

    links.pop()

    return links
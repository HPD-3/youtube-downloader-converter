try:
    from yt_dlp import YoutubeDL
except ImportError as exc:
    raise ImportError(
        "yt-dlp is required to download videos. Install it with 'pip install yt-dlp'."
    ) from exc


def _title_template():
    return "%(title).200s.%(ext)s"


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
    downloaded_title = None

    def capture_downloaded_filename(data):
        nonlocal downloaded_filename, downloaded_title
        if data.get("status") == "finished":
            downloaded_filename = data.get("filepath") or data.get("filename")
            downloaded_title = data.get("info_dict", {}).get("title")

    def build_filename_from_title(info_dict):
        title = info_dict.get("title") or "downloaded_video"
        ext = info_dict.get("ext") or "mp4"
        return f"{title[:200]}.{ext}"

    options = {
        "format": f"best[height<={_resolution_height(resolution)}][ext=mp4]/best[ext=mp4]/best",
        "noplaylist": not playlist,
        "outtmpl": _title_template(),
        "quiet": True,
        "progress_hooks": [capture_downloaded_filename],
    }

    with YoutubeDL(options) as downloader:
        info = downloader.extract_info(url, download=True)

    if downloaded_title and downloaded_filename:
        return build_filename_from_title({"title": downloaded_title, "ext": downloaded_filename.rsplit(".", 1)[-1]})

    if info:
        return build_filename_from_title(info)

    if downloaded_filename:
        return downloaded_filename

    raise RuntimeError("Could not determine the downloaded file name.")


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
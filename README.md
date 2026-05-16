# youtube-downloader-converter
A simple Python script that is able to download YouTube videos or playlists and convert them into MP3.

## Requirements

Install the runtime dependencies before launching the app:

```bash
pip install yt-dlp moviepy
```

If you are running the FastAPI app directly, also install the API dependencies from `requirements.txt`.

The backend now reads allowed browser origins from `CORS_ORIGINS`. For deployment, set it to a comma-separated list such as:

```bash
CORS_ORIGINS=https://webconverter-c3376.web.app,http://localhost:3000
```

MoviePy also needs FFmpeg available on your system path for MP3 conversion.

Copyright (c) HPD-3 2026 - 

WARNING: DOWNLOADING COPYRIGHTED MATERIAL IS HIGHLY ILLEGAL!
I DO NOT TAKE ANY RESPONSIBILITY FOR YOUR USAGE OF THIS TOOL!
THIS IS FOR EDUCATIONAL PURPOSES ONLY!

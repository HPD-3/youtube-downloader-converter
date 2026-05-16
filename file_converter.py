import os
import shutil
import subprocess


def convert_to_mp3(filename):
    output_filename = os.path.splitext(filename)[0] + ".mp3"
    ffmpeg = shutil.which("ffmpeg")

    if not ffmpeg:
        raise RuntimeError("FFmpeg is not available on the server.")

    command = [
        ffmpeg,
        "-y",
        "-i",
        filename,
        "-vn",
        "-codec:a",
        "libmp3lame",
        "-q:a",
        "2",
        output_filename,
    ]

    result = subprocess.run(command, capture_output=True, text=True)
    if result.returncode != 0:
        error_message = result.stderr.strip() or result.stdout.strip() or "Unknown FFmpeg conversion error."
        raise RuntimeError(error_message)

    return output_filename
import os

try:
    from moviepy import VideoFileClip
except ImportError:
    from moviepy.editor import VideoFileClip

def convert_to_mp3(filename):
    output_filename = os.path.splitext(filename)[0] + ".mp3"
    clip = VideoFileClip(filename)
    try:
        if clip.audio is None:
            raise RuntimeError("The downloaded file does not contain an audio track.")
        clip.audio.write_audiofile(output_filename)
    finally:
        clip.close()

    return output_filename
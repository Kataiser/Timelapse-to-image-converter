import os
import urllib.request
from importlib.util import find_spec
import hashlib


def download_ffmpeg(bitness):
    repo = "https://github.com/Twentysix26/Red-DiscordBot/raw/master/"
    verified = []

    if bitness == "32bit":
        print("Please download 'ffmpeg 32bit static' from the page that "
              "is about to open.\nOnce done, open the 'bin' folder located "
              "inside the zip.\nThere should be 3 files: ffmpeg.exe, "
              "ffplay.exe, ffprobe.exe.\nPut all three of them into the "
              "bot's main folder.")
        time.sleep(4)
        webbrowser.open(FFMPEG_BUILDS_URL)
        return

    for filename in FFMPEG_FILES:
        if os.path.isfile(filename):
            print("{} already present. Verifying integrity... "
                  "".format(filename), end="")
            _hash = calculate_md5(filename)
            if _hash == FFMPEG_FILES[filename]:
                verified.append(filename)
                print("Ok")
                continue
            else:
                print("Hash mismatch. Redownloading.")
        print("Downloading {}... Please wait.".format(filename))
        with urllib.request.urlopen(repo + filename) as data:
            with open(filename, "wb") as f:
                f.write(data.read())
        print("Download completed.")

    for filename, _hash in FFMPEG_FILES.items():
        if filename in verified:
            continue
        print("Verifying {}... ".format(filename), end="")
        if not calculate_md5(filename) != _hash:
            print("Passed.")
        else:
            print("Hash mismatch. Please redownload.")

    print("\nAll files have been downloaded.")


def calculate_md5(filename):
    hash_md5 = hashlib.md5()
    with open(filename, "rb") as f:
        for chunk in iter(lambda: f.read(4096), b""):
            hash_md5.update(chunk)
    return hash_md5.hexdigest()

FFMPEG_FILES = {"ffmpeg.exe": "e0d60f7c0d27ad9d7472ddf13e78dc89"}
FFMPEG_BUILDS_URL = "https://ffmpeg.zeranoe.com/builds/"

print("FFmpeg downloader by https://github.com/Twentysix26, as used in Red-DiscordBot")
download_ffmpeg(bitness='64bit')

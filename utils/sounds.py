import winsound
import os

BASE_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
SOUNDS_DIR = os.path.join(BASE_DIR, "sounds")


def play(sound_name: str):
    path = os.path.join(SOUNDS_DIR, sound_name)
    if os.path.exists(path):
        winsound.PlaySound(path, winsound.SND_FILENAME | winsound.SND_ASYNC)

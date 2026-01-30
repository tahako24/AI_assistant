import pvporcupine
import pyaudio
import struct
import winsound

from utils.voice import listen, speak
from core.router import route
from local_actions.system import handle_local
from agents.api_client import ask_llm
from memory.memory import remember, recall

# 🔑 Picovoice
ACCESS_KEY = "rfbuD+YTxl1XdBa6mhNhsOfEIolZ+0uG0I3o0XtSuXvyqT/TK/I2Aw=="
KEYWORD_PATH = "wake_words/novara.ppn"


def beep():
    winsound.Beep(1200, 120)


def start_nova():
    print("🤖 Novara запущена (wake word)")

    porcupine = pvporcupine.create(
        access_key=ACCESS_KEY,
        keyword_paths=[KEYWORD_PATH]
    )

    pa = pyaudio.PyAudio()
    stream = pa.open(
        rate=porcupine.sample_rate,
        channels=1,
        format=pyaudio.paInt16,
        input=True,
        frames_per_buffer=porcupine.frame_length
    )

    try:
        while True:
            pcm = stream.read(
                porcupine.frame_length,
                exception_on_overflow=False
            )
            pcm = struct.unpack_from(
                "h" * porcupine.frame_length,
                pcm
            )

            if porcupine.process(pcm) >= 0:
                # 🔔 wake word услышано
                beep()
                speak("Слушаю")

                # 🎙️ слушаем команду
                text = listen()
                if not text:
                    continue

                action = route(text)

                if action == "local":
                    handle_local(text)
                else:
                    try:
                        answer = ask_llm(text)
                        speak(answer)
                    except Exception:
                        speak("Ошибка соединения")

    finally:
        stream.stop_stream()
        stream.close()
        pa.terminate()
        porcupine.delete()

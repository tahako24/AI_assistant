import sounddevice as sd
import wavio
import pyttsx3
from faster_whisper import WhisperModel
import numpy as np

# ─── НАСТРОЙКИ ─────────────────────────────
SAMPLE_RATE = 16000
RECORD_SECONDS = 4
WAV_PATH = "input.wav"

# ─── TTS ──────────────────────────────────
engine = pyttsx3.init()
engine.setProperty("rate", 165)

def speak(text: str):
    print(f"🧠 Ассистент: {text}")
    engine.say(text)
    engine.runAndWait()

# ─── WHISPER ──────────────────────────────
print("🧠 Загружаю модель Whisper...")
whisper_model = WhisperModel(
    "small",
    device="cpu",
    compute_type="int8"
)
print("✅ Whisper готов")

# ─── LISTEN ───────────────────────────────
def listen() -> str | None:
    print("🎤 Слушаю...")

    try:
        recording = sd.rec(
            int(RECORD_SECONDS * SAMPLE_RATE),
            samplerate=SAMPLE_RATE,
            channels=1,
            dtype="int16"
        )
        sd.wait()
        wavio.write(WAV_PATH, recording, SAMPLE_RATE, sampwidth=2)
    except Exception as e:
        print("MIC ERROR:", e)
        speak("Ошибка микрофона")
        return None

    segments, _ = whisper_model.transcribe(
        WAV_PATH,
        language="ru",
        beam_size=5
    )

    text = "".join(seg.text for seg in segments).strip()

    if not text:
        return None

    print(f"👤 Ты сказала: {text}")
    return text.lower()

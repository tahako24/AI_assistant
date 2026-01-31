import pvporcupine
import pyaudio
import struct
import winsound

from ui.popup import show_popup
from utils.logger import log_info, log_error
from core.tray import enabled
from utils.voice import listen, speak
from core.router import route
from local_actions.system import handle_local
from agents.api_client import ask_llm
from memory.memory import remember, recall
from core.tray import enabled
from ui.popup import show_popup
from ui.popup_manager import show_text


ACCESS_KEY = "rfbuD+YTxl1XdBa6mhNhsOfEIolZ+0uG0I3o0XtSuXvyqT/TK/I2Aw=="
KEYWORD_PATH = "wake_words/novara.ppn"


def beep():
    winsound.Beep(1200, 120)

def find_mic_index(keyword="microphone"):
    pa = pyaudio.PyAudio()
    selected = None

    print("🎧 Доступные микрофоны:")
    for i in range(pa.get_device_count()):
        info = pa.get_device_info_by_index(i)
        if info["maxInputChannels"] > 0:
            print(f"  [{i}] {info['name']}")
            name = info["name"].lower()
            if keyword.lower() in name and selected is None:
                selected = i

    pa.terminate()

    if selected is not None:
        print(f"🎤 Использую микрофон: {selected}")
    else:
        print("⚠️ Микрофон по ключевому слову не найден, используется дефолтный")

    return selected


def start_nova():
    log_info("Novara запущена (wake word)")

    porcupine = pvporcupine.create(
        access_key=ACCESS_KEY,
        keyword_paths=[KEYWORD_PATH]
    )

    pa = pyaudio.PyAudio()

    mic_index = find_mic_index("chu2")
    log_info(f"Используется микрофон index={mic_index}")

    stream = pa.open(
        rate=porcupine.sample_rate,
        channels=1,
        format=pyaudio.paInt16,
        input=True,
        input_device_index=mic_index,
        frames_per_buffer=porcupine.frame_length
    )

    try:
        while True:
            pcm = stream.read(
                porcupine.frame_length,
                exception_on_overflow=False
            )
            pcm = struct.unpack_from(
                "h" * porcupine.frame_length, pcm
            )

            if porcupine.process(pcm) >= 0:
                log_info("Wake word услышан")

                if not enabled:
                    log_info("Novara выключена — игнорирую wake word")
                    continue

                beep()
                speak("Слушаю")

                text = listen()
                if not text:
                    log_info("Команда не распознана")
                    continue

                log_info(f"Команда пользователя: {text}")

                # 🪟 ВОТ СЮДА ↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓
                if "закрой окно" in text or "закрой экран" in text:
                    close_popup()
                    speak("Закрыла")
                    log_info("Popup закрыт голосовой командой")
                    continue
                # 🪟 ДО ЭТОГО МЕСТА ↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑

                action = route(text)

                if action == "local":
                    handle_local(text)

                else:
                    try:
                        log_info("Отправляю запрос в LLM")
                        answer = ask_llm(text)

                        log_info(f"Ответ LLM получен ({len(answer)} символов)")
                        log_info(f"Ответ LLM: {answer[:200]}")

                        speak(answer)
                        show_text(answer)

                        log_info("Popup вызван")
                    except Exception as e:
                        log_error(f"Ошибка LLM: {e}")
                        speak("Ошибка соединения")

    except Exception as e:
        log_error(f"Критическая ошибка wake word loop: {e}")

    finally:
        log_info("Завершение Novara")
        stream.stop_stream()
        stream.close()
        pa.terminate()
        porcupine.delete()

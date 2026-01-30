import keyboard
import os
import threading
import time

from core.router import route
from local_actions.system import handle_local
from agents.api_client import ask_llm
from utils.voice import listen, speak


def start_hotkeys():
    state = {
        "assistant_enabled": False,
        "recording": False,
    }

    listen_thread = None

    # ─────────────────────────────
    # ВКЛ / ВЫК ассистента
    # ─────────────────────────────
    def toggle_assistant():
        state["assistant_enabled"] = not state["assistant_enabled"]
        status = "включён" if state["assistant_enabled"] else "выключен"
        print(f"🤖 Ассистент {status}")
        speak(f"Ассистент {status}")

    # ─────────────────────────────
    # НАЧАЛО ЗАПИСИ (Ctrl+Shift DOWN)
    # ─────────────────────────────
    def start_recording():
        if not state["assistant_enabled"]:
            return
        if state["recording"]:
            return

        state["recording"] = True
        print("🎤 Запись началась")
        speak("Слушаю")

        def record():
            text = listen()

            if not text:
                speak("Не расслышала")
            else:
                action = route(text)

                if action == "local":
                    handle_local(text)
                else:
                    try:
                        answer = ask_llm(text)
                        speak(answer)
                    except Exception:
                        speak("Ошибка соединения")

            state["recording"] = False

        nonlocal listen_thread
        listen_thread = threading.Thread(target=record, daemon=True)
        listen_thread.start()

    # ─────────────────────────────
    # ОТПУСКАНИЕ КЛАВИШ
    # ─────────────────────────────
    def stop_recording():
        # listen() сам завершится — здесь просто защита
        pass

    # ─────────────────────────────
    # ВЫХОД
    # ─────────────────────────────
    def exit_program():
        print("👋 Выход из программы")
        os._exit(0)

    # ─────────────────────────────
    # ГОРЯЧИЕ КЛАВИШИ
    # ─────────────────────────────
    keyboard.add_hotkey("ctrl+f1", toggle_assistant)
    keyboard.add_hotkey("ctrl+f2", exit_program)

    keyboard.add_hotkey(
        "ctrl+shift",
        start_recording,
        trigger_on_release=False
    )

    keyboard.add_hotkey(
        "ctrl+shift",
        stop_recording,
        trigger_on_release=True
    )

    print("⌨️ Горячие клавиши активны:")
    print("   ▶ Ctrl + F1     — включить / выключить ассистента")
    print("   ▶ Ctrl + Shift  — удерживать для записи")
    print("   ▶ Ctrl + F2     — выход")

    keyboard.wait()  # ⛔ никаких while True

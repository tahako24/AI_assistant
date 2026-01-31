from core.tray import run_tray
from core.wake_word import start_nova
import threading


def main():
    print("AI assistant running in background ✅")

    threading.Thread(
        target=start_nova,
        daemon=True
    ).start()

    run_tray()


if __name__ == "__main__":
    main()

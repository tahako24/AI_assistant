import os

BASE_DIR = os.path.abspath(
    os.path.join(os.path.dirname(__file__), "..")
)

PROGRAMS_DIR = os.path.join(BASE_DIR, "programs")


def run_shortcut_contains(keyword: str) -> bool:
    for file in os.listdir(PROGRAMS_DIR):
        if file.lower().endswith(".lnk") and keyword.lower() in file.lower():
            path = os.path.join(PROGRAMS_DIR, file)
            os.startfile(path)
            return True
    return False


def handle_local(text: str):
    text = text.lower()

    # 📝 Блокнот
    if "блокнот" in text or "notepad" in text:
        os.startfile("notepad.exe")
        print("🖥️ Открываю блокнот")
        return

    # 🌐 Браузер / Chrome
    if any(w in text for w in ["браузер", "броузер", "chrome", "хром"]):
        if run_shortcut_contains("chrome"):
            print("🌐 Открываю браузер")
            return

    # 💬 Discord
    if any(w in text for w in ["discord", "дискорд"]):
        if run_shortcut_contains("discord"):
            print("💬 Открываю Discord")
            return

    # 🎨 Figma
    if any(w in text for w in ["figma", "фигма"]):
        if run_shortcut_contains("figma"):
            print("🎨 Открываю Figma")
            return

    # 🎮 Steam
    if any(w in text for w in ["steam", "стим"]):
        if run_shortcut_contains("steam"):
            print("🎮 Открываю Steam")
            return

    # 🧱 Minecraft / Legacy Launcher
    if any(w in text for w in ["minecraft", "майнкрафт", "legacy"]):
        if run_shortcut_contains("legacy"):
            print("🧱 Запускаю Minecraft")
            return

    # 🧠 Visual Studio
    if any(w in text for w in ["visual studio", "visual", "студию"]):
        if run_shortcut_contains("visual"):
            print("🧠 Открываю Visual Studio")
            return

    # 🟢 NVIDIA App
    if any(w in text for w in ["nvidia", "нвидиа"]):
        if run_shortcut_contains("nvidia"):
            print("🟢 Открываю NVIDIA App")
            return

    print("⚠️ Локальная команда не распознана")

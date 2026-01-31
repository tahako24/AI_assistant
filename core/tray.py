import pystray
from pystray import MenuItem as item
from PIL import Image
import os
import sys

from utils.logger import log_info

enabled = True


def status_text():
    return "🟢 Включена" if enabled else "🔴 Выключена"


def toggle_enable(icon, _):
    global enabled
    enabled = not enabled
    log_info(f"Статус изменён: {'включена' if enabled else 'выключена'}")
    icon.notify("Novara", status_text())
    icon.update_menu()


def restart_app(icon, _):
    log_info("Перезапуск Novara")
    os.execv(sys.executable, [sys.executable] + sys.argv)


def open_log(icon, _):
    log_info("Открыт лог-файл")
    log_path = os.path.abspath(
        os.path.join(os.path.dirname(__file__), "..", "logs", "novara.log")
    )
    os.startfile(log_path)


def on_exit(icon, _):
    log_info("Выход из Novara")
    icon.stop()
    os._exit(0)


def run_tray():
    image = Image.open(
        os.path.join(os.path.dirname(__file__), "..", "assets", "novara.png")
    )

    menu = pystray.Menu(
        item(lambda _: status_text(), None, enabled=False),
        item("Включить / Выключить", toggle_enable),
        item("🔄 Перезапустить", restart_app),
        item("📄 Открыть лог", open_log),
        item("❌ Выход", on_exit),
    )

    icon = pystray.Icon(
        "Novara",
        image,
        "Novara Assistant",
        menu
    )

    log_info("Tray запущен")
    icon.run()
import pystray
from pystray import MenuItem as item
from PIL import Image
import os
import sys

from utils.logger import log_info

enabled = True


def status_text():
    return "🟢 Включена" if enabled else "🔴 Выключена"


def toggle_enable(icon, _):
    global enabled
    enabled = not enabled
    log_info(f"Статус изменён: {'включена' if enabled else 'выключена'}")
    icon.notify("Novara", status_text())
    icon.update_menu()


def restart_app(icon, _):
    log_info("Перезапуск Novara")
    os.execv(sys.executable, [sys.executable] + sys.argv)


def open_log(icon, _):
    log_info("Открыт лог-файл")
    log_path = os.path.abspath(
        os.path.join(os.path.dirname(__file__), "..", "logs", "novara.log")
    )
    os.startfile(log_path)


def on_exit(icon, _):
    log_info("Выход из Novara")
    icon.stop()
    os._exit(0)


def run_tray():
    image = Image.open(
        os.path.join(os.path.dirname(__file__), "..", "assets", "novara.png")
    )

    menu = pystray.Menu(
        item(lambda _: status_text(), None, enabled=False),
        item("Включить / Выключить", toggle_enable),
        item("🔄 Перезапустить", restart_app),
        item("📄 Открыть лог", open_log),
        item("❌ Выход", on_exit),
    )

    icon = pystray.Icon(
        "Novara",
        image,
        "Novara Assistant",
        menu
    )

    log_info("Tray запущен")
    icon.run()

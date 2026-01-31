import subprocess
import sys
import os


def show_popup(text: str):
    popup_script = os.path.join(
        os.path.dirname(__file__),
        "popup_window.py"
    )

    subprocess.Popen(
        [
            sys.executable,
            popup_script,
            text
        ],
        creationflags=subprocess.CREATE_NEW_PROCESS_GROUP
    )

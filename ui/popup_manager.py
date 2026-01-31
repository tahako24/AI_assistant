import tkinter as tk
from tkinter.scrolledtext import ScrolledText
import threading
import queue

# ====== QUEUE ДЛЯ ОБНОВЛЕНИЙ ======
_ui_queue = queue.Queue()

# ====== UI STATE ======
_root = None
_text_area = None

# ====== COLORS ======
BG = "#1e1e1e"
FG = "#e6e6e6"
ACCENT = "#3a8bfd"
BTN_BG = "#2d2d2d"
BTN_FG = "#ffffff"


def _process_queue():
    """Обрабатывает входящие сообщения для UI"""
    try:
        while True:
            text = _ui_queue.get_nowait()
            _text_area.config(state="normal")
            _text_area.delete("1.0", tk.END)
            _text_area.insert(tk.END, text)
            _text_area.config(state="disabled")
            _root.deiconify()
            _root.lift()
    except queue.Empty:
        pass

    _root.after(100, _process_queue)


def _run_ui():
    global _root, _text_area

    _root = tk.Tk()
    _root.title("Novara")
    _root.geometry("620x400")
    _root.configure(bg=BG)
    _root.attributes("-topmost", True)

    header = tk.Label(
        _root,
        text="🧠 Novara",
        bg=BG,
        fg=ACCENT,
        font=("Segoe UI", 11, "bold")
    )
    header.pack(anchor="w", padx=12, pady=(10, 4))

    _text_area = ScrolledText(
        _root,
        wrap=tk.WORD,
        bg=BG,
        fg=FG,
        insertbackground=FG,
        font=("Segoe UI", 10),
        relief=tk.FLAT
    )
    _text_area.pack(expand=True, fill="both", padx=12, pady=6)
    _text_area.config(state="disabled")

    btn = tk.Button(
        _root,
        text="Закрыть",
        bg=BTN_BG,
        fg=BTN_FG,
        activebackground=ACCENT,
        activeforeground="white",
        relief=tk.FLAT,
        padx=12,
        pady=5,
        command=_root.withdraw
    )
    btn.pack(pady=(0, 12))

    _root.after(100, _process_queue)
    _root.mainloop()


def show_text(text: str):
    # Кладём текст в очередь
    _ui_queue.put(text)

    # Если UI ещё не запущен — запускаем ОДИН РАЗ
    if _root is None:
        threading.Thread(target=_run_ui, daemon=True).start()

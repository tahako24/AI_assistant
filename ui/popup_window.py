import tkinter as tk
from tkinter.scrolledtext import ScrolledText
import sys

text = sys.argv[1] if len(sys.argv) > 1 else ""

root = tk.Tk()
root.title("Novara")
root.geometry("560x360")
root.attributes("-topmost", True)

area = ScrolledText(
    root,
    wrap=tk.WORD,
    font=("Segoe UI", 10)
)
area.pack(expand=True, fill="both", padx=10, pady=10)

area.insert(tk.END, text)
area.config(state=tk.NORMAL)

btn = tk.Button(
    root,
    text="Закрыть",
    command=root.destroy
)
btn.pack(pady=(0, 10))

root.mainloop()

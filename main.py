# main.py
import tkinter as tk
from secure_media_app import SecureMediaApp

if __name__ == "__main__":
    root = tk.Tk()
    app = SecureMediaApp(root)
    root.mainloop()

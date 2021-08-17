import tkinter as tk
from tkinter import filedialog
from cinegrade.process import process_video


def run():
    root = tk.Tk()
    root.withdraw()
    file_paths = filedialog.askopenfilenames()
    if file_paths:
        for file_path in file_paths:
            process_video(file_path, 600)
    else:
        print("Exiting...")

import os
import platform
import subprocess
from tkinter import filedialog, messagebox

def open_folder_in_explorer(folder_path: str):
    """Cross-platform helper to open a directory path in the OS file manager."""
    if not folder_path or not os.path.exists(folder_path):
        os.makedirs(folder_path, exist_ok=True)

    system = platform.system()
    try:
        if system == "Windows":
            os.startfile(folder_path)
        elif system == "Darwin":  # macOS
            subprocess.run(["open", folder_path], check=True)
        else:  # Linux / Unix
            subprocess.run(["xdg-open", folder_path], check=True)
    except Exception as e:
        messagebox.showerror("Error", f"Could not open directory:\n{folder_path}\n\nError: {e}")

def browse_directory_dialog(initial_dir=""):
    """Opens a native directory picker dialog."""
    return filedialog.askdirectory(initialdir=initial_dir if os.path.exists(initial_dir) else None)

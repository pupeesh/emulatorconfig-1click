import os
import sys
import shutil
import subprocess
import tkinter as tk
from tkinter import ttk, messagebox
from datetime import datetime

IS_WINDOWS = sys.platform.startswith("win")

# --- Target Configuration Directories (Multi-Path Fallback Search) ---
if IS_WINDOWS:
    APPDATA = os.environ.get("APPDATA", "")
    LOCALAPPDATA = os.environ.get("LOCALAPPDATA", "")
    USERPROFILE = os.environ.get("USERPROFILE", "")

    EMULATOR_POSSIBLE_PATHS = {
        "Cemu": [
            os.path.join(APPDATA, "Cemu"),
            os.path.join(LOCALAPPDATA, "Cemu"),
            "C:\\Cemu", "D:\\Cemu"
        ],
        "Dolphin": [
            os.path.join(APPDATA, "Dolphin Emulator"),
            os.path.join(USERPROFILE, "Documents", "Dolphin Emulator")
        ],
        "PCSX2": [
            os.path.join(USERPROFILE, "Documents", "PCSX2"),
            os.path.join(APPDATA, "PCSX2")
        ],
        "PPSSPP": [
            os.path.join(USERPROFILE, "Documents", "PPSSPP", "PSP", "SYSTEM"),
            os.path.join(APPDATA, "PPSSPP", "PSP", "SYSTEM")
        ]
    }
    SCRIPTS = {
        "Cemu": "cemu-settings.ps1",
        "Dolphin": "dolphin-settings.ps1",
        "PCSX2": "pcsx2-settings.ps1",
        "PPSSPP": "ppsspp-settings.ps1"
    }
else:
    HOME = os.environ.get("HOME", "")
    EMULATOR_POSSIBLE_PATHS = {
        "Cemu": [
            os.path.expanduser("~/.config/Cemu"),
            os.path.expanduser("~/.var/app/info.cemu.Cemu/config/Cemu")
        ],
        "Dolphin": [
            os.path.expanduser("~/.config/dolphin-emu"),
            os.path.expanduser("~/.var/app/org.dolphin_emu.dolphin-emu/config/dolphin-emu")
        ],
        "PCSX2": [
            os.path.expanduser("~/.config/PCSX2"),
            os.path.expanduser("~/.var/app/net.pcsx2.PCSX2/config/PCSX2")
        ],
        "PPSSPP": [
            os.path.expanduser("~/.config/ppsspp/PSP/SYSTEM"),
            os.path.expanduser("~/.var/app/org.ppsspp.PPSSPP/config/ppsspp/PSP/SYSTEM")
        ]
    }
    SCRIPTS = {
        "Cemu": "cemu-settings.sh",
        "Dolphin": "dolphin-settings.sh",
        "PCSX2": "pcsx2-settings.sh",
        "PPSSPP": "ppsspp-settings.sh"
    }

def get_emulator_dir(emu_name):
    """Find and return the first valid existing configuration directory."""
    paths = EMULATOR_POSSIBLE_PATHS.get(emu_name, [])
    for path in paths:
        if os.path.exists(path):
            return path
    # Return default primary path if none exist yet
    return paths[0] if paths else ""

def is_emulator_detected(emu_name):
    """Check if any target config folder exists on the system."""
    paths = EMULATOR_POSSIBLE_PATHS.get(emu_name, [])
    return any(os.path.exists(p) for p in paths)

def run_script(emu_name):
    """Run the custom configurator script located inside the scripts/ subfolder silently."""
    script_filename = SCRIPTS.get(emu_name)
    script_path = os.path.join(os.path.dirname(__file__), "scripts", script_filename)

    if not os.path.exists(script_path):
        messagebox.showerror("Error", f"Script file not found:\n{script_path}")
        return

    try:
        if IS_WINDOWS:
            startupinfo = subprocess.STARTUPINFO()
            startupinfo.dwFlags |= subprocess.STARTF_USESHOWWINDOW
            cmd = ["powershell.exe", "-ExecutionPolicy", "Bypass", "-File", script_path]
            
            result = subprocess.run(
                cmd, 
                capture_output=True, 
                text=True, 
                creationflags=subprocess.CREATE_NO_WINDOW,
                startupinfo=startupinfo
            )
        else:
            os.chmod(script_path, 0o755)
            cmd = ["/bin/bash", script_path]
            result = subprocess.run(cmd, capture_output=True, text=True)

        if result.returncode == 0:
            messagebox.showinfo("Success", f"{emu_name} config applied successfully!\n\n{result.stdout}")
        else:
            messagebox.showerror("Script Error", f"Failed to execute {emu_name} script:\n\n{result.stderr}")

        refresh_statuses()

    except Exception as e:
        messagebox.showerror("Error", f"Execution error:\n{str(e)}")

def reset_to_default(emu_name):
    """Backup existing config folder and safely clear specific main configuration files."""
    config_dir = get_emulator_dir(emu_name)

    if not os.path.exists(config_dir):
        messagebox.showwarning("Warning", f"{emu_name} directory not found at:\n{config_dir}")
        return

    confirm = messagebox.askyesno(
        "Reset Confirmation", 
        f"Are you sure you want to reset {emu_name} settings?\n\nA backup will be saved before clearing configuration files."
    )
    if not confirm:
        return

    try:
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        backup_dir = f"{config_dir}_backup_{timestamp}"
        shutil.copytree(config_dir, backup_dir)

        # Target specific configuration files instead of deleting all INI/XMLs
        target_files = ["settings.xml", "Dolphin.ini", "GFX.ini", "PCSX2.ini", "ppsspp.ini", "controls.ini"]
        
        for root_dir, _, files in os.walk(config_dir):
            for file in files:
                if file in target_files or "Profile" in root_dir:
                    os.remove(os.path.join(root_dir, file))

        messagebox.showinfo(
            "Defaults Restored", 
            f"Successfully reset {emu_name}!\n\nBackup created at:\n{backup_dir}"
        )
        refresh_statuses()
    except Exception as e:
        messagebox.showerror("Reset Failed", f"Could not reset settings:\n{str(e)}")

# --- GUI Construction ---
root = tk.Tk()
root.title("Emulator Config Manager")
root.geometry("520x360")
root.resizable(False, False)

title_label = ttk.Label(root, text="Emulator Management Console", font=("Segoe UI", 12, "bold"))
title_label.pack(pady=(15, 2))

os_text = "Windows (PowerShell Mode)" if IS_WINDOWS else "Linux (Bash Mode)"
os_label = ttk.Label(root, text=f"Platform: {os_text}", font=("Segoe UI", 9, "italic"))
os_label.pack(pady=(0, 15))

header_frame = ttk.Frame(root)
header_frame.pack(fill="x", padx=20, pady=(0, 5))
ttk.Label(header_frame, text="Emulator", font=("Segoe UI", 9, "bold"), width=12).grid(row=0, column=0, sticky="w")
ttk.Label(header_frame, text="Status", font=("Segoe UI", 9, "bold"), width=14).grid(row=0, column=1, sticky="w")
ttk.Label(header_frame, text="Actions", font=("Segoe UI", 9, "bold")).grid(row=0, column=2, sticky="w")

separator = ttk.Separator(root, orient="horizontal")
separator.pack(fill="x", padx=20, pady=5)

status_labels = {}

def refresh_statuses():
    """Dynamically refresh detection indicators."""
    for emu_name, label in status_labels.items():
        detected = is_emulator_detected(emu_name)
        label.config(
            text="✔ Config Found" if detected else "✖ Not Detected",
            fg="green" if detected else "gray"
        )

# Build rows dynamically
for emu_name in SCRIPTS.keys():
    row = ttk.Frame(root)
    row.pack(fill="x", padx=20, pady=6)

    name_label = ttk.Label(row, text=emu_name, font=("Segoe UI", 10), width=12)
    name_label.grid(row=0, column=0, sticky="w")

    status_label = tk.Label(row, width=14, anchor="w", font=("Segoe UI", 9))
    status_label.grid(row=0, column=1, sticky="w")
    status_labels[emu_name] = status_label

    apply_btn = ttk.Button(
        row, 
        text="Apply Config", 
        command=lambda e=emu_name: run_script(e)
    )
    apply_btn.grid(row=0, column=2, padx=5)

    reset_btn = ttk.Button(
        row, 
        text="Reset Defaults", 
        command=lambda e=emu_name: reset_to_default(e)
    )
    reset_btn.grid(row=0, column=3, padx=5)

refresh_statuses()
root.mainloop()
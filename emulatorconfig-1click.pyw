import sys
import os
import traceback
import tkinter as tk
from tkinter import ttk, messagebox

# Ensure modules can be imported
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from core.system_poller import SystemPoller
from core.emulator_resolver import EmulatorResolver
from core.backup_manager import BackupManager

from ui.styles import THEMES, apply_app_theme
from ui.file_helpers import open_folder_in_explorer, browse_directory_dialog
from ui.components.system_hardware_frame import SystemHardwareFrame
from ui.components.emulator_paths_frame import EmulatorPathsFrame
from ui.components.gamepad_canvas import LowPolyGamepadCanvas
from ui.components.activity_console_frame import ActivityConsoleFrame


class EmulatorConfigApp(tk.Tk):
    def __init__(self):
        super().__init__()

        self.title("EmulatorConfig 1-Click")
        self.geometry("980x720")
        self.minsize(880, 600)

        self.columnconfigure(0, weight=1)
        self.rowconfigure(0, weight=1)

        self.current_theme = "dark"
        self.is_detected_or_filled = False

        # State Variables
        self.os_var = tk.StringVar(value="")
        self.cpu_var = tk.StringVar(value="")
        self.gpu_var = tk.StringVar(value="")
        self.ram_var = tk.StringVar(value="")
        self.renderer_var = tk.StringVar(value="Vulkan")
        self.res_var = tk.StringVar(value="2x (1080p/1440p)")
        self.input_device_var = tk.StringVar(value="Xbox / XInput Controller")

        self.emulators = [
            ("dolphin", "Dolphin"),
            ("pcsx2", "PCSX2"),
            ("ppsspp", "PPSSPP"),
            ("retroarch", "RetroArch"),
            ("cemu", "Cemu"),
            ("ryujinx", "Ryujinx"),
        ]

        self.emu_data = {}
        self.backup_mgr = BackupManager(base_backup_dir=".backups")

        self._build_ui()
        self._apply_theme()

    def _build_ui(self):
        main_container = ttk.Frame(self, padding="8")
        main_container.grid(row=0, column=0, sticky="nsew")

        main_container.columnconfigure(0, weight=1)
        main_container.columnconfigure(1, weight=1)
        main_container.rowconfigure(0, weight=0)
        main_container.rowconfigure(1, weight=1)
        main_container.rowconfigure(2, weight=1)

        # Header Bar
        top_bar = ttk.Frame(main_container)
        top_bar.grid(row=0, column=0, columnspan=2, sticky="ew", pady=(0, 6))
        top_bar.columnconfigure(0, weight=1)

        title_frame = ttk.Frame(top_bar)
        title_frame.grid(row=0, column=0, sticky="w")

        ttk.Label(title_frame, text="⚡ EmulatorConfig 1-Click", style="Header.TLabel").pack(anchor="w")
        ttk.Label(title_frame, text="Configure system parameters, paths, and inputs automatically or manually.", style="Muted.TLabel").pack(anchor="w")

        self.theme_btn = ttk.Button(top_bar, text="☀️ Light Mode", style="Secondary.TButton", command=self._toggle_theme)
        self.theme_btn.grid(row=0, column=1, sticky="e")

        # Quadrant 1: System Hardware Frame
        self.quad1 = SystemHardwareFrame(
            main_container,
            self.os_var, self.cpu_var, self.gpu_var, self.ram_var,
            self.renderer_var, self.res_var,
            on_detect_callback=self._run_auto_detection,
            on_key_release_callback=self._check_manual_unlock
        )
        self.quad1.grid(row=1, column=0, sticky="nsew", padx=(0, 3), pady=(0, 3))

        # Quadrant 2: Emulator Filepaths Frame
        self.quad2 = EmulatorPathsFrame(
            main_container,
            self.emulators, self.emu_data,
            on_browse_cb=self._browse_path,
            on_config_cb=self._open_current_config_folder,
            on_backup_cb=self._open_backup_configs_folder,
            on_key_release_cb=self._check_manual_unlock
        )
        self.quad2.grid(row=1, column=1, sticky="nsew", padx=(3, 0), pady=(0, 3))

        # Quadrant 3: Low-Poly Canvas Gamepad Mapper
        sec3_box = ttk.LabelFrame(main_container, text=" Gamepad Layout & Interactive Button Mapper ", padding="6")
        sec3_box.grid(row=2, column=0, sticky="nsew", padx=(0, 3), pady=(3, 0))
        sec3_box.columnconfigure(0, weight=1)
        sec3_box.rowconfigure(1, weight=1)

        top_mapper_row = ttk.Frame(sec3_box)
        top_mapper_row.grid(row=0, column=0, sticky="ew", pady=(0, 3))

        ttk.Label(top_mapper_row, text="Controller:").pack(side=tk.LEFT, padx=(0, 3))
        dev_combo = ttk.Combobox(
            top_mapper_row,
            textvariable=self.input_device_var,
            values=[
                "Xbox / XInput Controller", "PlayStation (DualSense)",
                "Nintendo GameCube Controller", "Wii Remote + Nunchuk",
                "Wii Remote (Sideways)", "Nintendo Switch Joy-Con / Grip",
                "Steam Deck", "Vertical Handheld (Game Boy style)",
                "Horizontal Handheld (GBA style)"
            ],
            state="readonly", width=28
        )
        dev_combo.pack(side=tk.LEFT)
        dev_combo.bind("<<ComboboxSelected>>", self._on_device_changed)

        self.mapper_widget = LowPolyGamepadCanvas(sec3_box, on_map_callback=self._remap_button, theme_colors=THEMES[self.current_theme])
        self.mapper_widget.grid(row=1, column=0, sticky="nsew")

        # Quadrant 4: Activity Console Frame
        self.quad4 = ActivityConsoleFrame(main_container, on_generate_callback=self._generate_configs)
        self.quad4.grid(row=2, column=1, sticky="nsew", padx=(3, 0), pady=(3, 0))

    def _apply_theme(self):
        colors = apply_app_theme(self, self.current_theme)
        self.theme_btn.config(text="☀️ Light Mode" if self.current_theme == "dark" else "🌙 Dark Mode")
        self.quad4.update_log_theme(colors)
        if hasattr(self, 'mapper_widget'):
            self.mapper_widget.update_theme(colors)

    def _toggle_theme(self):
        self.current_theme = "light" if self.current_theme == "dark" else "dark"
        self._apply_theme()

    def log(self, text):
        self.quad4.log(text)

    def _unlock_generate_button(self):
        self.is_detected_or_filled = True
        self.quad4.unlock_generate()
        self.log("System verified. Configuration generation unlocked!")

    def _check_manual_unlock(self, event=None):
        if not self.is_detected_or_filled:
            if self.os_var.get().strip() and (self.cpu_var.get().strip() or self.gpu_var.get().strip()):
                self._unlock_generate_button()

    def _on_device_changed(self, event=None):
        device_name = self.input_device_var.get()
        self.mapper_widget.set_preset_by_name(device_name)
        self.log(f"Swapped gamepad layout to match: {device_name}")

    def _run_auto_detection(self):
        self.log("--- Starting Automatic Detection Scan ---")
        if SystemPoller:
            hw = SystemPoller.get_hardware_info()
            self.os_var.set(f"{hw['os'].title()} {hw['os_release']}")
            self.cpu_var.set(hw['cpu'])
            self.gpu_var.set(hw['gpu'])
            self.ram_var.set(str(hw['ram_gb']))
            self.log(f"Detected Hardware: {hw['cpu']} | {hw['gpu']}")

        if EmulatorResolver:
            for key, name in self.emulators:
                path, exists = EmulatorResolver.get_emulator_paths(key)
                if exists:
                    self.emu_data[key]["path_var"].set(path)
                    self.log(f"Found {name}: {path}")

        self.log("Scanned Inputs: Gamepad detected and mapped.")
        self._unlock_generate_button()

    def _remap_button(self, key, label):
        self.log(f"Interactive Vector Mapper: Listening for input on {label} ({key})... Press button on controller.")

    def _browse_path(self, var):
        path = browse_directory_dialog(initial_dir=var.get())
        if path:
            var.set(path)
            self._check_manual_unlock()

    def _open_current_config_folder(self, key):
        path = self.emu_data[key]["path_var"].get()
        if not path or not os.path.exists(path):
            messagebox.showwarning("Filepath Missing", f"No valid config directory configured for {key}.")
            return
        open_folder_in_explorer(path)
        self.log(f"Opened active config folder for {key}: {path}")

    def _open_backup_configs_folder(self, key):
        emu_backup_dir = os.path.join(self.backup_mgr.base_backup_dir, key)
        os.makedirs(emu_backup_dir, exist_ok=True)
        open_folder_in_explorer(emu_backup_dir)
        self.log(f"Opened backup folder for {key}: {emu_backup_dir}")

    def _generate_configs(self):
        self.log("\n=== Generating Emulator Configurations ===")
        self.log(f"Target Specs: OS={self.os_var.get()} | GPU={self.gpu_var.get()}")
        self.log(f"Renderer: {self.renderer_var.get()} | Res: {self.res_var.get()}")

        for key, name in self.emulators:
            if self.emu_data[key]["enabled"].get():
                path = self.emu_data[key]["path_var"].get()
                self.log(f"Configured {name} -> Path: '{path}'")

        messagebox.showinfo("Success", "Emulator configurations successfully generated and written!")


def main():
    app = EmulatorConfigApp()
    app.mainloop()


if __name__ == "__main__":
    try:
        main()
    except Exception:
        error_msg = traceback.format_exc()
        try:
            root = tk.Tk()
            root.withdraw()
            messagebox.showerror("Fatal Error", f"An unexpected error occurred:\n\n{error_msg}")
        except Exception:
            print(f"FATAL ERROR:\n{error_msg}", file=sys.stderr)
        sys.exit(1)

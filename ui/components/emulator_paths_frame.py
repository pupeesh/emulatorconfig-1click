import tkinter as tk
from tkinter import ttk

class EmulatorPathsFrame(ttk.LabelFrame):
    """Quadrant 2: Emulator Filepaths, Browse, Current Config, and Backup Configs Buttons."""

    def __init__(self, parent, emulators, emu_data, on_browse_cb, on_config_cb, on_backup_cb, on_key_release_cb, **kwargs):
        super().__init__(parent, text=" Emulator Filepaths & Configuration Files ", padding="6", **kwargs)

        self.emulators = emulators
        self.emu_data = emu_data
        self.on_browse_cb = on_browse_cb
        self.on_config_cb = on_config_cb
        self.on_backup_cb = on_backup_cb
        self.on_key_release_cb = on_key_release_cb

        self.columnconfigure(0, weight=1)
        self.rowconfigure(0, weight=1)
        self._build_ui()

    def _build_ui(self):
        self.canvas = tk.Canvas(self, highlightthickness=0)
        scroll = ttk.Scrollbar(self, orient="vertical", command=self.canvas.yview)
        scroll_frame = ttk.Frame(self.canvas)

        scroll_frame.bind("<Configure>", lambda e: self.canvas.configure(scrollregion=self.canvas.bbox("all")))
        c_win = self.canvas.create_window((0, 0), window=scroll_frame, anchor="nw")
        self.canvas.bind("<Configure>", lambda e: self.canvas.itemconfig(c_win, width=e.width))
        self.canvas.configure(yscrollcommand=scroll.set)

        self.canvas.grid(row=0, column=0, sticky="nsew")
        scroll.grid(row=0, column=1, sticky="ns")
        scroll_frame.columnconfigure(0, weight=1)

        for idx, (key, name) in enumerate(self.emulators):
            card = ttk.Frame(scroll_frame, style="Card.TFrame", padding="4")
            card.grid(row=idx, column=0, sticky="ew", pady=2)
            card.columnconfigure(1, weight=1)

            path_var = tk.StringVar(value="")
            chk_var = tk.BooleanVar(value=True)

            self.emu_data[key] = {
                "enabled": chk_var,
                "path_var": path_var
            }

            ttk.Checkbutton(card, text=name, variable=chk_var, width=10).grid(row=0, column=0, sticky="w", padx=(0, 2))

            p_entry = ttk.Entry(card, textvariable=path_var)
            p_entry.grid(row=0, column=1, sticky="ew", padx=2)
            p_entry.bind("<KeyRelease>", self.on_key_release_cb)

            btn_frame = ttk.Frame(card, style="Card.TFrame")
            btn_frame.grid(row=0, column=2, sticky="e", padx=(2, 0))

            ttk.Button(btn_frame, text="Browse", style="Secondary.TButton", command=lambda v=path_var: self.on_browse_cb(v)).pack(side=tk.LEFT, padx=1)
            ttk.Button(btn_frame, text="Current config", style="Secondary.TButton", command=lambda k=key: self.on_config_cb(k)).pack(side=tk.LEFT, padx=1)
            ttk.Button(btn_frame, text="Backup configs", style="Secondary.TButton", command=lambda k=key: self.on_backup_cb(k)).pack(side=tk.LEFT, padx=1)

    def update_canvas_bg(self, bg_color):
        """Updates internal canvas background to match dark/light theme."""
        if hasattr(self, 'canvas'):
            self.canvas.configure(bg=bg_color)

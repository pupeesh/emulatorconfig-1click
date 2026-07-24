import tkinter as tk
from tkinter import ttk, scrolledtext

class ActivityConsoleFrame(ttk.LabelFrame):
    """Quadrant 4: Activity Log Console & Primary Config Generation Button."""

    def __init__(self, parent, on_generate_callback, **kwargs):
        super().__init__(parent, text=" Actions & Activity Console ", padding="6", **kwargs)

        self.on_generate_callback = on_generate_callback
        self.columnconfigure(0, weight=1)
        self.rowconfigure(0, weight=1)

        self._build_ui()

    def _build_ui(self):
        self.log_box = scrolledtext.ScrolledText(self, font=("Consolas", 8), bd=0)
        self.log_box.grid(row=0, column=0, sticky="nsew", pady=(0, 6))

        self.btn_generate = ttk.Button(
            self,
            text="Generate Configurations",
            style="Primary.TButton",
            state="disabled",
            command=self.on_generate_callback
        )
        self.btn_generate.grid(row=1, column=0, sticky="ew")

    def log(self, text):
        self.log_box.insert(tk.END, f"{text}\n")
        self.log_box.see(tk.END)

    def unlock_generate(self):
        self.btn_generate.config(state="normal", text="Generate Configurations")

    def update_log_theme(self, theme_colors):
        self.log_box.configure(
            bg=theme_colors["log_bg"],
            fg=theme_colors["log_fg"],
            insertbackground=theme_colors["fg"]
        )

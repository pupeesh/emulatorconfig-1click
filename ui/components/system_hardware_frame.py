from tkinter import ttk

class SystemHardwareFrame(ttk.LabelFrame):
    """Quadrant 1: System Specs, Graphics API, and Auto-Detect Button."""

    def __init__(self, parent, os_var, cpu_var, gpu_var, ram_var, renderer_var, res_var, on_detect_callback, on_key_release_callback, **kwargs):
        super().__init__(parent, text=" System Hardware & Classification ", padding="6", **kwargs)

        self.os_var = os_var
        self.cpu_var = cpu_var
        self.gpu_var = gpu_var
        self.ram_var = ram_var
        self.renderer_var = renderer_var
        self.res_var = res_var
        self.on_detect_callback = on_detect_callback
        self.on_key_release_callback = on_key_release_callback

        self.columnconfigure(0, weight=1)
        self._build_ui()

    def _build_ui(self):
        grid = ttk.Frame(self)
        grid.grid(row=0, column=0, sticky="ew")
        grid.columnconfigure(1, weight=1)

        fields = [
            ("Operating System:", self.os_var, 0),
            ("CPU Processor:", self.cpu_var, 1),
            ("GPU Graphics:", self.gpu_var, 2),
            ("RAM Memory (GB):", self.ram_var, 3),
        ]

        for label_text, var, row in fields:
            ttk.Label(grid, text=label_text).grid(row=row, column=0, sticky="w", padx=2, pady=2)
            entry = ttk.Entry(grid, textvariable=var)
            entry.grid(row=row, column=1, sticky="ew", padx=2, pady=2)
            entry.bind("<KeyRelease>", self.on_key_release_callback)

        pref_frame = ttk.Frame(self)
        pref_frame.grid(row=1, column=0, sticky="ew", pady=(4, 0))
        pref_frame.columnconfigure(1, weight=1)

        ttk.Label(pref_frame, text="Graphics API:").grid(row=0, column=0, sticky="w", padx=2, pady=2)
        ttk.Combobox(pref_frame, textvariable=self.renderer_var, values=["Vulkan", "OpenGL", "Direct3D 11", "Direct3D 12", "Metal"], state="readonly", width=12).grid(row=0, column=1, sticky="ew", padx=2, pady=2)

        ttk.Label(pref_frame, text="Target Res:").grid(row=1, column=0, sticky="w", padx=2, pady=2)
        ttk.Combobox(pref_frame, textvariable=self.res_var, values=["1x (Native/720p)", "2x (1080p/1440p)", "3x (3K/4K)"], state="readonly", width=12).grid(row=1, column=1, sticky="ew", padx=2, pady=2)

        btn_auto = ttk.Button(self, text="🔍 Automatic Detection Scan", style="Success.TButton", command=self.on_detect_callback)
        btn_auto.grid(row=2, column=0, sticky="ew", pady=(6, 0))

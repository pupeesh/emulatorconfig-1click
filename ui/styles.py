from tkinter import ttk

THEMES = {
    "dark": {
        "bg": "#11111b",             # Deep base dark
        "card_bg": "#1e1e2e",        # Surface layer background
        "fg": "#cdd6f4",             # High contrast primary text
        "muted": "#a6adc8",          # Secondary/muted label text
        "accent": "#89b4fa",         # Vivid blue accent
        "green": "#a6e3a1",          # Success button green
        "entry_bg": "#313244",       # Solid dark input field background
        "entry_border": "#45475a",   # Input border stroke
        "log_bg": "#181825",         # Console background
        "log_fg": "#a6e3a1"          # Terminal green output text
    },
    "light": {
        "bg": "#eff1f5",
        "card_bg": "#e6e9ef",
        "fg": "#4c4f69",
        "muted": "#6c6f85",
        "accent": "#1e66f5",
        "green": "#40a02b",
        "entry_bg": "#ffffff",
        "entry_border": "#bcc0cc",
        "log_bg": "#dce0e8",
        "log_fg": "#40a02b"
    }
}

def apply_app_theme(root, current_theme):
    """Configures colors, fonts, and widget states across all TTK widgets for Dark or Light mode."""
    c = THEMES[current_theme]
    root.configure(bg=c["bg"])

    style = ttk.Style(root)
    style.theme_use("clam")

    # Global TTK defaults
    style.configure(".", background=c["bg"], foreground=c["fg"], font=("Segoe UI", 9))
    style.configure("TFrame", background=c["bg"])
    style.configure("Card.TFrame", background=c["card_bg"], relief="flat")

    # Section LabelFrames
    style.configure("TLabelframe", background=c["bg"], foreground=c["accent"], bordercolor=c["entry_border"])
    style.configure("TLabelframe.Label", background=c["bg"], foreground=c["accent"], font=("Segoe UI", 9, "bold"))

    # Typography
    style.configure("Header.TLabel", font=("Segoe UI", 14, "bold"), foreground=c["accent"], background=c["bg"])
    style.configure("Muted.TLabel", font=("Segoe UI", 8), foreground=c["muted"], background=c["bg"])
    style.configure("CardText.TLabel", background=c["card_bg"], foreground=c["fg"], font=("Segoe UI", 8))

    # Checkbuttons
    style.configure("TCheckbutton", background=c["card_bg"], foreground=c["fg"], font=("Segoe UI", 9))
    style.map("TCheckbutton", background=[("active", c["card_bg"])])

    # Text Entry Fields
    style.configure(
        "TEntry",
        fieldbackground=c["entry_bg"],
        foreground=c["fg"],
        bordercolor=c["entry_border"],
        lightcolor=c["entry_border"],
        darkcolor=c["entry_border"],
        insertcolor=c["fg"]
    )

    # Combobox Override (Fixes the ugly grey read-only dropdowns)
    style.configure(
        "TCombobox",
        fieldbackground=c["entry_bg"],
        background=c["entry_bg"],
        foreground=c["fg"],
        bordercolor=c["entry_border"],
        arrowcolor=c["fg"]
    )
    style.map(
        "TCombobox",
        fieldbackground=[("readonly", c["entry_bg"]), ("focus", c["entry_bg"]), ("active", c["entry_bg"])],
        background=[("readonly", c["entry_bg"]), ("focus", c["entry_bg"]), ("active", c["entry_bg"])],
        foreground=[("readonly", c["fg"]), ("focus", c["fg"]), ("active", c["fg"])],
        arrowcolor=[("readonly", c["fg"]), ("focus", c["fg"]), ("active", c["fg"])]
    )

    # Primary Action Button
    style.configure("Primary.TButton", font=("Segoe UI", 9, "bold"), background=c["accent"], foreground="#11111b")
    style.map("Primary.TButton", background=[("active", "#b4befe"), ("disabled", c["entry_bg"])], foreground=[("disabled", c["muted"])])

    # Success / Auto-Detect Button
    style.configure("Success.TButton", font=("Segoe UI", 9, "bold"), background=c["green"], foreground="#11111b")
    style.map("Success.TButton", background=[("active", "#94e2d5")])

    # Secondary Small Utility Buttons
    style.configure("Secondary.TButton", font=("Segoe UI", 8), background=c["entry_bg"], foreground=c["fg"], bordercolor=c["entry_border"], padding=2)
    style.map("Secondary.TButton", background=[("active", c["card_bg"])], foreground=[("active", c["accent"])])

    # Options menu popdown listbox color fix
    root.option_add("*TCombobox*Listbox.background", c["entry_bg"])
    root.option_add("*TCombobox*Listbox.foreground", c["fg"])
    root.option_add("*TCombobox*Listbox.selectBackground", c["accent"])
    root.option_add("*TCombobox*Listbox.selectForeground", "#11111b")

    return c

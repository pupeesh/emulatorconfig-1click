from tkinter import ttk

THEMES = {
    "dark": {
        "bg": "#181825",
        "card_bg": "#1e1e2e",
        "fg": "#cdd6f4",
        "muted": "#a6adc8",
        "accent": "#89b4fa",
        "green": "#a6e3a1",
        "entry_bg": "#313244",
        "log_bg": "#11111b",
        "log_fg": "#a6e3a1"
    },
    "light": {
        "bg": "#eff1f5",
        "card_bg": "#e6e9ef",
        "fg": "#4c4f69",
        "muted": "#6c6f85",
        "accent": "#1e66f5",
        "green": "#40a02b",
        "entry_bg": "#ffffff",
        "log_bg": "#dce0e8",
        "log_fg": "#40a02b"
    }
}

def apply_app_theme(root, current_theme):
    """Configures colors and fonts across all TTK widgets for Dark or Light mode."""
    c = THEMES[current_theme]
    root.configure(bg=c["bg"])

    style = ttk.Style(root)
    style.theme_use("clam")

    style.configure(".", background=c["bg"], foreground=c["fg"], font=("Segoe UI", 9))
    style.configure("TFrame", background=c["bg"])
    style.configure("Card.TFrame", background=c["card_bg"], relief="flat")
    style.configure("TLabelframe", background=c["bg"], foreground=c["accent"])
    style.configure("TLabelframe.Label", background=c["bg"], foreground=c["accent"], font=("Segoe UI", 9, "bold"))

    style.configure("Header.TLabel", font=("Segoe UI", 14, "bold"), foreground=c["accent"], background=c["bg"])
    style.configure("Muted.TLabel", font=("Segoe UI", 8), foreground=c["muted"], background=c["bg"])
    style.configure("CardText.TLabel", background=c["card_bg"], foreground=c["fg"], font=("Segoe UI", 8))

    style.configure("TCheckbutton", background=c["card_bg"], foreground=c["fg"], font=("Segoe UI", 9))
    style.map("TCheckbutton", background=[("active", c["card_bg"])])

    style.configure("TEntry", fieldbackground=c["entry_bg"], foreground=c["fg"])
    style.configure("TCombobox", fieldbackground=c["entry_bg"], foreground=c["fg"])

    style.configure("Primary.TButton", font=("Segoe UI", 9, "bold"), background=c["accent"], foreground="#ffffff")
    style.map("Primary.TButton", background=[("active", c["accent"]), ("disabled", c["muted"])])

    style.configure("Success.TButton", font=("Segoe UI", 9, "bold"), background=c["green"], foreground="#ffffff")
    style.map("Success.TButton", background=[("active", c["green"])])

    style.configure("Secondary.TButton", font=("Segoe UI", 7), background=c["entry_bg"], foreground=c["fg"], padding=1)
    style.map("Secondary.TButton", background=[("active", c["card_bg"])])

    return c

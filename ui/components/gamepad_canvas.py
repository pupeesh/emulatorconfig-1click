import tkinter as tk
from tkinter import ttk

class LowPolyGamepadCanvas(ttk.Frame):
    """Draws clean low-poly vector silhouettes with mathematically centered text labels and dynamic bindings."""

    def __init__(self, parent, on_map_callback, theme_colors, **kwargs):
        super().__init__(parent, **kwargs)
        self.on_map_callback = on_map_callback
        self.theme_colors = theme_colors
        self.current_preset = "xbox"
        self.interactive_elements = []
        self.hovered_element = None
        self.listening_key = None
        self.bindings = {}

        self.canvas = tk.Canvas(self, bg=self.theme_colors["card_bg"], highlightthickness=0)
        self.canvas.pack(fill=tk.BOTH, expand=True)

        self.canvas.bind("<Motion>", self._on_mouse_move)
        self.canvas.bind("<Button-1>", self._on_mouse_click)

        self.draw_gamepad()

    def update_theme(self, theme_colors):
        self.theme_colors = theme_colors
        self.canvas.configure(bg=self.theme_colors["card_bg"])
        self.draw_gamepad()

    def update_bindings(self, new_bindings):
        """Updates active hardware bindings."""
        self.bindings = new_bindings
        self.draw_gamepad()

    def set_listening_state(self, key):
        """Highlights the active button when awaiting hardware input."""
        self.listening_key = key
        self.draw_gamepad()

    def set_preset_by_name(self, name):
        n = name.lower()
        if "wii" in n and "nunchuk" in n:
            self.current_preset = "wii_nunchuk"
        elif "wii" in n and "sideways" in n:
            self.current_preset = "wii_sideways"
        elif "gamecube" in n:
            self.current_preset = "gamecube"
        elif "dualsense" in n or "ps" in n or "playstation" in n:
            self.current_preset = "ps"
        elif "joycon" in n or "switch" in n:
            self.current_preset = "switch"
        elif "deck" in n or "steam" in n:
            self.current_preset = "steamdeck"
        elif "vertical" in n or ("anbernic" in n and "gb" in n):
            self.current_preset = "handheld_vertical"
        elif "horizontal" in n or "handheld" in n:
            self.current_preset = "handheld_horizontal"
        else:
            self.current_preset = "xbox"
        self.draw_gamepad()

    def draw_gamepad(self):
        """Redraws vector silhouettes with pixel-centered alignment."""
        self.canvas.delete("all")
        self.interactive_elements.clear()

        poly_color = self.theme_colors["entry_bg"]
        outline_color = self.theme_colors["accent"]
        btn_bg = self.theme_colors["bg"]
        text_fg = self.theme_colors["fg"]

        p = self.current_preset

        # 1. XBOX / XINPUT
        if p == "xbox":
            body = [(100, 50), (340, 50), (390, 80), (430, 140), (390, 220), (330, 220), (280, 160), (160, 160), (110, 220), (50, 220), (10, 140), (50, 80)]
            self.canvas.create_polygon(body, fill=poly_color, outline=outline_color, width=2)

            self._draw_rect(60, 22, 110, 42, "L2", "LT", btn_bg, text_fg, outline_color)
            self._draw_rect(120, 25, 170, 45, "L1", "LB", btn_bg, text_fg, outline_color)
            self._draw_rect(270, 25, 320, 45, "R1", "RB", btn_bg, text_fg, outline_color)
            self._draw_rect(330, 22, 380, 42, "R2", "RT", btn_bg, text_fg, outline_color)

            self._draw_circle(90, 85, 16, "LS", "LS", btn_bg, text_fg, outline_color)
            self._draw_circle(310, 140, 16, "RS", "RS", btn_bg, text_fg, outline_color)

            self._draw_circle(115, 125, 9, "DPAD_UP", "▲", btn_bg, text_fg, outline_color, font_size=7)
            self._draw_circle(98, 140, 9, "DPAD_LEFT", "◄", btn_bg, text_fg, outline_color, font_size=7)
            self._draw_circle(132, 140, 9, "DPAD_RIGHT", "►", btn_bg, text_fg, outline_color, font_size=7)
            self._draw_circle(115, 155, 9, "DPAD_DOWN", "▼", btn_bg, text_fg, outline_color, font_size=7)

            self._draw_circle(350, 70, 10, "Y", "Y", btn_bg, text_fg, outline_color)
            self._draw_circle(330, 88, 10, "X", "X", btn_bg, text_fg, outline_color)
            self._draw_circle(370, 88, 10, "B", "B", btn_bg, text_fg, outline_color)
            self._draw_circle(350, 106, 10, "A", "A", btn_bg, text_fg, outline_color)

            self._draw_rect(184, 100, 220, 118, "SELECT", "Back", btn_bg, text_fg, outline_color, font_size=6)
            self._draw_rect(224, 100, 260, 118, "START", "Start", btn_bg, text_fg, outline_color, font_size=6)

        # 2. PLAYSTATION
        elif p == "ps":
            body = [(100, 50), (340, 50), (390, 80), (430, 140), (390, 220), (330, 220), (280, 160), (160, 160), (110, 220), (50, 220), (10, 140), (50, 80)]
            self.canvas.create_polygon(body, fill=poly_color, outline=outline_color, width=2)
            self.canvas.create_rectangle(180, 58, 260, 95, outline=self.theme_colors["muted"], width=1)

            self._draw_rect(60, 22, 110, 42, "L2", "L2", btn_bg, text_fg, outline_color)
            self._draw_rect(120, 25, 170, 45, "L1", "L1", btn_bg, text_fg, outline_color)
            self._draw_rect(270, 25, 320, 45, "R1", "R1", btn_bg, text_fg, outline_color)
            self._draw_rect(330, 22, 380, 42, "R2", "R2", btn_bg, text_fg, outline_color)

            self._draw_circle(170, 135, 16, "LS", "L3", btn_bg, text_fg, outline_color)
            self._draw_circle(270, 135, 16, "RS", "R3", btn_bg, text_fg, outline_color)

            self._draw_circle(90, 75, 9, "DPAD_UP", "▲", btn_bg, text_fg, outline_color, font_size=7)
            self._draw_circle(73, 90, 9, "DPAD_LEFT", "◄", btn_bg, text_fg, outline_color, font_size=7)
            self._draw_circle(107, 90, 9, "DPAD_RIGHT", "►", btn_bg, text_fg, outline_color, font_size=7)
            self._draw_circle(90, 105, 9, "DPAD_DOWN", "▼", btn_bg, text_fg, outline_color, font_size=7)

            self._draw_circle(350, 72, 10, "Y", "△", btn_bg, text_fg, outline_color)
            self._draw_circle(332, 90, 10, "X", "□", btn_bg, text_fg, outline_color)
            self._draw_circle(368, 90, 10, "B", "○", btn_bg, text_fg, outline_color)
            self._draw_circle(350, 108, 10, "A", "✕", btn_bg, text_fg, outline_color)

            self._draw_rect(138, 65, 176, 81, "SELECT", "Share", btn_bg, text_fg, outline_color, font_size=6)
            self._draw_rect(264, 65, 302, 81, "START", "Opts", btn_bg, text_fg, outline_color, font_size=6)

        # 3. GAMECUBE
        elif p == "gamecube":
            body = [(100, 50), (340, 50), (380, 80), (410, 180), (350, 220), (280, 170), (160, 170), (90, 220), (30, 180), (60, 80)]
            self.canvas.create_polygon(body, fill=poly_color, outline=outline_color, width=2)

            self._draw_rect(70, 22, 120, 42, "L1", "L", btn_bg, text_fg, outline_color)
            self._draw_rect(320, 22, 370, 42, "R1", "R", btn_bg, text_fg, outline_color)
            self._draw_rect(295, 46, 345, 58, "Z", "Z", btn_bg, text_fg, outline_color)

            self._draw_circle(100, 85, 19, "LS", "Stick", btn_bg, text_fg, outline_color, font_size=6)
            self._draw_circle(315, 135, 17, "RS", "C-Stk", btn_bg, text_fg, outline_color, font_size=6)

            self._draw_circle(135, 135, 8, "DPAD_UP", "▲", btn_bg, text_fg, outline_color, font_size=6)
            self._draw_circle(122, 148, 8, "DPAD_LEFT", "◄", btn_bg, text_fg, outline_color, font_size=6)
            self._draw_circle(148, 148, 8, "DPAD_RIGHT", "►", btn_bg, text_fg, outline_color, font_size=6)
            self._draw_circle(135, 161, 8, "DPAD_DOWN", "▼", btn_bg, text_fg, outline_color, font_size=6)

            self._draw_circle(345, 90, 14, "A", "A", btn_bg, text_fg, outline_color)
            self._draw_circle(320, 98, 9, "B", "B", btn_bg, text_fg, outline_color)
            self._draw_circle(345, 68, 9, "Y", "Y", btn_bg, text_fg, outline_color)
            self._draw_circle(372, 88, 9, "X", "X", btn_bg, text_fg, outline_color)

            self._draw_circle(220, 105, 12, "START", "Start", btn_bg, text_fg, outline_color, font_size=6)

        # 4. WII REMOTE + NUNCHUK
        elif p == "wii_nunchuk":
            nunchuk_curved = [(90, 45), (105, 48), (118, 58), (124, 75), (122, 105), (112, 140), (98, 175), (90, 195), (82, 175), (68, 140), (58, 105), (56, 75), (62, 58), (75, 48)]
            self.canvas.create_polygon(nunchuk_curved, fill=poly_color, outline=outline_color, width=2, smooth=True)
            self.canvas.create_oval(74, 55, 106, 87, outline=self.theme_colors["muted"], width=1)
            self._draw_circle(90, 71, 15, "LS", "Stick", btn_bg, text_fg, outline_color, font_size=6)

            self._draw_rect(65, 25, 115, 40, "C", "C", btn_bg, text_fg, outline_color)
            self._draw_rect(65, 5, 115, 20, "Z", "Z", btn_bg, text_fg, outline_color)
            self.canvas.create_line(90, 195, 90, 218, 280, 222, 280, 205, fill=self.theme_colors["muted"], width=2, smooth=True)

            wiimote = [(260, 30), (320, 30), (320, 205), (260, 205)]
            self.canvas.create_polygon(wiimote, fill=poly_color, outline=outline_color, width=2)

            self._draw_circle(290, 52, 8, "DPAD_UP", "▲", btn_bg, text_fg, outline_color, font_size=6)
            self._draw_circle(277, 65, 8, "DPAD_LEFT", "◄", btn_bg, text_fg, outline_color, font_size=6)
            self._draw_circle(303, 65, 8, "DPAD_RIGHT", "►", btn_bg, text_fg, outline_color, font_size=6)
            self._draw_circle(290, 78, 8, "DPAD_DOWN", "▼", btn_bg, text_fg, outline_color, font_size=6)

            self._draw_circle(290, 100, 10, "A", "A", btn_bg, text_fg, outline_color)
            self._draw_circle(277, 122, 7, "SELECT", "-", btn_bg, text_fg, outline_color)
            self._draw_circle(303, 122, 7, "START", "+", btn_bg, text_fg, outline_color)

            self._draw_circle(290, 148, 9, "1", "1", btn_bg, text_fg, outline_color)
            self._draw_circle(290, 172, 9, "2", "2", btn_bg, text_fg, outline_color)

        # 5. WII REMOTE SIDEWAYS
        elif p == "wii_sideways":
            wiimote_horiz = [(40, 80), (400, 80), (400, 150), (40, 150)]
            self.canvas.create_polygon(wiimote_horiz, fill=poly_color, outline=outline_color, width=2)

            self._draw_circle(80, 102, 8, "DPAD_UP", "▲", btn_bg, text_fg, outline_color, font_size=6)
            self._draw_circle(67, 115, 8, "DPAD_LEFT", "◄", btn_bg, text_fg, outline_color, font_size=6)
            self._draw_circle(93, 115, 8, "DPAD_RIGHT", "►", btn_bg, text_fg, outline_color, font_size=6)
            self._draw_circle(80, 128, 8, "DPAD_DOWN", "▼", btn_bg, text_fg, outline_color, font_size=6)

            self._draw_circle(140, 115, 12, "A", "A", btn_bg, text_fg, outline_color)
            self._draw_circle(190, 102, 8, "SELECT", "-", btn_bg, text_fg, outline_color)
            self._draw_circle(190, 128, 8, "START", "+", btn_bg, text_fg, outline_color)

            self._draw_circle(310, 115, 10, "1", "1", btn_bg, text_fg, outline_color)
            self._draw_circle(360, 115, 10, "2", "2", btn_bg, text_fg, outline_color)

        # 6. SWITCH JOY-CONS
        elif p == "switch":
            l_joycon = [(70, 50), (180, 50), (180, 200), (110, 200), (70, 160)]
            r_joycon = [(260, 50), (370, 50), (370, 160), (330, 200), (260, 200)]
            self.canvas.create_polygon(l_joycon, fill=poly_color, outline=outline_color, width=2)
            self.canvas.create_polygon(r_joycon, fill=poly_color, outline=outline_color, width=2)

            self._draw_rect(75, 25, 120, 42, "L2", "ZL", btn_bg, text_fg, outline_color)
            self._draw_rect(130, 28, 175, 45, "L1", "L", btn_bg, text_fg, outline_color)
            self._draw_rect(265, 28, 310, 45, "R1", "R", btn_bg, text_fg, outline_color)
            self._draw_rect(320, 25, 365, 42, "R2", "ZR", btn_bg, text_fg, outline_color)

            self._draw_circle(125, 80, 15, "LS", "LS", btn_bg, text_fg, outline_color)
            self._draw_circle(125, 130, 8, "DPAD_UP", "▲", btn_bg, text_fg, outline_color, font_size=6)
            self._draw_circle(112, 143, 8, "DPAD_LEFT", "◄", btn_bg, text_fg, outline_color, font_size=6)
            self._draw_circle(138, 143, 8, "DPAD_RIGHT", "►", btn_bg, text_fg, outline_color, font_size=6)
            self._draw_circle(125, 156, 8, "DPAD_DOWN", "▼", btn_bg, text_fg, outline_color, font_size=6)
            self._draw_rect(152, 60, 172, 72, "SELECT", "-", btn_bg, text_fg, outline_color)

            self._draw_circle(315, 80, 9, "X", "X", btn_bg, text_fg, outline_color)
            self._draw_circle(300, 95, 9, "Y", "Y", btn_bg, text_fg, outline_color)
            self._draw_circle(330, 95, 9, "A", "A", btn_bg, text_fg, outline_color)
            self._draw_circle(315, 110, 9, "B", "B", btn_bg, text_fg, outline_color)
            self._draw_circle(315, 150, 15, "RS", "RS", btn_bg, text_fg, outline_color)
            self._draw_rect(268, 60, 288, 72, "START", "+", btn_bg, text_fg, outline_color)

        # 7. STEAM DECK
        elif p == "steamdeck":
            body = [(30, 45), (410, 45), (430, 80), (430, 180), (400, 215), (40, 215), (10, 180), (10, 80)]
            self.canvas.create_polygon(body, fill=poly_color, outline=outline_color, width=2)
            self.canvas.create_rectangle(150, 60, 290, 180, outline=self.theme_colors["muted"], width=1)

            self._draw_rect(30, 22, 80, 38, "L2", "L2", btn_bg, text_fg, outline_color)
            self._draw_rect(85, 25, 130, 41, "L1", "L1", btn_bg, text_fg, outline_color)
            self._draw_rect(310, 25, 355, 41, "R1", "R1", btn_bg, text_fg, outline_color)
            self._draw_rect(360, 22, 410, 38, "R2", "R2", btn_bg, text_fg, outline_color)

            self._draw_circle(115, 75, 14, "LS", "LS", btn_bg, text_fg, outline_color)
            self._draw_circle(325, 75, 14, "RS", "RS", btn_bg, text_fg, outline_color)
            self._draw_rect(95, 130, 135, 160, "LS", "Pad L", btn_bg, text_fg, outline_color, font_size=6)
            self._draw_rect(305, 130, 345, 160, "RS", "Pad R", btn_bg, text_fg, outline_color, font_size=6)

            self._draw_circle(70, 75, 8, "DPAD_UP", "▲", btn_bg, text_fg, outline_color, font_size=6)
            self._draw_circle(57, 88, 8, "DPAD_LEFT", "◄", btn_bg, text_fg, outline_color, font_size=6)
            self._draw_circle(83, 88, 8, "DPAD_RIGHT", "►", btn_bg, text_fg, outline_color, font_size=6)
            self._draw_circle(70, 101, 8, "DPAD_DOWN", "▼", btn_bg, text_fg, outline_color, font_size=6)

            self._draw_circle(370, 65, 8, "Y", "Y", btn_bg, text_fg, outline_color)
            self._draw_circle(357, 78, 8, "X", "X", btn_bg, text_fg, outline_color)
            self._draw_circle(383, 78, 8, "B", "B", btn_bg, text_fg, outline_color)
            self._draw_circle(370, 91, 8, "A", "A", btn_bg, text_fg, outline_color)
            self._draw_rect(116, 48, 148, 58, "SELECT", "View", btn_bg, text_fg, outline_color, font_size=6)
            self._draw_rect(292, 48, 324, 58, "START", "Menu", btn_bg, text_fg, outline_color, font_size=6)

        # 8. HANDHELD VERTICAL
        elif p == "handheld_vertical":
            body = [(130, 30), (310, 30), (310, 220), (130, 220)]
            self.canvas.create_polygon(body, fill=poly_color, outline=outline_color, width=2)
            self.canvas.create_rectangle(150, 45, 290, 110, outline=self.theme_colors["muted"], width=1)

            self._draw_rect(130, 12, 175, 26, "L1", "L1/L2", btn_bg, text_fg, outline_color, font_size=6)
            self._draw_rect(265, 12, 310, 26, "R1", "R1/R2", btn_bg, text_fg, outline_color, font_size=6)

            self._draw_circle(175, 140, 8, "DPAD_UP", "▲", btn_bg, text_fg, outline_color, font_size=6)
            self._draw_circle(162, 153, 8, "DPAD_LEFT", "◄", btn_bg, text_fg, outline_color, font_size=6)
            self._draw_circle(188, 153, 8, "DPAD_RIGHT", "►", btn_bg, text_fg, outline_color, font_size=6)
            self._draw_circle(175, 166, 8, "DPAD_DOWN", "▼", btn_bg, text_fg, outline_color, font_size=6)

            self._draw_circle(265, 138, 9, "X", "X", btn_bg, text_fg, outline_color)
            self._draw_circle(250, 151, 9, "Y", "Y", btn_bg, text_fg, outline_color)
            self._draw_circle(280, 151, 9, "A", "A", btn_bg, text_fg, outline_color)
            self._draw_circle(265, 164, 9, "B", "B", btn_bg, text_fg, outline_color)
            self._draw_rect(182, 190, 218, 205, "SELECT", "Select", btn_bg, text_fg, outline_color, font_size=6)
            self._draw_rect(222, 190, 258, 205, "START", "Start", btn_bg, text_fg, outline_color, font_size=6)

        # 9. HANDHELD HORIZONTAL
        elif p == "handheld_horizontal":
            body = [(50, 45), (390, 45), (410, 80), (410, 180), (390, 215), (50, 215), (30, 180), (30, 80)]
            self.canvas.create_polygon(body, fill=poly_color, outline=outline_color, width=2)
            self.canvas.create_rectangle(150, 55, 290, 175, outline=self.theme_colors["muted"], width=1)

            self._draw_rect(50, 25, 120, 40, "L1", "L Trg", btn_bg, text_fg, outline_color, font_size=6)
            self._draw_rect(320, 25, 390, 40, "R1", "R Trg", btn_bg, text_fg, outline_color, font_size=6)

            self._draw_circle(90, 80, 15, "LS", "LS", btn_bg, text_fg, outline_color)
            self._draw_circle(90, 140, 8, "DPAD_UP", "▲", btn_bg, text_fg, outline_color, font_size=6)
            self._draw_circle(77, 153, 8, "DPAD_LEFT", "◄", btn_bg, text_fg, outline_color, font_size=6)
            self._draw_circle(103, 153, 8, "DPAD_RIGHT", "►", btn_bg, text_fg, outline_color, font_size=6)
            self._draw_circle(90, 166, 8, "DPAD_DOWN", "▼", btn_bg, text_fg, outline_color, font_size=6)

            self._draw_circle(350, 80, 9, "X", "X", btn_bg, text_fg, outline_color)
            self._draw_circle(335, 93, 9, "Y", "Y", btn_bg, text_fg, outline_color)
            self._draw_circle(365, 93, 9, "A", "A", btn_bg, text_fg, outline_color)
            self._draw_circle(350, 106, 9, "B", "B", btn_bg, text_fg, outline_color)

            self._draw_circle(350, 155, 15, "RS", "RS", btn_bg, text_fg, outline_color)
            self._draw_rect(165, 185, 208, 200, "SELECT", "Select", btn_bg, text_fg, outline_color, font_size=6)
            self._draw_rect(232, 185, 275, 200, "START", "Start", btn_bg, text_fg, outline_color, font_size=6)

    def _draw_circle(self, cx, cy, radius, key, label, bg, fg, outline, font_size=8):
        """Draws a circle button with strict pixel-centered bounding offsets."""
        is_hovered = (self.hovered_element and self.hovered_element[4] == key)
        is_listening = (self.listening_key == key)

        if is_listening:
            fill = "#f9e2af"
            text_color = "#11111b"
            display_text = "..."
        elif is_hovered:
            fill = self.theme_colors["accent"]
            text_color = self.theme_colors["bg"]
            display_text = label
        else:
            fill = bg
            text_color = fg
            display_text = label

        circle = self.canvas.create_oval(cx - radius, cy - radius, cx + radius, cy + radius, fill=fill, outline=outline, width=1.5)

        y_offset = -1 if label in ["▲", "▼", "◄", "►"] else 0

        text = self.canvas.create_text(
            cx, cy + y_offset,
            text=display_text,
            fill=text_color,
            font=("Segoe UI", font_size, "bold"),
            anchor="center"
        )
        self.interactive_elements.append((cx - radius, cy - radius, cx + radius, cy + radius, key, label, circle, text))

    def _draw_rect(self, x1, y1, x2, y2, key, label, bg, fg, outline, font_size=7):
        """Draws a rectangular button with mathematically centered label coordinates."""
        is_hovered = (self.hovered_element and self.hovered_element[4] == key)
        is_listening = (self.listening_key == key)

        if is_listening:
            fill = "#f9e2af"
            text_color = "#11111b"
            display_text = "PRESS"
        elif is_hovered:
            fill = self.theme_colors["accent"]
            text_color = self.theme_colors["bg"]
            display_text = label
        else:
            fill = bg
            text_color = fg
            display_text = label

        rect = self.canvas.create_rectangle(x1, y1, x2, y2, fill=fill, outline=outline, width=1.5)
        cx, cy = (x1 + x2) / 2.0, (y1 + y2) / 2.0

        text = self.canvas.create_text(
            cx, cy,
            text=display_text,
            fill=text_color,
            font=("Segoe UI", font_size, "bold"),
            anchor="center"
        )
        self.interactive_elements.append((x1, y1, x2, y2, key, label, rect, text))

    def _on_mouse_move(self, event):
        x, y = event.x, event.y
        new_hover = None
        for elem in self.interactive_elements:
            x1, y1, x2, y2, key, label, item, text_item = elem
            if x1 <= x <= x2 and y1 <= y <= y2:
                new_hover = elem
                break
        if new_hover != self.hovered_element:
            self.hovered_element = new_hover
            self.draw_gamepad()

    def _on_mouse_click(self, event):
        x, y = event.x, event.y
        for elem in self.interactive_elements:
            x1, y1, x2, y2, key, label, item, text_item = elem
            if x1 <= x <= x2 and y1 <= y <= y2:
                self.on_map_callback(key, label)
                break

# core/input_mapper.py

class UniversalInputMapper:
    """Translates physical hardware events to standardized abstract inputs and specialized layouts."""

    # Standard XInput / SDL2 Physical Mapping Defaults
    DEFAULT_STANDARD_BINDINGS = {
        "A": "Btn 0",          # South
        "B": "Btn 1",          # East
        "X": "Btn 2",          # West
        "Y": "Btn 3",          # North
        "L1": "Btn 4",         # Left Bumper
        "R1": "Btn 5",         # Right Bumper
        "L2": "Axis 2+",       # Left Trigger
        "R2": "Axis 5+",       # Right Trigger
        "SELECT": "Btn 6",     # Back / Share / Select
        "START": "Btn 7",      # Start / Options / Menu
        "LS": "Axis 0/1",      # Left Stick
        "RS": "Axis 3/4",      # Right Stick
        "DPAD_UP": "Hat 0.1",
        "DPAD_DOWN": "Hat 0.4",
        "DPAD_LEFT": "Hat 0.8",
        "DPAD_RIGHT": "Hat 0.2",
    }

    # Layout translations for specialized shapes
    SPECIAL_LAYOUT_TRANSLATIONS = {
        "gamecube": {
            "A": "A",          # Main Green Button -> Physical A
            "B": "B",          # Red B -> Physical B
            "X": "X",          # Right Bean X -> Physical X
            "Y": "Y",          # Top Bean Y -> Physical Y
            "Z": "R1",         # GC Z Bumper -> Physical RB
            "L1": "L2",        # Full Analog L -> Physical LT
            "R1": "R2",        # Full Analog R -> Physical RT
            "LS": "LS",        # Main Stick
            "RS": "RS",        # Yellow C-Stick
            "START": "START",
        },
        "wii_nunchuk": {
            "A": "A",          # Wiimote A -> Physical A
            "1": "X",          # Wiimote 1 -> Physical X
            "2": "Y",          # Wiimote 2 -> Physical Y
            "B": "R2",         # Wiimote B Trigger -> Physical RT
            "C": "L1",         # Nunchuk C -> Physical LB
            "Z": "L2",         # Nunchuk Z -> Physical LT
            "LS": "LS",        # Nunchuk Stick
            "SELECT": "SELECT",# Wiimote -
            "START": "START",  # Wiimote +
        }
    }

    def __init__(self):
        self.active_bindings = dict(self.DEFAULT_STANDARD_BINDINGS)

    def auto_bind_preset(self, preset_name: str):
        """Automatically assigns default bindings to standard or specialized layout shapes."""
        self.active_bindings = dict(self.DEFAULT_STANDARD_BINDINGS)

        if preset_name in self.SPECIAL_LAYOUT_TRANSLATIONS:
            special_map = self.SPECIAL_LAYOUT_TRANSLATIONS[preset_name]
            for target_key, physical_source in special_map.items():
                if physical_source in self.DEFAULT_STANDARD_BINDINGS:
                    self.active_bindings[target_key] = self.DEFAULT_STANDARD_BINDINGS[physical_source]

        return self.active_bindings

    def set_custom_binding(self, key: str, hardware_code: str):
        """Allows user to override any specific button manually."""
        self.active_bindings[key] = hardware_code

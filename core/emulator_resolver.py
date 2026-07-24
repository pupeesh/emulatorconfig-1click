import os
import platform

class EmulatorResolver:
    
    EMULATOR_META = {
        "dolphin": {"file": "Config/GFX.ini", "format": "ini"},
        "pcsx2": {"file": "inis/PCSX2.ini", "format": "ini"},
        "ppsspp": {"file": "PSP/SYSTEM/ppsspp.ini", "format": "ini"},
        "retroarch": {"file": "retroarch.cfg", "format": "cfg"},
        "cemu": {"file": "settings.xml", "format": "xml"},
        "ryujinx": {"file": "Config.json", "format": "json"},
        "retroarch-core-options": {"file": "retroarch-core-options.cfg", "format": "cfg"}
    }

    @staticmethod
    def detect_os():
        system = platform.system().lower()
        if "win" in system:
            return "windows"
        elif "darwin" in system:
            return "macos"
        return "linux"

    @staticmethod
    def check_portable_or_custom(emulator_executable_dir):
        """Checks if an emulator is running in Portable Mode next to its executable."""
        if not emulator_executable_dir or not os.path.exists(emulator_executable_dir):
            return None

        portable_file = os.path.join(emulator_executable_dir, "portable.txt")
        portable_dir = os.path.join(emulator_executable_dir, "portable")
        user_dir = os.path.join(emulator_executable_dir, "User")

        if os.path.exists(portable_file) or os.path.exists(portable_dir):
            if os.path.exists(user_dir):
                return user_dir
            return emulator_executable_dir

        return None

    @staticmethod
    def get_emulator_paths(emulator_key):
        """Returns (base_directory_path, exists_on_disk) for a given emulator."""
        os_type = EmulatorResolver.detect_os()
        home = os.path.expanduser("~")
        xdg_config = os.getenv("XDG_CONFIG_HOME", os.path.join(home, ".config"))
        emulator_key = emulator_key.lower()

        paths = []

        if "retroarch" in emulator_key:
            if os_type == "windows":
                paths = [
                    os.path.join(os.getenv("APPDATA", ""), "RetroArch"),
                    os.path.join(home, "AppData", "Roaming", "RetroArch")
                ]
            elif os_type == "macos":
                paths = [os.path.join(home, "Library", "Application Support", "RetroArch")]
            elif os_type == "linux":
                paths = [
                    os.path.join(xdg_config, "retroarch"),
                    os.path.join(home, ".var", "app", "org.libretro.RetroArch", "config", "retroarch"),
                    os.path.join(home, "Emulation", "tools", "retroarch")
                ]

        elif emulator_key == "dolphin":
            if os_type == "windows":
                paths = [
                    os.path.join(os.getenv("APPDATA", ""), "Dolphin Emulator"),
                    os.path.join(home, "Documents", "Dolphin Emulator")
                ]
            elif os_type == "macos":
                paths = [os.path.join(home, "Library", "Application Support", "Dolphin")]
            elif os_type == "linux":
                paths = [
                    os.path.join(xdg_config, "dolphin-emu"),
                    os.path.join(home, ".var", "app", "org.DolphinEmu.dolphin-emu", "config", "dolphin-emu"),
                    os.path.join(home, "Emulation", "tools", "dolphin-emu")
                ]

        elif emulator_key == "pcsx2":
            if os_type == "windows":
                paths = [
                    os.path.join(os.getenv("APPDATA", ""), "PCSX2"),
                    os.path.join(home, "Documents", "PCSX2")
                ]
            elif os_type == "macos":
                paths = [os.path.join(home, "Library", "Application Support", "PCSX2")]
            elif os_type == "linux":
                paths = [
                    os.path.join(xdg_config, "PCSX2"),
                    os.path.join(home, ".var", "app", "net.pcsx2.PCSX2", "config", "PCSX2"),
                    os.path.join(home, "Emulation", "tools", "pcsx2")
                ]

        elif emulator_key == "ppsspp":
            if os_type == "windows":
                paths = [os.path.join(os.getenv("APPDATA", ""), "PPSSPP")]
            elif os_type == "macos":
                paths = [os.path.join(home, "Library", "Application Support", "PPSSPP")]
            elif os_type == "linux":
                paths = [
                    os.path.join(xdg_config, "ppsspp"),
                    os.path.join(home, ".var", "app", "org.ppsspp.PPSSPP", "config", "ppsspp"),
                    os.path.join(home, "Emulation", "tools", "ppsspp")
                ]

        elif emulator_key == "cemu":
            if os_type == "windows":
                paths = [
                    os.path.join(os.getenv("APPDATA", ""), "Cemu"),
                    os.path.join(home, "AppData", "Roaming", "Cemu")
                ]
            elif os_type == "macos":
                paths = [os.path.join(home, "Library", "Application Support", "Cemu")]
            elif os_type == "linux":
                paths = [
                    os.path.join(xdg_config, "cemu"),
                    os.path.join(home, ".var", "app", "info.cemu.Cemu", "config", "cemu"),
                    os.path.join(home, "Emulation", "tools", "cemu")
                ]

        elif emulator_key == "ryujinx":
            if os_type == "windows":
                paths = [os.path.join(os.getenv("APPDATA", ""), "Ryujinx")]
            elif os_type == "macos":
                paths = [os.path.join(home, "Library", "Application Support", "Ryujinx")]
            elif os_type == "linux":
                paths = [
                    os.path.join(xdg_config, "Ryujinx"),
                    os.path.join(home, ".var", "app", "org.ryujinx.Ryujinx", "config", "Ryujinx")
                ]

        for p in paths:
            if os.path.exists(p):
                return p, True

        return (paths[0] if paths else ""), False

    @staticmethod
    def get_target_config_file(emulator_key, base_dir):
        meta = EmulatorResolver.EMULATOR_META.get(emulator_key.lower(), {})
        if not meta or not base_dir:
            return None, None
        return os.path.join(base_dir, meta["file"]), meta["format"]

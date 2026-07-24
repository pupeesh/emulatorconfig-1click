import os
import sys
import platform
import subprocess

class SystemPoller:
    @staticmethod
    def detect_os():
        system = platform.system().lower()
        if "win" in system:
            return "windows"
        elif "darwin" in system:
            return "macos"
        else:
            return "linux"

    @staticmethod
    def _get_cpu_name():
        os_type = SystemPoller.detect_os()
        try:
            if os_type == "linux":
                with open("/proc/cpuinfo", "r") as f:
                    for line in f:
                        if "model name" in line:
                            return line.split(":")[1].strip()
            elif os_type == "windows":
                return platform.processor() or os.getenv("PROCESSOR_IDENTIFIER", "Unknown CPU")
            elif os_type == "macos":
                cmd = ["sysctl", "-n", "machdep.cpu.brand_string"]
                return subprocess.check_output(cmd).decode().strip()
        except Exception:
            pass
        return platform.processor() or platform.machine()

    @staticmethod
    def _get_total_ram_gb():
        os_type = SystemPoller.detect_os()
        try:
            if os_type == "linux":
                with open("/proc/meminfo", "r") as f:
                    for line in f:
                        if "MemTotal" in line:
                            mem_kb = int(line.split()[1])
                            return round(mem_kb / (1024 * 1024), 1)
            elif os_type == "windows":
                # Uses WMIC / PowerShell query safely or fallback
                output = subprocess.check_output("wmic os get TotalVisibleMemorySize", shell=True)
                kb = int(output.decode().split("\n")[1].strip())
                return round(kb / (1024 * 1024), 1)
            elif os_type == "macos":
                cmd = ["sysctl", "-n", "hw.memsize"]
                bytes_mem = int(subprocess.check_output(cmd).decode().strip())
                return round(bytes_mem / (1024**3), 1)
        except Exception:
            pass
        return "Unknown"

    @staticmethod
    def _get_gpu_info():
        os_type = SystemPoller.detect_os()
        try:
            if os_type == "linux":
                # Use lspci to grab VGA/3D controller info
                output = subprocess.check_output("lspci | grep -E 'VGA|3D'", shell=True).decode()
                gpu_line = output.splitlines()[0]
                return gpu_line.split(" controller: ")[-1].strip()
            elif os_type == "windows":
                output = subprocess.check_output("wmic path win32_VideoController get name", shell=True)
                lines = [line.strip() for line in output.decode().split("\n") if line.strip()]
                if len(lines) > 1:
                    return lines[1]
            elif os_type == "macos":
                cmd = ["system_profiler", "SPDisplaysDataType"]
                output = subprocess.check_output(cmd).decode()
                for line in output.splitlines():
                    if "Chipset Model:" in line:
                        return line.split("Chipset Model:")[1].strip()
        except Exception:
            pass
        return "Generic GPU / Integrated"

    @staticmethod
    def get_hardware_info():
        os_type = SystemPoller.detect_os()
        
        # Default graphics API recommendation based on OS
        renderer = "Vulkan"
        if os_type == "macos":
            renderer = "Metal"
        elif os_type == "windows":
            renderer = "Vulkan"

        return {
            "os": os_type,
            "os_release": platform.release(),
            "arch": platform.machine(),
            "cpu": SystemPoller._get_cpu_name(),
            "cpu_cores": os.cpu_count() or 1,
            "ram_gb": SystemPoller._get_total_ram_gb(),
            "gpu": SystemPoller._get_gpu_info(),
            "renderer": renderer,
            "internal_res": "2"  # Preset default
        }

    @staticmethod
    def resolve_emulator_paths(emulator="dolphin"):
        os_type = SystemPoller.detect_os()
        home = os.path.expanduser("~")
        
        paths = []
        if emulator.lower() == "dolphin":
            if os_type == "windows":
                paths = [
                    os.path.join(os.getenv("APPDATA", ""), "Dolphin Emulator"),
                    os.path.join(home, "Documents", "Dolphin Emulator")
                ]
            elif os_type == "macos":
                paths = [
                    os.path.join(home, "Library", "Application Support", "Dolphin")
                ]
            elif os_type == "linux":
                paths = [
                    os.path.join(home, ".config", "dolphin-emu")
                ]

        for p in paths:
            if os.path.exists(p):
                return p
        return paths[0] if paths else ""

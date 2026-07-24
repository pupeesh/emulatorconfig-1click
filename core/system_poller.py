import os
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
        return "linux"

    @staticmethod
    def _get_cpu_name():
        os_type = SystemPoller.detect_os()
        try:
            if os_type == "linux":
                if os.path.exists("/proc/cpuinfo"):
                    with open("/proc/cpuinfo", "r") as f:
                        for line in f:
                            if "model name" in line:
                                return line.split(":")[1].strip()
            elif os_type == "windows":
                return platform.processor() or os.getenv("PROCESSOR_IDENTIFIER", "Unknown CPU")
            elif os_type == "macos":
                cmd = ["sysctl", "-n", "machdep.cpu.brand_string"]
                return subprocess.check_output(cmd, stderr=subprocess.DEVNULL, timeout=2.0).decode().strip()
        except Exception:
            pass
        return platform.processor() or platform.machine() or "Unknown CPU"

    @staticmethod
    def _get_total_ram_gb():
        os_type = SystemPoller.detect_os()
        try:
            if os_type == "linux":
                if os.path.exists("/proc/meminfo"):
                    with open("/proc/meminfo", "r") as f:
                        for line in f:
                            if "MemTotal" in line:
                                mem_kb = int(line.split()[1])
                                return round(mem_kb / (1024 * 1024), 1)
            elif os_type == "windows":
                output = subprocess.check_output(
                    ["wmic", "os", "get", "TotalVisibleMemorySize"], 
                    stderr=subprocess.DEVNULL,
                    timeout=2.0
                )
                kb = int(output.decode().split("\n")[1].strip())
                return round(kb / (1024 * 1024), 1)
            elif os_type == "macos":
                cmd = ["sysctl", "-n", "hw.memsize"]
                bytes_mem = int(subprocess.check_output(cmd, stderr=subprocess.DEVNULL, timeout=2.0).decode().strip())
                return round(bytes_mem / (1024**3), 1)
        except Exception:
            pass
        return "Unknown"

    @staticmethod
    def _get_gpu_info():
        os_type = SystemPoller.detect_os()
        try:
            if os_type == "linux":
                output = subprocess.check_output(
                    ["lspci"], stderr=subprocess.DEVNULL, timeout=2.0
                ).decode()
                for line in output.splitlines():
                    if "VGA" in line or "3D" in line:
                        return line.split(" controller: ")[-1].strip()
            elif os_type == "windows":
                output = subprocess.check_output(
                    ["wmic", "path", "win32_VideoController", "get", "name"],
                    stderr=subprocess.DEVNULL,
                    timeout=2.0
                )
                lines = [line.strip() for line in output.decode().split("\n") if line.strip()]
                if len(lines) > 1:
                    return lines[1]
            elif os_type == "macos":
                cmd = ["system_profiler", "SPDisplaysDataType"]
                output = subprocess.check_output(cmd, stderr=subprocess.DEVNULL, timeout=2.0).decode()
                for line in output.splitlines():
                    if "Chipset Model:" in line:
                        return line.split("Chipset Model:")[1].strip()
        except Exception:
            pass
        return "Generic GPU / Integrated"

    @staticmethod
    def get_hardware_info():
        os_type = SystemPoller.detect_os()
        renderer = "Metal" if os_type == "macos" else "Vulkan"

        return {
            "os": os_type,
            "os_release": platform.release(),
            "arch": platform.machine(),
            "cpu": SystemPoller._get_cpu_name(),
            "cpu_cores": os.cpu_count() or 1,
            "ram_gb": SystemPoller._get_total_ram_gb(),
            "gpu": SystemPoller._get_gpu_info(),
            "renderer": renderer,
            "internal_res": "2"
        }

import os
import sys

# Add project root to sys.path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from core.system_poller import SystemPoller
from core.yaml_engine import YAMLEngine

def run_test():
    print("--- 1. Testing System Poller Specs ---")
    sys_info = SystemPoller.get_hardware_info()
    dolphin_path = SystemPoller.resolve_emulator_paths("dolphin")
    
    print(f"OS: {sys_info['os']} ({sys_info['os_release']})")
    print(f"Architecture: {sys_info['arch']}")
    print(f"CPU: {sys_info['cpu']} ({sys_info['cpu_cores']} Threads)")
    print(f"RAM: {sys_info['ram_gb']} GB")
    print(f"GPU: {sys_info['gpu']}")
    print(f"Recommended Target Renderer: {sys_info['renderer']}")
    print(f"Resolved Dolphin Path: {dolphin_path}\n")

    print("--- 2. Testing YAML Engine & Injection ---")
    template_path = os.path.join("config_templates", "dolphin.yml")
    mock_target = os.path.join("tests", "mock_sys", "dolphin", "Config", "GFX.ini")

    yaml_data = YAMLEngine.parse_simple_yaml(template_path)
    processed_data = YAMLEngine.inject_variables(yaml_data, sys_info)
    YAMLEngine.write_ini_config(mock_target, processed_data)

    print(f"Successfully generated mock config at: {mock_target}\n")
    with open(mock_target, "r") as f:
        print(f.read())

if __name__ == "__main__":
    run_test()

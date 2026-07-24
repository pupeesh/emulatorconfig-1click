import os
import sys

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from core.emulator_resolver import EmulatorResolver
from core.system_poller import SystemPoller
from core.yaml_engine import YAMLEngine
from core.config_writer import ConfigWriter

def test_emulator_resolver_pipeline():
    print("--- 1. Hardware Spec Polling ---")
    sys_info = SystemPoller.get_hardware_info()
    print(f"OS: {sys_info['os']} ({sys_info['os_release']}) | CPU: {sys_info['cpu']}")
    print(f"Target Renderer: {sys_info['renderer']}\n")

    print("--- 2. Multi-Emulator & Core Options Path Resolution ---")
    all_targets = ["dolphin", "pcsx2", "ppsspp", "retroarch", "retroarch-core-options", "cemu", "ryujinx"]
    mock_base = os.path.abspath(os.path.join("tests", "mock_sys"))

    for target in all_targets:
        path, exists = EmulatorResolver.get_emulator_paths(target)
        status = "Detected on disk" if exists else "Default target path"
        print(f"[{target.upper()}] -> {path} ({status})")

        template_name = "retroarch-core-options" if target == "retroarch-core-options" else target
        template_file = os.path.join("config_templates", f"{template_name}.yml")

        if os.path.exists(template_file):
            parsed = YAMLEngine.parse_simple_yaml(template_file)
            injected = YAMLEngine.inject_variables(parsed, sys_info)

            mock_emu_dir = os.path.join(mock_base, target)
            target_file, fmt = EmulatorResolver.get_target_config_file(target, mock_emu_dir)

            if fmt == "ini":
                ConfigWriter.write_ini(target_file, injected)
            elif fmt == "cfg":
                flat_dict = {}
                for k, v in injected.items():
                    if isinstance(v, dict):
                        flat_dict.update(v)
                    else:
                        flat_dict[k] = v
                ConfigWriter.write_cfg(target_file, flat_dict)
            elif fmt == "json":
                ConfigWriter.write_json(target_file, injected)
            elif fmt == "xml":
                flat_dict = {}
                for k, v in injected.items():
                    if isinstance(v, dict):
                        flat_dict.update(v)
                    else:
                        flat_dict[k] = v
                ConfigWriter.write_xml(target_file, flat_dict)

            assert os.path.exists(target_file), f"Failed to generate config for {target}"
            print(f"  -> Created mock config ({fmt.upper()}): {target_file}")

    print("\n--- 3. Testing Portable Mode Detection ---")
    mock_portable_dir = os.path.join(mock_base, "portable_dolphin")
    mock_user_dir = os.path.join(mock_portable_dir, "User")
    os.makedirs(mock_user_dir, exist_ok=True)
    
    with open(os.path.join(mock_portable_dir, "portable.txt"), "w") as f:
        f.write("portable mode trigger")

    detected_portable = EmulatorResolver.check_portable_or_custom(mock_portable_dir)
    print(f"Portable Executable Dir: {mock_portable_dir}")
    print(f"Resolved Portable Config Dir: {detected_portable}")
    
    assert detected_portable == mock_user_dir, "Portable mode resolution failed!"
    print("  -> Portable Mode detected successfully!")

    print("\nComplete Pipeline Test Passed Successfully!")

if __name__ == "__main__":
    test_emulator_resolver_pipeline()

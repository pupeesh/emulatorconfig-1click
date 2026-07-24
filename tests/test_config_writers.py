import os
import sys

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from core.config_writer import ConfigWriter

def test_config_writers():
    mock_base = os.path.abspath(os.path.join("tests", "mock_sys"))

    print("--- 1. Testing INI Writer (Dolphin / PCSX2) ---")
    ini_path = os.path.join(mock_base, "dolphin", "Dolphin.ini")
    ConfigWriter.write_ini(ini_path, {"GFX": {"Backend": "Vulkan", "Adapter": "0"}})
    with open(ini_path) as f:
        assert "Backend = Vulkan" in f.read()
    print("  ✓ INI Writer passed")

    print("--- 2. Testing Flat CFG Writer (RetroArch) ---")
    cfg_path = os.path.join(mock_base, "retroarch", "retroarch.cfg")
    ConfigWriter.write_cfg(cfg_path, {"video_driver": "vulkan", "rewind_enable": "true"})
    with open(cfg_path) as f:
        assert 'video_driver = "vulkan"' in f.read()
    print("  ✓ CFG Writer passed")

    print("--- 3. Testing JSON Writer (Ryujinx) ---")
    json_path = os.path.join(mock_base, "ryujinx", "Config.json")
    ConfigWriter.write_json(json_path, {"graphics": {"backend": "Vulkan", "res_scale": 2}})
    with open(json_path) as f:
        assert '"backend": "Vulkan"' in f.read()
    print("  ✓ JSON Writer passed")

    print("--- 4. Testing XML Writer (Cemu) ---")
    xml_path = os.path.join(mock_base, "cemu", "settings.xml")
    ConfigWriter.write_xml(xml_path, {"Graphic/API": "Vulkan"})
    with open(xml_path) as f:
        assert "<API>Vulkan</API>" in f.read()
    print("  ✓ XML Writer passed")

    print("\nAll Multi-Format Config Writers Passed Successfully!")

if __name__ == "__main__":
    test_config_writers()

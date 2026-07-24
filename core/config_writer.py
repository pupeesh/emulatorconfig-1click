import os
import json
from configparser import ConfigParser
import xml.etree.ElementTree as ET

class ConfigWriter:
    
    # -------------------------------------------------------------
    # 1. INI / CFG Writer (Dolphin, PCSX2, PPSSPP)
    # -------------------------------------------------------------
    @staticmethod
    def write_ini(target_path, config_dict):
        """Non-destructively merges and writes sectioned INI files atomically."""
        os.makedirs(os.path.dirname(os.path.abspath(target_path)), exist_ok=True)
        config = ConfigParser()
        config.optionxform = str  # Preserve key case sensitivity

        if os.path.exists(target_path):
            try:
                config.read(target_path, encoding="utf-8")
            except Exception:
                pass

        for section, keys in config_dict.items():
            if not config.has_section(section):
                config.add_section(section)
            for k, v in keys.items():
                config.set(section, str(k), str(v))

        temp_path = f"{target_path}.tmp"
        with open(temp_path, "w", encoding="utf-8") as f:
            config.write(f)
            f.flush()
            os.fsync(f.fileno())

        os.replace(temp_path, target_path)
        return True

    # -------------------------------------------------------------
    # 2. Flat CFG Writer (RetroArch)
    # -------------------------------------------------------------
    @staticmethod
    def write_cfg(target_path, updates_dict):
        """Non-destructively updates key = "value" pairs inside RetroArch .cfg files."""
        os.makedirs(os.path.dirname(os.path.abspath(target_path)), exist_ok=True)
        lines = []
        existing_keys = set()

        if os.path.exists(target_path):
            with open(target_path, "r", encoding="utf-8") as f:
                for line in f:
                    stripped = line.strip()
                    if "=" in stripped and not stripped.startswith("#"):
                        key = stripped.split("=")[0].strip()
                        if key in updates_dict:
                            lines.append(f'{key} = "{updates_dict[key]}"\n')
                            existing_keys.add(key)
                            continue
                    lines.append(line)

        # Append new keys that didn't exist in the file
        for k, v in updates_dict.items():
            if k not in existing_keys:
                lines.append(f'{k} = "{v}"\n')

        temp_path = f"{target_path}.tmp"
        with open(temp_path, "w", encoding="utf-8") as f:
            f.writelines(lines)
            f.flush()
            os.fsync(f.fileno())

        os.replace(temp_path, target_path)
        return True

    # -------------------------------------------------------------
    # 3. JSON Writer (Ryujinx, Eden)
    # -------------------------------------------------------------
    @staticmethod
    def write_json(target_path, updates_dict):
        """Non-destructively updates nested dictionaries inside JSON configs."""
        os.makedirs(os.path.dirname(os.path.abspath(target_path)), exist_ok=True)
        data = {}

        if os.path.exists(target_path):
            try:
                with open(target_path, "r", encoding="utf-8") as f:
                    data = json.load(f)
            except Exception:
                data = {}

        def deep_update(d, u):
            for k, v in u.items():
                if isinstance(v, dict) and k in d and isinstance(d[k], dict):
                    deep_update(d[k], v)
                else:
                    d[k] = v

        deep_update(data, updates_dict)

        temp_path = f"{target_path}.tmp"
        with open(temp_path, "w", encoding="utf-8") as f:
            json.dump(data, f, indent=2)
            f.flush()
            os.fsync(f.fileno())

        os.replace(temp_path, target_path)
        return True

    # -------------------------------------------------------------
    # 4. XML Writer (Cemu)
    # -------------------------------------------------------------
    @staticmethod
    def _find_or_create_element(root, path):
        """Recursively finds or builds XML nodes for paths like 'Graphic/API'."""
        parts = [p for p in path.split("/") if p]
        curr = root
        for part in parts:
            child = curr.find(part)
            if child is None:
                child = ET.SubElement(curr, part)
            curr = child
        return curr

    @staticmethod
    def write_xml(target_path, updates_dict, root_tag="Content"):
        """Non-destructively updates nested tag values in XML files."""
        os.makedirs(os.path.dirname(os.path.abspath(target_path)), exist_ok=True)

        if os.path.exists(target_path):
            try:
                tree = ET.parse(target_path)
                root = tree.getroot()
            except Exception:
                root = ET.Element(root_tag)
                tree = ET.ElementTree(root)
        else:
            root = ET.Element(root_tag)
            tree = ET.ElementTree(root)

        for tag_path, val in updates_dict.items():
            elem = ConfigWriter._find_or_create_element(root, tag_path)
            elem.text = str(val)

        temp_path = f"{target_path}.tmp"
        tree.write(temp_path, encoding="utf-8", xml_declaration=True)
        
        with open(temp_path, "a", encoding="utf-8") as f:
            f.flush()
            os.fsync(f.fileno())

        os.replace(temp_path, target_path)
        return True

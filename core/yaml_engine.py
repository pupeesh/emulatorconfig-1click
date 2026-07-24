import os

class YAMLEngine:
    @staticmethod
    def parse_simple_yaml(yaml_path):
        """Simple pure-Python YAML parser for key-value dictionary mappings."""
        data = {}
        current_section = "General"
        
        if not os.path.exists(yaml_path):
            return data

        with open(yaml_path, "r", encoding="utf-8") as f:
            for line in f:
                # Strip comments starting at #
                line = line.split("#")[0].strip()
                if not line:
                    continue
                if line.endswith(":"):
                    current_section = line[:-1].strip()
                    if current_section not in data:
                        data[current_section] = {}
                elif ":" in line:
                    key, val = line.split(":", 1)
                    key = key.strip()
                    val = val.strip().strip('"').strip("'")
                    if current_section not in data:
                        data[current_section] = {}
                    data[current_section][key] = val
        return data

    @staticmethod
    def inject_variables(yaml_data, context):
        """Replaces placeholders ($RENDERER, $INTERNAL_RES) with system variables."""
        processed = {}
        for section, keys in yaml_data.items():
            processed[section] = {}
            for k, v in keys.items():
                for ctx_k, ctx_v in context.items():
                    v = str(v).replace(f"${ctx_k.upper()}", str(ctx_v))
                processed[section][k] = v
        return processed

#!/bin/bash
# ==========================================
# CEMU GLOBAL SETTINGS & CONTROLLER CONFIGURATOR (LINUX)
# ==========================================

# -----------------------------------------------------------------------------
# CUSTOM INSTALLATIONS GUIDE:
# - Native/AppImage defaults: ~/.config/Cemu/
# - Flatpak: ~/.var/app/info.cemu.Cemu/config/Cemu/
# - Portable AppImage/Extracts: [Cemu_Folder]/
# - If on secondary drive (e.g. /mnt/games/cemu), edit below:
#   CUSTOM_DIR="/mnt/games/cemu"
# -----------------------------------------------------------------------------
CUSTOM_DIR=""

POSSIBLE_DIRS=(
    "$CUSTOM_DIR"
    "$HOME/.var/app/info.cemu.Cemu/config/Cemu"
    "$HOME/.config/Cemu"
    "/mnt/Emulators/Cemu"
)

CEMU_DIR=""
for dir in "${POSSIBLE_DIRS[@]}"; do
    if [ -n "$dir" ] && [ -d "$dir" ]; then
        CEMU_DIR="$dir"
        break
    fi
done

if [ -z "$CEMU_DIR" ]; then
    CEMU_DIR="$HOME/.config/Cemu"
fi

PROFILES_DIR="$CEMU_DIR/controllerProfiles"
mkdir -p "$CEMU_DIR"
mkdir -p "$PROFILES_DIR"

cat << 'EOF' > "$CEMU_DIR/settings.xml"
<?xml version="1.0" encoding="UTF-8"?>
<content>
    <Graphic>
        <api>Vulkan</api>
        <asyncCompile>true</asyncCompile>
        <VSync>1</VSync>
    </Graphic>
    <CPU>
        <Mode>DualcoreRecompiler</Mode>
    </CPU>
</content>
EOF

cat << 'EOF' > "$PROFILES_DIR/P1_ProController.xml"
<?xml version="1.0" encoding="UTF-8"?>
<emu_controller>
    <user_option name="controller_type" value="1"/>
    <user_option name="api" value="XInput"/>
    <user_option name="device" value="Controller 1"/>
    <user_option name="rumble" value="100"/>
    <mappings>
        <mapping button="1" key="0"/>
        <mapping button="2" key="1"/>
        <mapping button="4" key="2"/>
        <mapping button="8" key="3"/>
        <mapping button="16" key="4"/>
        <mapping button="32" key="5"/>
        <mapping button="64" key="6"/>
        <mapping button="128" key="7"/>
        <mapping button="256" key="8"/>
        <mapping button="512" key="9"/>
        <mapping button="1024" key="10"/>
        <mapping button="2048" key="11"/>
    </mappings>
</emu_controller>
EOF

sed 's/value="Controller 1"/value="Controller 2"/g' "$PROFILES_DIR/P1_ProController.xml" > "$PROFILES_DIR/P2_ProController.xml"

echo "[Cemu] Applied settings to: $CEMU_DIR"
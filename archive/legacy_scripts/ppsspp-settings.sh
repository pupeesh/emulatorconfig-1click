#!/bin/bash
# ==========================================
# PPSSPP CONTROLLER & GRAPHICS CONFIGURATOR (LINUX)
# ==========================================

# -----------------------------------------------------------------------------
# CUSTOM INSTALLATIONS GUIDE:
# - Standard Native: ~/.config/ppsspp/PSP/SYSTEM/
# - Flatpak: ~/.var/app/org.ppsspp.PPSSPP/config/ppsspp/PSP/SYSTEM/
# - Portable ZIP builds: [PPSSPP_Folder]/memstick/PSP/SYSTEM/
# - If on secondary drive (e.g. /mnt/storage/ppsspp), edit below:
#   CUSTOM_DIR="/mnt/storage/ppsspp/memstick/PSP/SYSTEM"
# -----------------------------------------------------------------------------
CUSTOM_DIR=""

POSSIBLE_DIRS=(
    "$CUSTOM_DIR"
    "$HOME/.var/app/org.ppsspp.PPSSPP/config/ppsspp/PSP/SYSTEM"
    "$HOME/.config/ppsspp/PSP/SYSTEM"
    "/mnt/Emulators/PPSSPP/memstick/PSP/SYSTEM"
)

MEMSTICK_DIR=""
for dir in "${POSSIBLE_DIRS[@]}"; do
    if [ -n "$dir" ] && [ -d "$dir" ]; then
        MEMSTICK_DIR="$dir"
        break
    fi
done

if [ -z "$MEMSTICK_DIR" ]; then
    MEMSTICK_DIR="$HOME/.config/ppsspp/PSP/SYSTEM"
fi

mkdir -p "$MEMSTICK_DIR"

cat << 'EOF' > "$MEMSTICK_DIR/ppsspp.ini"
[Graphics]
GPUBackend = 3
InternalResolution = 3
AnisotropicFiltering = 4
BufferedRendering = 1

[System]
FastRun = True
EOF

cat << 'EOF' > "$MEMSTICK_DIR/controls.ini"
[ControlMapping]
Up = 1-19,10-4001
Down = 1-20,10-4002
Left = 1-21,10-4004
Right = 1-22,10-4008
Circle = 1-10,10-40001
Cross = 1-9,10-40002
Square = 1-12,10-40004
Triangle = 1-11,10-40008
Start = 1-13,10-400001
Select = 1-14,10-400002
L = 1-15,10-400004
R = 1-16,10-400008
An.Up = 1-4001
An.Down = 1-4002
An.Left = 1-4004
An.Right = 1-4008
EOF

echo "[PPSSPP] Applied settings to: $MEMSTICK_DIR"
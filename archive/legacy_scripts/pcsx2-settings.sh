#!/bin/bash
# ==========================================
# PCSX2 CONTROLLER & GRAPHICS CONFIGURATOR (LINUX)
# ==========================================

# -----------------------------------------------------------------------------
# CUSTOM INSTALLATIONS GUIDE:
# - Standard Native / AppImage: ~/.config/PCSX2/inis/PCSX2.ini
# - Flatpak (Flathub): ~/.var/app/net.pcsx2.PCSX2/config/PCSX2/inis/PCSX2.ini
# - If installed on a secondary drive (e.g. /mnt/games/PCSX2), edit below:
#   CUSTOM_PATH="/mnt/games/PCSX2/inis/PCSX2.ini"
# -----------------------------------------------------------------------------
CUSTOM_PATH=""

POSSIBLE_PATHS=(
    "$CUSTOM_PATH"
    "$HOME/.var/app/net.pcsx2.PCSX2/config/PCSX2/inis/PCSX2.ini"
    "$HOME/.config/PCSX2/inis/PCSX2.ini"
    "/mnt/Emulators/PCSX2/inis/PCSX2.ini"
)

PCSX2_INI=""
for path in "${POSSIBLE_PATHS[@]}"; do
    if [ -n "$path" ] && [ -d "$(dirname "$path")" ]; then
        PCSX2_INI="$path"
        break
    fi
done

if [ -z "$PCSX2_INI" ]; then
    PCSX2_INI="$HOME/.config/PCSX2/inis/PCSX2.ini"
fi

mkdir -p "$(dirname "$PCSX2_INI")"

cat << 'EOF' > "$PCSX2_INI"
[EmuCore/GS]
Renderer = Vulkan
UpscaleMultiplier = 2
MaxAnisotropy = 16
AsyncTextureLoading = True

[EmuCore]
EnableWideScreenPatches = True

[Pad1]
Type = DualShock2
InvertLeftStickY = false
InvertRightStickY = false
ButtonUp = Axis/LeftAnalogY-
ButtonDown = Axis/LeftAnalogY+
ButtonLeft = Axis/LeftAnalogX-
ButtonRight = Axis/LeftAnalogX+
Up = Hat/DPadUp
Down = Hat/DPadDown
Left = Hat/DPadLeft
Right = Hat/DPadRight
Triangle = Button/Y
Circle = Button/B
Cross = Button/A
Square = Button/X
L1 = Button/LeftShoulder
R1 = Button/RightShoulder
L2 = Axis/LeftTrigger+
R2 = Axis/RightTrigger+
L3 = Button/LeftThumb
R3 = Button/RightThumb
Start = Button/Start
Select = Button/Back

[Pad2]
Type = DualShock2
InvertLeftStickY = false
InvertRightStickY = false
ButtonUp = Axis/LeftAnalogY-
ButtonDown = Axis/LeftAnalogY+
ButtonLeft = Axis/LeftAnalogX-
ButtonRight = Axis/LeftAnalogX+
Up = Hat/DPadUp
Down = Hat/DPadDown
Left = Hat/DPadLeft
Right = Hat/DPadRight
Triangle = Button/Y
Circle = Button/B
Cross = Button/A
Square = Button/X
L1 = Button/LeftShoulder
R1 = Button/RightShoulder
L2 = Axis/LeftTrigger+
R2 = Axis/RightTrigger+
L3 = Button/LeftThumb
R3 = Button/RightThumb
Start = Button/Start
Select = Button/Back
EOF

echo "[PCSX2] Applied settings to: $PCSX2_INI"
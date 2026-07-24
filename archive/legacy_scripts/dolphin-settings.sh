#!/bin/bash
# ==========================================
# DOLPHIN GLOBAL SETTINGS & CONTROLLER CONFIGURATOR (LINUX)
# ==========================================

# -----------------------------------------------------------------------------
# CUSTOM INSTALLATIONS GUIDE:
# - Standard Native App: ~/.config/dolphin-emu/
# - Flatpak: ~/.var/app/org.dolphin_emu.dolphin-emu/config/dolphin-emu/
# - Portable AppImage: [Dolphin_Folder]/User/
# - If running a portable build on secondary drive, edit below:
#   CUSTOM_DOLPHIN_DIR="/mnt/storage/Dolphin-x64"
# -----------------------------------------------------------------------------
CUSTOM_DOLPHIN_DIR=""

POSSIBLE_DOLPHIN_DIRS=(
    "$CUSTOM_DOLPHIN_DIR"
    "$HOME/.var/app/org.dolphin_emu.dolphin-emu/config/dolphin-emu"
    "$HOME/.config/dolphin-emu"
    "/mnt/Emulators/Dolphin-x64"
)

DOLPHIN_DIR=""
for dir in "${POSSIBLE_DOLPHIN_DIRS[@]}"; do
    if [ -n "$dir" ] && [ -d "$dir" ]; then
        DOLPHIN_DIR="$dir"
        break
    fi
done

if [ -z "$DOLPHIN_DIR" ]; then
    DOLPHIN_DIR="$HOME/.config/dolphin-emu"
fi

if [ -f "$DOLPHIN_DIR/portable.txt" ]; then
    CONFIG_DIR="$DOLPHIN_DIR/User/Config"
    GAME_SETTINGS_FOLDER="$DOLPHIN_DIR/User/GameSettings"
    GC_PROFILES_DIR="$DOLPHIN_DIR/User/Config/Profiles/GCPad"
    WII_PROFILES_DIR="$DOLPHIN_DIR/User/Config/Profiles/Wiimote"
else
    CONFIG_DIR="$DOLPHIN_DIR/Config"
    GAME_SETTINGS_FOLDER="$DOLPHIN_DIR/GameSettings"
    GC_PROFILES_DIR="$DOLPHIN_DIR/Config/Profiles/GCPad"
    WII_PROFILES_DIR="$DOLPHIN_DIR/Config/Profiles/Wiimote"
fi

mkdir -p "$GC_PROFILES_DIR"
mkdir -p "$WII_PROFILES_DIR"
mkdir -p "$GAME_SETTINGS_FOLDER"
mkdir -p "$CONFIG_DIR"

cat << 'EOF' > "$CONFIG_DIR/GFX.ini"
[Settings]
Backend = Vulkan
EFBScale = 4
MSAA = 1
SSAA = False
AspectRatio = 0
VSync = True
FastDepthCalc = True
SafeTextureCacheColorSamples = 128
ShaderCompilationMode = 2
WaitForShadersBeforeStarting = False
BackendMultithreading = True
ShaderCompilerThreads = 4
[Enhancements]
MaxAnisotropy = 4
ForceFiltering = True
ArbitraryMipmapDetection = True
DisableCopyFilter = True
[Hacks]
EFBAccessEnable = True
BBoxEnable = False
FORCEPROGRESSIVE = True
EOF

cat << 'EOF' > "$CONFIG_DIR/Dolphin.ini"
[General]
ShowLag = False
ShowFrameCount = False
[Core]
GFXBackend = Vulkan
CPUThread = True
EnableCheats = True
EOF

cat << 'EOF' > "$GC_PROFILES_DIR/GCPad_P1.ini"
[Profile]
Device = Evdev/0/Xbox Gamepad
Buttons/A = `Button 0`
Buttons/B = `Button 1`
Buttons/X = `Button 2`
Buttons/Y = `Button 3`
Buttons/Z = `Button 5`
Buttons/Start = `Button 7`
Main Stick/Dead Zone = 20.
Main Stick/Up = `Axis 1-`
Main Stick/Down = `Axis 1+`
Main Stick/Left = `Axis 0-`
Main Stick/Right = `Axis 0+`
C-Stick/Dead Zone = 20.
C-Stick/Up = `Axis 4-`
C-Stick/Down = `Axis 4+`
C-Stick/Left = `Axis 3-`
C-Stick/Right = `Axis 3+`
Triggers/L = `Axis 2+`
Triggers/R = `Axis 5+`
D-Pad/Up = `Axis 7-`
D-Pad/Down = `Axis 7+`
D-Pad/Left = `Axis 6-`
D-Pad/Right = `Axis 6+`
Options/Always Connected = True
EOF

sed 's/Evdev\/0\/Xbox Gamepad/Evdev\/1\/Xbox Gamepad/g' "$GC_PROFILES_DIR/GCPad_P1.ini" > "$GC_PROFILES_DIR/GCPad_P2.ini"

GC_GAMES=("RSBE01" "RMCE01" "RFEE01" "STKE08" "RB4E08" "SNCE8P")
CLASSIC_GAMES=("SX4E01" "SX3EXJ" "R3RE8P" "SOJE41" "SRSE20")
MOTION_GAMES=("S7AEWR" "RLBEWR" "SLHEWR" "RLGE64" "SF8E01" "RMGE01" "SB4E01" "RNHE41" "RUYE41" "REDE41" "RD2E41" "RPPE41" "RPWZ41" "R5WEA4" "RSRE8P" "RS9E8P" "RM8E01" "SMNE01" "RK5E01" "REXE01")

GC_CONFIG="[Controls]
PadType0 = 6
PadType1 = 6
PadProfile1 = GCPad_P1
PadProfile2 = GCPad_P2
WiimoteSource0 = 0
WiimoteSource1 = 0"

for id in "${GC_GAMES[@]}"; do
    echo "$GC_CONFIG" > "$GAME_SETTINGS_FOLDER/$id.ini"
done

echo "[Dolphin] Applied settings to: $DOLPHIN_DIR"
# ==========================================
# PCSX2 CONTROLLER & GRAPHICS CONFIGURATOR
# ==========================================

# -----------------------------------------------------------------------------
# CUSTOM INSTALLATIONS GUIDE:
# - Installers default to: Documents\PCSX2 or AppData\PCSX2
# - Portable builds store config in: [PCSX2_Folder]\inis\PCSX2.ini
# - If installed on D:\ or E:\ (e.g., "D:\Emulators\PCSX2"), uncomment and edit:
#   $customPath = "D:\Emulators\PCSX2\inis\PCSX2.ini"
# -----------------------------------------------------------------------------
$customPath = $null 

$possiblePaths = @(
    $customPath,
    "$env:USERPROFILE\Documents\PCSX2\inis\PCSX2.ini",
    "$env:APPDATA\PCSX2\inis\PCSX2.ini",
    "${env:ProgramFiles}\PCSX2\inis\PCSX2.ini",
    "${env:ProgramFiles(x86)}\PCSX2\inis\PCSX2.ini",
    "C:\Emulators\PCSX2\inis\PCSX2.ini",
    "D:\Emulators\PCSX2\inis\PCSX2.ini"
)

$pcsx2Ini = $null
foreach ($path in $possiblePaths) {
    if ($path -and (Test-Path (Split-Path -Path $path -Parent))) {
        $pcsx2Ini = $path
        break
    }
}

if (-not $pcsx2Ini) {
    $pcsx2Ini = "$env:USERPROFILE\Documents\PCSX2\inis\PCSX2.ini"
}

$iniDir = Split-Path -Path $pcsx2Ini -Parent
New-Item -ItemType Directory -Path $iniDir -Force | Out-Null

$pcsx2Settings = @'
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
'@

Set-Content -Path $pcsx2Ini -Value $pcsx2Settings -Force
Write-Host "[PCSX2] Applied settings to: $pcsx2Ini" -ForegroundColor Green
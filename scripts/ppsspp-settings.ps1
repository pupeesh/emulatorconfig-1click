# ==========================================
# PPSSPP CONTROLLER & GRAPHICS CONFIGURATOR
# ==========================================

# -----------------------------------------------------------------------------
# CUSTOM INSTALLATIONS GUIDE:
# - Standard Installers default to: Documents\PPSSPP\PSP\SYSTEM
# - Portable ZIP builds default to: [PPSSPP_Folder]\memstick\PSP\SYSTEM
# - If installed on drive D:\ or E:\ (e.g., "D:\Games\PPSSPP"), uncomment and edit:
#   $customDir = "D:\Games\PPSSPP\memstick\PSP\SYSTEM"
# -----------------------------------------------------------------------------
$customDir = $null

$possibleDirs = @(
    $customDir,
    "$env:USERPROFILE\Documents\PPSSPP\PSP\SYSTEM",
    "$env:APPDATA\PPSSPP\PSP\SYSTEM",
    "${env:ProgramFiles}\PPSSPP\memstick\PSP\SYSTEM",
    "${env:ProgramFiles(x86)}\PPSSPP\memstick\PSP\SYSTEM",
    "C:\Emulators\PPSSPP\memstick\PSP\SYSTEM",
    "D:\PPSSPP\memstick\PSP\SYSTEM"
)

$memstickDir = $null
foreach ($dir in $possibleDirs) {
    if ($dir -and (Test-Path $dir)) {
        $memstickDir = $dir
        break
    }
}

if (-not $memstickDir) {
    $memstickDir = "$env:USERPROFILE\Documents\PPSSPP\PSP\SYSTEM"
}

New-Item -ItemType Directory -Path $memstickDir -Force | Out-Null

# --- Graphics & System Optimizations ---
$ppssppIni = "$memstickDir\ppsspp.ini"
$ppssppGfx = @'
[Graphics]
GPUBackend = 3
InternalResolution = 3
AnisotropicFiltering = 4
BufferedRendering = 1

[System]
FastRun = True
'@
Set-Content -Path $ppssppIni -Value $ppssppGfx -Force

# --- Control Mapping ---
$ppssppControls = @'
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
'@

Set-Content -Path "$memstickDir\controls.ini" -Value $ppssppControls -Force
Write-Host "[PPSSPP] Applied settings to: $memstickDir" -ForegroundColor Green
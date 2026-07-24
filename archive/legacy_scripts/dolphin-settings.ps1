# ==========================================
# DOLPHIN GLOBAL SETTINGS & CONTROLLER CONFIGURATOR
# ==========================================

# -----------------------------------------------------------------------------
# CUSTOM INSTALLATIONS GUIDE:
# - Standard installs store config in: %APPDATA%\Dolphin Emulator
# - Portable installs store config in: [Dolphin_Folder]\User
# - If running a portable build on drive D:\ or E:\ (e.g., "D:\Dolphin-x64"),
#   uncomment and edit:
#   $customDolphinDir = "D:\Dolphin-x64"
# -----------------------------------------------------------------------------
$customDolphinDir = $null

$possibleDolphinDirs = @(
    $customDolphinDir,
    "${env:ProgramFiles}\Dolphin",
    "${env:ProgramFiles}\Dolphin-x64",
    "${env:ProgramFiles(x86)}\Dolphin",
    "C:\Emulators\Dolphin-x64",
    "D:\Dolphin-x64"
)

$dolphinDir = $null
foreach ($dir in $possibleDolphinDirs) {
    if ($dir -and (Test-Path $dir)) {
        $dolphinDir = $dir
        break
    }
}

$appDataDir     = "$env:APPDATA\Dolphin Emulator"
$gcProfilesDir  = "$appDataDir\Config\Profiles\GCPad"
$wiiProfilesDir = "$appDataDir\Config\Profiles\Wiimote"
$configDir      = "$appDataDir\Config"

# Detect Portable Mode or fallback to older Documents structure
if ($dolphinDir -and (Test-Path "$dolphinDir\portable.txt")) {
    $gameSettingsFolder = "$dolphinDir\User\GameSettings"
    $configDir          = "$dolphinDir\User\Config"
    $gcProfilesDir      = "$dolphinDir\User\Config\Profiles\GCPad"
    $wiiProfilesDir     = "$dolphinDir\User\Config\Profiles\Wiimote"
} else {
    if (-not (Test-Path $appDataDir) -and (Test-Path "$env:USERPROFILE\Documents\Dolphin Emulator")) {
        $appDataDir     = "$env:USERPROFILE\Documents\Dolphin Emulator"
        $gcProfilesDir  = "$appDataDir\Config\Profiles\GCPad"
        $wiiProfilesDir = "$appDataDir\Config\Profiles\Wiimote"
        $configDir      = "$appDataDir\Config"
    }
    $gameSettingsFolder = "$appDataDir\GameSettings"
}

# Ensure directories exist
New-Item -ItemType Directory -Path $gcProfilesDir -Force | Out-Null
New-Item -ItemType Directory -Path $wiiProfilesDir -Force | Out-Null
New-Item -ItemType Directory -Path $gameSettingsFolder -Force | Out-Null
New-Item -ItemType Directory -Path $configDir -Force | Out-Null

function Write-ProfileFile {
    param ([string]$FilePath, [string]$Content)
    if (Test-Path $FilePath) {
        Write-Host "[Overwriting] " -NoNewline -ForegroundColor Yellow
        Write-Host "$FilePath" -ForegroundColor Gray
    } else {
        Write-Host "[Creating]    " -NoNewline -ForegroundColor Green
        Write-Host "$FilePath" -ForegroundColor White
    }
    Set-Content -Path $FilePath -Value $Content -Force
}

# --- Graphics & System Optimizations ---
$gfxIniContent = @'
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
'@

$dolphinIniContent = @'
[General]
ShowLag = False
ShowFrameCount = False
[Core]
GFXBackend = Vulkan
CPUThread = True
EnableCheats = True
'@

Write-Host "--- Writing Graphics & System Settings ---" -ForegroundColor Cyan
Write-ProfileFile -FilePath "$configDir\GFX.ini" -Content $gfxIniContent
Write-ProfileFile -FilePath "$configDir\Dolphin.ini" -Content $dolphinIniContent

# --- Controller Profiles ---
$gcP1_Profile = @'
[Profile]
Device = XInput/0/Gamepad
Buttons/A = `Button A`
Buttons/B = `Button B`
Buttons/X = `Button X`
Buttons/Y = `Button Y`
Buttons/Z = `Shoulder R`
Buttons/Start = Start
Main Stick/Dead Zone = 20.
Main Stick/Up = `Left Y+`
Main Stick/Down = `Left Y-`
Main Stick/Left = `Left X-`
Main Stick/Right = `Left X+`
C-Stick/Dead Zone = 20.
C-Stick/Up = `Right Y+`
C-Stick/Down = `Right Y-`
C-Stick/Left = `Right X-`
C-Stick/Right = `Right X+`
Triggers/L = `Trigger L`
Triggers/R = `Trigger R`
D-Pad/Up = `Pad N`
D-Pad/Down = `Pad S`
D-Pad/Left = `Pad W`
D-Pad/Right = `Pad E`
Options/Always Connected = True
'@

$gcP2_Profile = $gcP1_Profile -replace "XInput/0/Gamepad", "XInput/1/Gamepad"

$motionP1_Profile = @'
[Profile]
Device = XInput/0/Gamepad
Buttons/A = `Button A`
Buttons/B = `Button X`
Buttons/1 = `Button B`
Buttons/2 = `Button Y`
Buttons/- = Back
Buttons/+ = Start
Buttons/Home = Guide
D-Pad/Up = `Pad N`
D-Pad/Down = `Pad S`
D-Pad/Left = `Pad W`
D-Pad/Right = `Pad E`
IR/Dead Zone = 25.
IR/Relative Input = True
IR/Up = `Right Y+`
IR/Down = `Right Y-`
IR/Left = `Right X-`
IR/Right = `Right X+`
Shake/X = `Shoulder R`
Shake/Y = `Shoulder R`
Shake/Z = `Shoulder R`
Extension = Nunchuk
Nunchuk/Buttons/C = `Shoulder L`
Nunchuk/Buttons/Z = `Trigger L`
Nunchuk/Stick/Dead Zone = 25.
Nunchuk/Stick/Up = `Left Y+`
Nunchuk/Stick/Down = `Left Y-`
Nunchuk/Stick/Left = `Left X-`
Nunchuk/Stick/Right = `Left X+`
Nunchuk/Shake/X = `Thumb R`
Nunchuk/Shake/Y = `Thumb R`
Nunchuk/Shake/Z = `Thumb R`
'@

$motionP2_Profile = $motionP1_Profile -replace "XInput/0/Gamepad", "XInput/1/Gamepad"

$classicP1_Profile = @'
[Profile]
Device = XInput/0/Gamepad
Extension = Classic
Classic/Buttons/A = `Button A`
Classic/Buttons/B = `Button B`
Classic/Buttons/X = `Button X`
Classic/Buttons/Y = `Button Y`
Classic/Buttons/- = Back
Classic/Buttons/+ = Start
Classic/Buttons/ZL = `Shoulder L`
Classic/Buttons/ZR = `Shoulder R`
Classic/Triggers/L = `Trigger L`
Classic/Triggers/R = `Trigger R`
Classic/D-Pad/Up = `Pad N`
Classic/D-Pad/Down = `Pad S`
Classic/D-Pad/Left = `Pad W`
Classic/D-Pad/Right = `Pad E`
Classic/Left Stick/Up = `Left Y+`
Classic/Left Stick/Down = `Left Y-`
Classic/Left Stick/Left = `Left X-`
Classic/Left Stick/Right = `Left X+`
Classic/Right Stick/Up = `Right Y+`
Classic/Right Stick/Down = `Right Y-`
Classic/Right Stick/Left = `Right X-`
Classic/Right Stick/Right = `Right X+`
'@

$classicP2_Profile = $classicP1_Profile -replace "XInput/0/Gamepad", "XInput/1/Gamepad"

Write-Host "`n--- Writing Controller Profile Files ---" -ForegroundColor Cyan
Write-ProfileFile -FilePath "$gcProfilesDir\GCPad_P1.ini" -Content $gcP1_Profile
Write-ProfileFile -FilePath "$gcProfilesDir\GCPad_P2.ini" -Content $gcP2_Profile
Write-ProfileFile -FilePath "$wiiProfilesDir\Classic_P1.ini" -Content $classicP1_Profile
Write-ProfileFile -FilePath "$wiiProfilesDir\Classic_P2.ini" -Content $classicP2_Profile
Write-ProfileFile -FilePath "$wiiProfilesDir\Motion_P1.ini" -Content $motionP1_Profile
Write-ProfileFile -FilePath "$wiiProfilesDir\Motion_P2.ini" -Content $motionP2_Profile

# --- Categorized Game Setup ---
$gcGames      = @("RSBE01", "RMCE01", "RFEE01", "STKE08", "RB4E08", "SNCE8P")
$classicGames = @("SX4E01", "SX3EXJ", "R3RE8P", "SOJE41", "SRSE20")
$motionGames  = @("S7AEWR", "RLBEWR", "SLHEWR", "RLGE64", "SF8E01", "RMGE01", "SB4E01", "RNHE41", "RUYE41", "REDE41", "RD2E41", "RPPE41", "RPWZ41", "R5WEA4", "RSRE8P", "RS9E8P", "RM8E01", "SMNE01", "RK5E01", "REXE01")

$gcConfig = "[Controls]`nPadType0 = 6`nPadType1 = 6`nPadProfile1 = GCPad_P1`nPadProfile2 = GCPad_P2`nWiimoteSource0 = 0`nWiimoteSource1 = 0"
$classicConfig = "[Controls]`nPadType0 = 0`nPadType1 = 0`nWiimoteSource0 = 1`nWiimoteSource1 = 1`nWiimoteProfile1 = Classic_P1`nWiimoteProfile2 = Classic_P2"
$motionConfig = "[Controls]`nPadType0 = 0`nPadType1 = 0`nWiimoteSource0 = 1`nWiimoteSource1 = 1`nWiimoteProfile1 = Motion_P1`nWiimoteProfile2 = Motion_P2"

Write-Host "`n--- Writing Per-Game Control Settings ---" -ForegroundColor Cyan
foreach ($id in $gcGames) { Write-ProfileFile -FilePath "$gameSettingsFolder\$id.ini" -Content $gcConfig }
foreach ($id in $classicGames) { Write-ProfileFile -FilePath "$gameSettingsFolder\$id.ini" -Content $classicConfig }
foreach ($id in $motionGames) { Write-ProfileFile -FilePath "$gameSettingsFolder\$id.ini" -Content $motionConfig }

Write-Host "`n[Dolphin] Execution Complete!" -ForegroundColor Green
# ==========================================
# CEMU GLOBAL SETTINGS & CONTROLLER CONFIGURATOR
# ==========================================

# -----------------------------------------------------------------------------
# CUSTOM INSTALLATIONS GUIDE:
# - Modern Cemu defaults to: %APPDATA%\Cemu or %LOCALAPPDATA%\Cemu
# - Portable/Standalone installs use the folder containing Cemu.exe
# - If installed on drive D:\ or E:\ (e.g., "D:\Cemu"), uncomment and edit:
#   $customDir = "D:\Cemu"
# -----------------------------------------------------------------------------
$customDir = $null

$possibleDirs = @(
    $customDir,
    "$env:APPDATA\Cemu",
    "$env:LOCALAPPDATA\Cemu",
    "${env:ProgramFiles}\Cemu",
    "${env:ProgramFiles(x86)}\Cemu",
    "C:\Cemu",
    "C:\Emulators\Cemu",
    "D:\Cemu"
)

$cemuDir = $null
foreach ($dir in $possibleDirs) {
    if ($dir -and (Test-Path $dir)) {
        $cemuDir = $dir
        break
    }
}

if (-not $cemuDir) {
    $cemuDir = "$env:APPDATA\Cemu"
}

$profilesDir = "$cemuDir\controllerProfiles"

New-Item -ItemType Directory -Path $cemuDir -Force | Out-Null
New-Item -ItemType Directory -Path $profilesDir -Force | Out-Null

# --- Global Settings ---
$cemuSettings = @'
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
'@
Set-Content -Path "$cemuDir\settings.xml" -Value $cemuSettings -Force

# --- Controller Profiles ---
$cemuProfileP1 = @'
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
'@

$cemuProfileP2 = $cemuProfileP1 -replace 'value="Controller 1"', 'value="Controller 2"'

Set-Content -Path "$profilesDir\P1_ProController.xml" -Value $cemuProfileP1 -Force
Set-Content -Path "$profilesDir\P2_ProController.xml" -Value $cemuProfileP2 -Force
Write-Host "[Cemu] Applied settings to: $cemuDir" -ForegroundColor Green
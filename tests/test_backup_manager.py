import os
import sys
import time
import shutil

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from core.backup_manager import BackupManager

def test_backup_manager():
    print("--- 1. Setting up Mock Files ---")
    mock_sys_dir = os.path.abspath(os.path.join("tests", "mock_sys", "dolphin"))
    config_dir = os.path.join(mock_sys_dir, "Config")
    games_dir = os.path.join(mock_sys_dir, "GameSettings")

    os.makedirs(config_dir, exist_ok=True)
    os.makedirs(games_dir, exist_ok=True)

    gfx_ini = os.path.join(config_dir, "GFX.ini")
    pad_ini = os.path.join(config_dir, "GCPadNew.ini")
    game_ini = os.path.join(games_dir, "GZ2E01.ini")

    with open(gfx_ini, "w") as f: f.write("[GFX]\nBackend = OpenGL\n")
    with open(pad_ini, "w") as f: f.write("[GCPad1]\nDevice = Keyboard\n")
    with open(game_ini, "w") as f: f.write("[Core]\nGFXBackend = OpenGL\n")

    targets = {
        "system-settings": [gfx_ini],
        "global-controls": [pad_ini],
        "pergame-files": [game_ini]
    }

    print("--- 2. Testing Centralized Snapshot Creation & 5-Limit Pruning ---")
    vault_dir = os.path.join("tests", "mock_vault")
    vault = BackupManager(base_backup_dir=vault_dir, max_backups=5)

    last_snapshot = None
    for i in range(7):
        last_snapshot = vault.create_backup_snapshot(targets)
        print(f"Created Snapshot {i+1}: {os.path.basename(last_snapshot)}")
        time.sleep(1.1)

    snapshots_left = [d for d in os.listdir(vault_dir) if d.startswith("bak_")]
    print(f"\nSnapshots currently stored in vault: {len(snapshots_left)} (Limit is 5)")
    assert len(snapshots_left) == 5, "Pruning failed! More than 5 backups found."

    print("\n--- 3. Testing Restore Snapshot Logic ---")
    with open(gfx_ini, "w") as f: f.write("[GFX]\nBackend = CORRUPTED\n")

    dest_mappings = {
        "system-settings": config_dir,
        "global-controls": config_dir,
        "pergame-files": games_dir
    }

    success = vault.restore_snapshot(last_snapshot, dest_mappings)
    print(f"Restore executed: {success}")

    with open(gfx_ini, "r") as f:
        content = f.read()
        print(f"Restored GFX.ini Content:\n{content}")
        assert "OpenGL" in content, "Restore failed! Content not reverted."

    print("\nBackup & Auto-Pruning Engine Passed Successfully!")

    # Cleanup temporary test vault directory
    shutil.rmtree(vault_dir, ignore_errors=True)

if __name__ == "__main__":
    test_backup_manager()

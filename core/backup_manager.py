import os
import shutil
from datetime import datetime

class BackupManager:
    def __init__(self, base_backup_dir=".backups", max_backups=5):
        self.base_backup_dir = os.path.abspath(base_backup_dir)
        self.max_backups = max_backups
        os.makedirs(self.base_backup_dir, exist_ok=True)

    def create_backup_snapshot(self, target_files_dict):
        """
        Creates a categorized backup snapshot.
        target_files_dict format:
        {
            "system-settings": ["/path/to/Dolphin.ini", "/path/to/GFX.ini"],
            "global-controls": ["/path/to/GCPadNew.ini"],
            "pergame-files": ["/path/to/GameSettings/GZ2E01.ini"]
        }
        """
        timestamp = datetime.now().strftime("bak_%Y%m%d_%H%M%S")
        snapshot_dir = os.path.join(self.base_backup_dir, timestamp)

        backed_up_count = 0
        for category, file_paths in target_files_dict.items():
            category_dir = os.path.join(snapshot_dir, category)
            for file_path in file_paths:
                if file_path and os.path.exists(file_path):
                    os.makedirs(category_dir, exist_ok=True)
                    shutil.copy2(file_path, os.path.join(category_dir, os.path.basename(file_path)))
                    backed_up_count += 1

        if backed_up_count > 0:
            self._prune_old_backups()
            return snapshot_dir
        else:
            if os.path.exists(snapshot_dir):
                os.rmdir(snapshot_dir)
            return None

    def _prune_old_backups(self):
        """Enforces keeping only the 'max_backups' most recent snapshots."""
        snapshots = sorted([
            os.path.join(self.base_backup_dir, d)
            for d in os.listdir(self.base_backup_dir)
            if os.path.isdir(os.path.join(self.base_backup_dir, d)) and d.startswith("bak_")
        ])

        while len(snapshots) > self.max_backups:
            oldest = snapshots.pop(0)
            shutil.rmtree(oldest)

    def restore_snapshot(self, snapshot_path, destination_mappings):
        """
        Restores files from a snapshot folder to target directories.
        destination_mappings format:
        {
            "system-settings": "/path/to/emulator/Config",
            "global-controls": "/path/to/emulator/Config",
            "pergame-files": "/path/to/emulator/GameSettings"
        }
        """
        if not os.path.exists(snapshot_path):
            return False

        restored_count = 0
        for category, target_dir in destination_mappings.items():
            category_dir = os.path.join(snapshot_path, category)
            if os.path.exists(category_dir):
                os.makedirs(target_dir, exist_ok=True)
                for file_name in os.listdir(category_dir):
                    src_file = os.path.join(category_dir, file_name)
                    dst_file = os.path.join(target_dir, file_name)
                    if os.path.isfile(src_file):
                        shutil.copy2(src_file, dst_file)
                        restored_count += 1
        return restored_count > 0

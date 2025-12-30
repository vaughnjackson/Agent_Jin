"""
Data Manager Module for Digital Life Assistant.

Handles JSON persistence, data validation, backup/restore,
and API integration hooks.
"""

import json
import os
from typing import Dict, List, Any, Optional
from datetime import datetime
from pathlib import Path


class DataManager:
    """Manage data persistence and backups."""

    def __init__(self, data_dir: Optional[str] = None):
        """
        Initialize DataManager.

        Args:
            data_dir: Directory for data storage (defaults to ~/.claude/skills/digital-life-assistant/data/)
        """
        if data_dir is None:
            home = Path.home()
            self.data_dir = home / ".claude" / "skills" / "digital-life-assistant" / "data"
        else:
            self.data_dir = Path(data_dir)

        # Create data directory if it doesn't exist
        self.data_dir.mkdir(parents=True, exist_ok=True)

        # Data file paths
        self.data_files = {
            "tasks": self.data_dir / "tasks.json",
            "habits": self.data_dir / "habits.json",
            "progress": self.data_dir / "progress.json",
            "schedule": self.data_dir / "schedule.json",
            "reminders": self.data_dir / "reminders.json",
        }

        # Config file path
        self.config_file = self.data_dir.parent / "config.json"

        # Backup directory
        self.backup_dir = self.data_dir / "backups"
        self.backup_dir.mkdir(exist_ok=True)

        # Initialize data files if they don't exist
        self._initialize_data_files()

    def _initialize_data_files(self) -> None:
        """Initialize empty data files if they don't exist."""
        for data_type, file_path in self.data_files.items():
            if not file_path.exists():
                self._write_json(file_path, [])

    def load_data(self, data_type: str) -> List[Dict[str, Any]]:
        """
        Load data from JSON file.

        Args:
            data_type: Type of data to load (tasks, habits, progress, schedule, reminders)

        Returns:
            List of data objects
        """
        if data_type not in self.data_files:
            raise ValueError(f"Unknown data type: {data_type}")

        file_path = self.data_files[data_type]

        try:
            return self._read_json(file_path)
        except (json.JSONDecodeError, FileNotFoundError):
            # Return empty list if file is corrupted or missing
            return []

    def save_data(self, data_type: str, data: List[Dict[str, Any]]) -> None:
        """
        Save data to JSON file with automatic backup.

        Args:
            data_type: Type of data to save
            data: Data to save
        """
        if data_type not in self.data_files:
            raise ValueError(f"Unknown data type: {data_type}")

        file_path = self.data_files[data_type]

        # Create backup before saving
        self._create_backup(data_type)

        # Save data
        self._write_json(file_path, data)

    def _read_json(self, file_path: Path) -> Any:
        """Read JSON from file."""
        with open(file_path, 'r') as f:
            return json.load(f)

    def _write_json(self, file_path: Path, data: Any) -> None:
        """Write JSON to file with pretty formatting."""
        with open(file_path, 'w') as f:
            json.dump(data, f, indent=2, ensure_ascii=False)

    def _create_backup(self, data_type: str) -> None:
        """
        Create timestamped backup of data file.

        Args:
            data_type: Type of data to backup
        """
        file_path = self.data_files[data_type]

        if not file_path.exists():
            return

        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        backup_file = self.backup_dir / f"{data_type}_{timestamp}.json"

        # Copy current file to backup
        data = self._read_json(file_path)
        self._write_json(backup_file, data)

        # Clean old backups (keep last 30)
        self._cleanup_old_backups(data_type, keep_count=30)

    def _cleanup_old_backups(self, data_type: str, keep_count: int = 30) -> None:
        """
        Remove old backup files, keeping only the most recent N.

        Args:
            data_type: Type of data
            keep_count: Number of backups to keep
        """
        backup_pattern = f"{data_type}_*.json"
        backup_files = sorted(self.backup_dir.glob(backup_pattern))

        # Remove oldest backups if we have more than keep_count
        if len(backup_files) > keep_count:
            for old_backup in backup_files[:-keep_count]:
                old_backup.unlink()

    def restore_from_backup(
        self,
        data_type: str,
        backup_timestamp: Optional[str] = None
    ) -> bool:
        """
        Restore data from backup.

        Args:
            data_type: Type of data to restore
            backup_timestamp: Specific backup timestamp (YYYYMMDD_HHMMSS), or None for most recent

        Returns:
            True if restored successfully, False otherwise
        """
        backup_pattern = f"{data_type}_*.json"
        backup_files = sorted(self.backup_dir.glob(backup_pattern), reverse=True)

        if not backup_files:
            return False

        # Find backup file
        backup_file = None
        if backup_timestamp:
            backup_file = self.backup_dir / f"{data_type}_{backup_timestamp}.json"
            if not backup_file.exists():
                return False
        else:
            # Use most recent backup
            backup_file = backup_files[0]

        # Restore from backup
        try:
            data = self._read_json(backup_file)
            file_path = self.data_files[data_type]
            self._write_json(file_path, data)
            return True
        except (json.JSONDecodeError, FileNotFoundError):
            return False

    def load_config(self) -> Dict[str, Any]:
        """
        Load configuration file.

        Returns:
            Configuration dictionary
        """
        if not self.config_file.exists():
            # Return default config
            default_config = {
                "google_calendar": {
                    "enabled": False,
                    "credentials_path": "",
                    "token_path": "",
                },
                "notion": {
                    "enabled": False,
                    "api_token": "",
                    "database_id": "",
                },
                "todoist": {
                    "enabled": False,
                    "api_token": "",
                },
            }
            return default_config

        try:
            return self._read_json(self.config_file)
        except (json.JSONDecodeError, FileNotFoundError):
            return {}

    def save_config(self, config: Dict[str, Any]) -> None:
        """
        Save configuration file.

        Args:
            config: Configuration dictionary
        """
        self._write_json(self.config_file, config)

    def export_all_data(self, export_dir: Optional[str] = None) -> str:
        """
        Export all data to a directory.

        Args:
            export_dir: Directory to export to (defaults to data_dir/exports/)

        Returns:
            Path to export directory
        """
        if export_dir is None:
            export_dir = self.data_dir / "exports" / datetime.now().strftime("%Y%m%d_%H%M%S")
        else:
            export_dir = Path(export_dir)

        export_dir.mkdir(parents=True, exist_ok=True)

        # Export all data files
        for data_type, file_path in self.data_files.items():
            if file_path.exists():
                data = self._read_json(file_path)
                export_file = export_dir / f"{data_type}.json"
                self._write_json(export_file, data)

        # Export config (without sensitive tokens)
        config = self.load_config()
        safe_config = self._sanitize_config(config)
        export_config_file = export_dir / "config.json"
        self._write_json(export_config_file, safe_config)

        return str(export_dir)

    def _sanitize_config(self, config: Dict[str, Any]) -> Dict[str, Any]:
        """
        Remove sensitive information from config for export.

        Args:
            config: Original config

        Returns:
            Sanitized config
        """
        safe_config = config.copy()

        # Remove API tokens
        if "google_calendar" in safe_config:
            safe_config["google_calendar"] = {
                "enabled": safe_config["google_calendar"].get("enabled", False)
            }

        if "notion" in safe_config:
            safe_config["notion"] = {
                "enabled": safe_config["notion"].get("enabled", False)
            }

        if "todoist" in safe_config:
            safe_config["todoist"] = {
                "enabled": safe_config["todoist"].get("enabled", False)
            }

        return safe_config

    def import_data(self, import_dir: str) -> Dict[str, bool]:
        """
        Import data from a directory.

        Args:
            import_dir: Directory containing data files to import

        Returns:
            Dictionary showing which data types were imported successfully
        """
        import_path = Path(import_dir)
        results = {}

        for data_type in self.data_files.keys():
            import_file = import_path / f"{data_type}.json"

            if import_file.exists():
                try:
                    data = self._read_json(import_file)
                    self.save_data(data_type, data)
                    results[data_type] = True
                except (json.JSONDecodeError, ValueError):
                    results[data_type] = False
            else:
                results[data_type] = False

        return results

    def get_data_stats(self) -> Dict[str, Any]:
        """
        Get statistics about stored data.

        Returns:
            Statistics dictionary
        """
        stats = {
            "data_directory": str(self.data_dir),
            "total_backups": len(list(self.backup_dir.glob("*.json"))),
            "data_files": {},
        }

        for data_type, file_path in self.data_files.items():
            if file_path.exists():
                data = self.load_data(data_type)
                file_size = file_path.stat().st_size

                stats["data_files"][data_type] = {
                    "count": len(data),
                    "size_bytes": file_size,
                    "last_modified": datetime.fromtimestamp(
                        file_path.stat().st_mtime
                    ).isoformat(),
                }

        return stats

    def validate_data_integrity(self) -> Dict[str, Any]:
        """
        Validate data integrity across all data files.

        Returns:
            Validation results
        """
        results = {
            "valid": True,
            "errors": [],
            "warnings": [],
        }

        for data_type, file_path in self.data_files.items():
            if not file_path.exists():
                results["warnings"].append(f"{data_type}.json does not exist")
                continue

            try:
                data = self._read_json(file_path)

                if not isinstance(data, list):
                    results["valid"] = False
                    results["errors"].append(f"{data_type}.json is not a list")
                    continue

                # Check for duplicate IDs
                ids = [item.get("id") for item in data if "id" in item]
                if len(ids) != len(set(ids)):
                    results["valid"] = False
                    results["errors"].append(f"{data_type}.json has duplicate IDs")

            except json.JSONDecodeError:
                results["valid"] = False
                results["errors"].append(f"{data_type}.json has invalid JSON")

        return results

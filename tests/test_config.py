"""
Test configuration management
"""
import json
from pathlib import Path
import tempfile
import shutil

import pytest
from simple_yt_dlp.config import Config, migrate_old_config


class TestConfig:
    """Test Config class"""

    @pytest.fixture
    def temp_config_path(self):
        """Create a temporary config file"""
        temp_dir = Path(tempfile.mkdtemp())
        config_path = temp_dir / "test_config.json"
        yield config_path
        # Cleanup
        if temp_dir.exists():
            shutil.rmtree(temp_dir)

    def test_config_initialization(self, temp_config_path):
        """Test config initialization"""
        config = Config(config_path=temp_config_path)
        assert config.config_path == temp_config_path
        assert config.get("test_key") is None
        assert config.get("test_key", "default") == "default"

    def test_config_set_get(self, temp_config_path):
        """Test setting and getting config values"""
        config = Config(config_path=temp_config_path)

        config.set("test_key", "test_value")
        assert config.get("test_key") == "test_value"

        # Verify persistence
        config2 = Config(config_path=temp_config_path)
        assert config2.get("test_key") == "test_value"

    def test_download_dir_property(self, temp_config_path):
        """Test download_dir property"""
        config = Config(config_path=temp_config_path)
        test_dir = Path("/tmp/test_downloads")

        config.download_dir = test_dir
        assert config.download_dir == test_dir

    def test_last_format_property(self, temp_config_path):
        """Test last_format property"""
        config = Config(config_path=temp_config_path)

        config.last_format = "mp4_best"
        assert config.last_format == "mp4_best"


class TestConfigMigration:
    """Test old config migration"""

    @pytest.fixture
    def old_config_path(self):
        """Create a temporary old config file"""
        temp_dir = Path(tempfile.mkdtemp())
        old_path = temp_dir / ".simple_yt_dlp_config.json"

        # Create old config
        old_data = {
            "download_dir": "/tmp/old_downloads",
            "last_format": "mkv_best",
        }
        with open(old_path, "w") as f:
            json.dump(old_data, f)

        yield old_path

        # Cleanup
        if temp_dir.exists():
            shutil.rmtree(temp_dir)

    @pytest.fixture
    def new_config(self):
        """Create a new config for migration"""
        temp_dir = Path(tempfile.mkdtemp())
        config_path = temp_dir / "new_config.json"
        config = Config(config_path=config_path)
        yield config
        # Cleanup
        if temp_dir.exists():
            shutil.rmtree(temp_dir)

    def test_migrate_old_config(self, old_config_path, new_config):
        """Test migration from old config"""
        # Before migration, new config should be empty
        assert new_config.download_dir is None
        assert new_config.last_format is None

        # Migrate
        success = migrate_old_config(old_config_path, new_config)
        assert success is True

        # After migration
        assert str(new_config.download_dir) == "/tmp/old_downloads"
        assert new_config.last_format == "mkv_best"

        # Old config should be backed up
        backup_path = old_config_path.with_suffix(".json.bak")
        assert backup_path.exists()
        assert not old_config_path.exists()

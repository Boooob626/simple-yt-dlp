"""Config package - Configuration management"""
from .manager import Config, migrate_old_config

__all__ = ["Config", "migrate_old_config"]

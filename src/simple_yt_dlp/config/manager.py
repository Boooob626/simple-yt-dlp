"""
Configuration Manager - 配置管理（带向后兼容）
Configuration Manager with backward compatibility support
"""
import json
import logging
from pathlib import Path
from typing import Any, Optional

# 模块级日志（用于配置相关的调试）
logger = logging.getLogger("simple-yt-dlp.config")


# 旧配置路径（用于迁移）
OLD_CONFIG_PATH = Path.home() / ".simple_yt_dlp_config.json"


class Config:
    """
    配置管理类 - Handles persistent configuration storage

    支持的配置项:
    - download_dir: 下载目录路径
    - last_format: 上次选择的格式
    - cookie_file: Cookie 文件路径（可选）
    """

    def __init__(self, config_path: Optional[Path] = None):
        """
        初始化配置管理器

        Args:
            config_path: 配置文件路径，默认为 ~/.config/simple-yt-dlp/config.json
        """
        if config_path is None:
            config_dir = Path.home() / ".config" / "simple-yt-dlp"
            config_dir.mkdir(parents=True, exist_ok=True)
            config_path = config_dir / "config.json"

        self.config_path = config_path
        self._config: dict[str, Any] = {}
        self._load()

        # 尝试从旧配置迁移
        self._try_migrate_old_config()

    def _load(self) -> None:
        """从文件加载配置"""
        if self.config_path.exists():
            try:
                with open(self.config_path, "r", encoding="utf-8") as f:
                    self._config = json.load(f)
                logger.debug(f"配置已加载: {self.config_path}")
            except (json.JSONDecodeError, IOError) as e:
                logger.warning(f"配置文件损坏，使用默认配置: {e}")
                self._config = {}
        else:
            logger.debug("配置文件不存在，使用默认配置")

    def _save(self) -> None:
        """保存配置到文件"""
        try:
            with open(self.config_path, "w", encoding="utf-8") as f:
                json.dump(self._config, f, indent=2, ensure_ascii=False)
            logger.debug(f"配置已保存: {self.config_path}")
        except IOError as e:
            logger.error(f"配置保存失败: {e}")

    def _try_migrate_old_config(self) -> None:
        """
        尝试从旧配置文件迁移用户设置

        旧配置路径: ~/.simple_yt_dlp_config.json
        新配置路径: ~/.config/simple-yt-dlp/config.json
        """
        # 如果新配置为空且旧配置存在，进行迁移
        if not self._config and OLD_CONFIG_PATH.exists():
            migrate_old_config(OLD_CONFIG_PATH, self)

    def get(self, key: str, default: Any = None) -> Any:
        """
        获取配置值

        Args:
            key: 配置键
            default: 默认值

        Returns:
            配置值，如果不存在则返回默认值
        """
        return self._config.get(key, default)

    def set(self, key: str, value: Any) -> None:
        """
        设置配置值并保存

        Args:
            key: 配置键
            value: 配置值
        """
        self._config[key] = value
        self._save()

    @property
    def download_dir(self) -> Optional[Path]:
        """获取下载目录配置"""
        path_str = self.get("download_dir")
        return Path(path_str) if path_str else None

    @download_dir.setter
    def download_dir(self, path: Path) -> None:
        """设置下载目录配置"""
        self.set("download_dir", str(path))

    @property
    def last_format(self) -> Optional[str]:
        """获取上次选择的格式"""
        return self.get("last_format")

    @last_format.setter
    def last_format(self, format_str: str) -> None:
        """设置上次选择的格式"""
        self.set("last_format", format_str)

    @property
    def cookie_file(self) -> Optional[Path]:
        """获取 Cookie 文件路径"""
        path_str = self.get("cookie_file")
        return Path(path_str) if path_str else None

    @cookie_file.setter
    def cookie_file(self, path: Path) -> None:
        """设置 Cookie 文件路径"""
        self.set("cookie_file", str(path))


def migrate_old_config(old_path: Path, new_config: Config) -> bool:
    """
    从旧配置文件迁移用户设置

    Args:
        old_path: 旧配置文件路径
        new_config: 新配置管理器实例

    Returns:
        迁移是否成功
    """
    if not old_path.exists():
        return False

    try:
        with open(old_path, "r", encoding="utf-8") as f:
            old_data = json.load(f)

        # 迁移关键字段
        migrated = False
        if "download_dir" in old_data and old_data["download_dir"]:
            new_config.download_dir = Path(old_data["download_dir"])
            migrated = True
            logger.info(f"已迁移下载目录: {old_data['download_dir']}")

        if "last_format" in old_data and old_data["last_format"]:
            new_config.last_format = old_data["last_format"]
            migrated = True
            logger.info(f"已迁移上次格式: {old_data['last_format']}")

        # 保留旧文件作为备份
        backup_path = old_path.with_suffix(".json.bak")
        old_path.rename(backup_path)
        logger.info(f"旧配置已备份到: {backup_path}")

        return migrated

    except (json.JSONDecodeError, IOError) as e:
        logger.error(f"配置迁移失败: {e}")
        return False

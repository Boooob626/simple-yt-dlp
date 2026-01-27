"""
Logging System - 日志系统
File-based logging for yt-dlp core logic (separate from Textual UI logs)

日志分离策略:
- UI 事件 → 使用 Textual 的 self.log() (内置)
- yt-dlp 核心逻辑 → 使用此处的 logger (写入文件)
"""
import logging
from pathlib import Path


def setup_logging(
    log_dir: Path | None = None,
    log_level: int = logging.DEBUG,
) -> logging.Logger:
    """
    配置文件日志系统 - 用于 yt-dlp 核心逻辑

    Args:
        log_dir: 日志目录，默认为 ~/.cache/simple-yt-dlp
        log_level: 日志级别

    Returns:
        配置好的 logger 实例
    """
    if log_dir is None:
        log_dir = Path.home() / ".cache" / "simple-yt-dlp"

    log_dir.mkdir(parents=True, exist_ok=True)

    logger = logging.getLogger("simple-yt-dlp")
    logger.setLevel(log_level)

    # 避免重复添加处理器
    if logger.handlers:
        return logger

    # 文件处理器
    log_file = log_dir / "debug.log"
    file_handler = logging.FileHandler(log_file, encoding="utf-8")
    file_handler.setLevel(log_level)

    # 日志格式
    formatter = logging.Formatter(
        "%(asctime)s - %(name)s - %(levelname)s - %(message)s",
        datefmt="%Y-%m-%d %H:%M:%S"
    )
    file_handler.setFormatter(formatter)

    logger.addHandler(file_handler)

    # 静默初始化日志
    logger.debug("=" * 60)
    logger.debug("日志系统初始化完成")
    logger.debug(f"日志文件: {log_file}")
    logger.debug("=" * 60)

    return logger


def get_logger(name: str = "simple-yt-dlp") -> logging.Logger:
    """
    获取 logger 实例

    Args:
        name: logger 名称

    Returns:
        logger 实例
    """
    return logging.getLogger(name)


# 自动初始化默认 logger
_default_logger: logging.Logger | None = None


def get_default_logger() -> logging.Logger:
    """
    获取默认 logger（自动初始化）

    Returns:
        默认 logger 实例
    """
    global _default_logger
    if _default_logger is None:
        _default_logger = setup_logging()
    return _default_logger

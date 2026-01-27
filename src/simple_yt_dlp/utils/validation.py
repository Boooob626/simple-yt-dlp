"""
Validation Utils - 验证工具函数
URL validation and filename sanitization utilities
"""
import re
from pathlib import Path


def validate_youtube_url(url: str) -> tuple[bool, str]:
    """
    验证 YouTube URL

    Args:
        url: 待验证的 URL

    Returns:
        (是否有效, 错误消息)
    """
    if not url:
        return False, "请输入 YouTube URL"

    # 基本域名检查
    if "youtube.com" not in url and "youtu.be" not in url:
        return False, "URL 必须来自 YouTube"

    # 基本 URL 格式检查
    youtube_pattern = re.compile(
        r"^(https?://)?(www\.)?(youtube\.com|youtu\.be)/.+$"
    )
    if not youtube_pattern.match(url):
        return False, "无效的 YouTube URL 格式"

    return True, ""


def sanitize_filename(filename: str, max_length: int = 70) -> str:
    """
    清理文件名（移除非法字符）

    Args:
        filename: 原始文件名
        max_length: 最大长度

    Returns:
        清理后的文件名
    """
    # 移除非法字符
    cleaned = re.sub(r'[^\w\s.-]', '', filename)

    # 限制长度
    if len(cleaned) > max_length:
        cleaned = cleaned[:max_length] + "..."

    return cleaned.strip()


def is_valid_directory_path(path: str) -> bool:
    """
    验证目录路径是否有效

    Args:
        path: 目录路径字符串

    Returns:
        路径是否有效
    """
    try:
        p = Path(path)
        # 检查路径是否可解析
        p.expanduser().resolve()
        return True
    except (OSError, RuntimeError, ValueError):
        return False

"""
Cookie Support - Cookie 支持工具
Cookie file management for age-restricted and private videos
"""
import logging
from pathlib import Path

logger = logging.getLogger("simple-yt-dlp.cookies")


# 默认 Cookie 文件位置
DEFAULT_COOKIE_PATHS = [
    Path("cookies.txt"),
    Path.home() / ".config" / "simple-yt-dlp" / "cookies.txt",
]


def find_cookie_file(
    custom_path: Path | None = None,
    search_paths: list[Path] | None = None,
) -> Path | None:
    """
    查找 Cookie 文件

    Args:
        custom_path: 自定义 Cookie 文件路径
        search_paths: 搜索路径列表

    Returns:
        找到的 Cookie 文件路径，未找到返回 None
    """
    # 如果指定了自定义路径，直接检查
    if custom_path:
        if custom_path.exists() and custom_path.is_file():
            logger.info(f"使用自定义 Cookie 文件: {custom_path}")
            return custom_path
        else:
            logger.warning(f"指定的 Cookie 文件不存在: {custom_path}")
            return None

    # 在默认位置搜索
    search_paths = search_paths or DEFAULT_COOKIE_PATHS
    for path in search_paths:
        if path.exists() and path.is_file():
            logger.info(f"找到 Cookie 文件: {path}")
            return path

    logger.debug("未找到 Cookie 文件")
    return None


def validate_cookie_file(cookie_path: Path) -> tuple[bool, str]:
    """
    验证 Cookie 文件是否有效

    Args:
        cookie_path: Cookie 文件路径

    Returns:
        (是否有效, 错误消息)
    """
    if not cookie_path.exists():
        return False, "Cookie 文件不存在"

    if not cookie_path.is_file():
        return False, "Cookie 路径不是文件"

    # 检查文件是否可读
    try:
        with open(cookie_path, "r", encoding="utf-8") as f:
            content = f.read()
            # 基本格式检查：Netscape cookie 格式应该包含特定字段
            if not content.strip():
                return False, "Cookie 文件为空"

            # 检查是否看起来像有效的 cookie 文件
            lines = content.strip().split("\n")
            # 跳过注释行
            data_lines = [l for l in lines if not l.startswith("#")]
            if not data_lines:
                return False, "Cookie 文件无有效数据"

        return True, ""
    except Exception as e:
        return False, f"读取 Cookie 文件失败: {e}"


def get_cookie_file_for_ytdlp(cookie_path: Path | None = None) -> str | None:
    """
    获取用于 yt-dlp 的 Cookie 文件路径

    Args:
        cookie_path: 指定的 Cookie 文件路径

    Returns:
        Cookie 文件路径字符串，无效时返回 None
    """
    path = cookie_path or find_cookie_file()
    if path:
        valid, msg = validate_cookie_file(path)
        if valid:
            return str(path)
        else:
            logger.warning(f"Cookie 文件无效: {msg}")
            return None

    return None


class CookieManager:
    """
    Cookie 管理器 - 管理和验证 Cookie 文件
    """

    def __init__(self, cookie_path: Path | None = None):
        """
        初始化 Cookie 管理器

        Args:
            cookie_path: Cookie 文件路径
        """
        self.cookie_path = cookie_path

    @property
    def is_available(self) -> bool:
        """检查 Cookie 是否可用"""
        if not self.cookie_path:
            return False

        valid, _ = validate_cookie_file(self.cookie_path)
        return valid

    @property
    def path_for_ytdlp(self) -> str | None:
        """获取用于 yt-dlp 的路径字符串"""
        return get_cookie_file_for_ytdlp(self.cookie_path)

    def validate(self) -> tuple[bool, str]:
        """验证当前 Cookie 文件"""
        if not self.cookie_path:
            return False, "未配置 Cookie 文件"

        return validate_cookie_file(self.cookie_path)

"""
Download Core - 核心下载逻辑封装
Core download logic wrapper for yt-dlp
"""
import asyncio
import logging
import shutil
from pathlib import Path
from typing import Callable, Optional

from .formats import get_format_config, requires_ffmpeg


# 设置日志
logger = logging.getLogger(__name__)


class DownloadCore:
    """
    下载核心类 - 封装 yt-dlp 下载逻辑
    Core download class that wraps yt-dlp download logic
    """

    def __init__(
        self,
        download_dir: Path,
        ffmpeg_location: Optional[str] = None,
        cookie_file: Optional[Path] = None,
        progress_callback: Optional[Callable[[dict], None]] = None,
    ):
        """
        初始化下载核心

        Args:
            download_dir: 下载目录
            ffmpeg_location: FFmpeg 可执行文件路径
            cookie_file: Cookie 文件路径（用于年龄限制视频）
            progress_callback: 进度回调函数
        """
        self.download_dir = download_dir
        self.ffmpeg_location = ffmpeg_location
        self.cookie_file = cookie_file
        self.progress_callback = progress_callback

    def _clear_cache(self) -> None:
        """
        清除 yt-dlp 缓存目录

        用于解决 403 Forbidden 等缓存相关问题

        参考: https://github.com/yt-dlp/yt-dlp/wiki/Cache
        """
        import yt_dlp

        try:
            # 使用 YoutubeDL 的 Cache API 来清除缓存
            with yt_dlp.YoutubeDL({'quiet': True}) as ydl:
                ydl.cache.remove()
                cache_dir = ydl.cache._get_root_dir()
                logger.info(f"✅ 已清除 yt-dlp 缓存: {cache_dir}")
        except Exception as e:
            logger.warning(f"⚠️ 清除缓存失败: {e}")

    def _is_403_error(self, error: Exception) -> bool:
        """
        检测是否为 403 Forbidden 错误

        Args:
            error: 异常对象

        Returns:
            是否为 403 错误
        """
        error_str = str(error).lower()
        return (
            "403" in error_str or
            "forbidden" in error_str or
            "sign in" in error_str or
            "login" in error_str
        )

    def build_ydl_opts(self, format_id: str) -> dict:
        """
        构建 yt-dlp 选项配置

        Args:
            format_id: 格式标识符

        Returns:
            yt-dlp 选项字典
        """
        ext, ydl_format, is_audio = get_format_config(format_id)

        # 构建 FFmpeg 后处理器列表
        postprocessors = [
            # 隐私保护：移除元数据
            {"key": "FFmpegMetadata", "add_metadata": False},
        ]

        # 根据格式添加转码处理器
        if is_audio:
            # 音频提取和转码
            # 无损格式使用最高质量，有损格式使用 192kbps
            quality = "0" if format_id in ["flac", "wav"] else "192"
            postprocessors.append({
                "key": "FFmpegExtractAudio",
                "preferredcodec": ext,
                "preferredquality": quality,
            })
        elif ext != "mp4":
            # 非 MP4 格式需要转码
            postprocessors.append({
                "key": "FFmpegVideoConvertor",
                "preferedformat": ext,
            })

        # 基础配置
        ydl_opts = {
            "format": ydl_format,
            "progress_hooks": [self._progress_hook] if self.progress_callback else [],
            "outtmpl": str(self.download_dir / "%(title).75s.%(ext)s"),  # 限制文件名长度
            "merge_output_format": ext if not is_audio else None,
            "quiet": True,
            "no_warnings": True,
            "noplaylist": True,
            "ignoreerrors": False,
            # 隐私保护配置
            "no_call_home": True,          # 禁用更新检查
            "no_check_certificate": False, # 保持安全检查
            "prefer_insecure": False,      # 永不优先使用不安全连接
            "clean_infojson": True,        # 删除元数据文件
            "restrictfilenames": True,     # 清理文件名
            "trim_file_name": 150,         # 防止文件名过长
            "geo_bypass": True,            # 在法律允许的情况下绕过地理位置限制
            # 反爬虫检测：模拟真实浏览器
            "user_agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
            "referer": "https://www.google.com/",
            "no_check_certificates": False,
            "postprocessors": postprocessors,
        }

        # 添加 FFmpeg 路径（如果指定）
        if self.ffmpeg_location:
            ydl_opts["ffmpeg_location"] = self.ffmpeg_location

        # 添加 Cookie 支持（如果指定）
        if self.cookie_file and self.cookie_file.exists():
            ydl_opts["cookiefile"] = str(self.cookie_file)

        return ydl_opts

    def _progress_hook(self, d: dict) -> None:
        """
        yt-dlp 进度钩子

        Args:
            d: 进度信息字典
        """
        if self.progress_callback:
            self.progress_callback(d)

    async def download(
        self,
        url: str,
        format_id: str,
        info_callback: Optional[Callable[[str], None]] = None,
    ) -> tuple[bool, str, Optional[str]]:
        """
        执行下载（带智能重试）

        Args:
            url: 视频 URL
            format_id: 格式标识符
            info_callback: 信息回调函数（用于更新状态）

        Returns:
            (成功状态, 标题, 错误信息)
        """
        import yt_dlp
        import re

        max_retries = 2  # 最多重试 2 次
        last_error = None

        for attempt in range(max_retries):
            try:
                ydl_opts = self.build_ydl_opts(format_id)

                with yt_dlp.YoutubeDL(ydl_opts) as ydl:
                    # 提取视频信息
                    if info_callback:
                        if attempt == 0:
                            info_callback("🔍 Extracting video information securely...")
                        else:
                            info_callback("🔄 Retrying with fresh cache...")

                    info = ydl.extract_info(url, download=False)
                    title = info.get("title", "Unknown Title")

                    # 清理标题用于显示
                    display_title = re.sub(r'[^\w\s.-]', '', title)[:70]
                    if len(title) > 70:
                        display_title += "..."

                    # 开始下载
                    format_name = get_format_config(format_id)[0].upper()

                    if info_callback:
                        is_audio = format_id in ["mp3", "wav", "flac", "m4a", "opus"]
                        if is_audio:
                            info_callback(f"⬇️ 提取音频为 {format_name} 格式...")
                        else:
                            info_callback(f"⬇️ 下载中为 {format_name} 格式...")

                    ydl.download([url])

                    # 下载成功
                    if attempt > 0:
                        logger.info(f"✅ 重试成功 (第 {attempt + 1} 次尝试)")
                    return True, display_title, None

            except yt_dlp.utils.DownloadError as e:
                last_error = e
                error_msg = str(e)

                # 检测是否为 403 错误
                if self._is_403_error(e):
                    if attempt == 0:
                        # 第一次遇到 403，清除缓存并重试
                        logger.warning(f"⚠️ 检测到 403 错误，清除缓存后重试...")
                        if info_callback:
                            info_callback("⚠️ 403 错误，自动清除缓存重试中...")
                        self._clear_cache()
                        continue  # 继续下一次尝试
                    else:
                        # 第二次仍然是 403，放弃
                        logger.error(f"❌ 重试后仍然 403，下载失败")
                        break
                else:
                    # 其他错误，不重试
                    logger.error(f"❌ 下载错误: {error_msg[:100]}")
                    break

            except Exception as e:
                last_error = e
                error_msg = f"{type(e).__name__}: {str(e)}"
                logger.error(f"❌ 未知错误: {error_msg[:100]}")
                break

        # 所有尝试都失败
        error_msg = str(last_error).split("\n")[0][:100] if last_error else "Unknown error"
        return False, "", error_msg

    def extract_video_info(self, url: str) -> Optional[dict]:
        """
        提取视频信息（不下载）

        Args:
            url: 视频 URL

        Returns:
            视频信息字典，失败时返回 None
        """
        import yt_dlp

        ydl_opts = {
            "quiet": True,
            "no_warnings": True,
            "extract_flat": True,
        }

        try:
            with yt_dlp.YoutubeDL(ydl_opts) as ydl:
                return ydl.extract_info(url, download=False)
        except Exception:
            return None

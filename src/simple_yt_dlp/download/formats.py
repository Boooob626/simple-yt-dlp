"""
Format Configurations - 格式配置和映射
Format mapping and configuration for download options
"""
from typing import Final

# 格式映射：格式ID -> (扩展名, yt-dlp格式字符串)
# Format mapping: format_id -> (extension, yt-dlp format string)
FORMAT_MAPPING: Final[dict[str, tuple[str, str]]] = {
    "mp4_best": ("mp4", "bestvideo+bestaudio/best"),
    "mp4_1080p": ("mp4", "bestvideo[height<=1080]+bestaudio/best[height<=1080]"),
    "mp4_720p": ("mp4", "bestvideo[height<=720]+bestaudio/best[height<=720]"),
    "mp4_480p": ("mp4", "bestvideo[height<=480]+bestaudio/best[height<=480]"),
    "mp4_360p": ("mp4", "bestvideo[height<=360]+bestaudio/best[height<=360]"),
    "mkv_best": ("mkv", "bestvideo+bestaudio/best"),
    "webm_best": ("webm", "bestvideo+bestaudio/best"),
    "mov_best": ("mov", "bestvideo+bestaudio/best"),
    "flac": ("flac", "bestaudio/best"),
    "wav": ("wav", "bestaudio/best"),
    "m4a": ("m4a", "bestaudio/best"),
    "opus": ("opus", "bestaudio/best"),
    "mp3": ("mp3", "bestaudio/best"),
}

# 音频格式集合
# Audio format identifiers
AUDIO_FORMATS: Final[set[str]] = {"mp3", "wav", "flac", "m4a", "opus"}

# 格式显示名称映射
# Format display names for UI
FORMAT_NAMES: Final[dict[str, str]] = {
    "mp4_best": "MP4 (4K)",
    "mp4_1080p": "MP4 (1080p)",
    "mp4_720p": "MP4 (720p)",
    "mp4_480p": "MP4 (480p)",
    "mp4_360p": "MP4 (360p)",
    "mkv_best": "MKV",
    "webm_best": "WebM",
    "mov_best": "MOV",
    "flac": "FLAC",
    "wav": "WAV",
    "m4a": "M4A",
    "opus": "OPUS",
    "mp3": "MP3",
}

# 需要 FFmpeg 的格式集合（用于优雅降级）
# Formats that require FFmpeg (for graceful degradation)
FFMPEG_REQUIRED_FORMATS: Final[set[str]] = {
    "mp3", "flac", "wav", "opus", "m4a",  # 音频提取
    "mp4_best", "mkv_best", "webm_best", "mov_best"  # 高质量视频合并
}

# Select 组件的选项列表
# Options for the Select widget
SELECT_OPTIONS: Final[list[tuple[str, str]]] = [
    ("MP4 (4K/Best)", "mp4_best"),
    ("MP4 (1080p)", "mp4_1080p"),
    ("MP4 (720p)", "mp4_720p"),
    ("MP4 (480p)", "mp4_480p"),
    ("MP4 (360p)", "mp4_360p"),
    ("MKV (Best Quality)", "mkv_best"),
    ("WebM (High Compression)", "webm_best"),
    ("MOV (Apple Compatible)", "mov_best"),
    ("Audio Only - FLAC (Lossless)", "flac"),
    ("Audio Only - WAV (Lossless)", "wav"),
    ("Audio Only - M4A/AAC", "m4a"),
    ("Audio Only - OPUS", "opus"),
    ("Audio Only - MP3", "mp3"),
]


def get_format_config(format_id: str) -> tuple[str, str, bool]:
    """
    获取格式配置

    Args:
        format_id: 格式标识符

    Returns:
        (扩展名, yt-dlp格式字符串, 是否为音频格式)
    """
    ext, ydl_format = FORMAT_MAPPING.get(format_id, ("mp4", "bestvideo+bestaudio/best"))
    is_audio = format_id in AUDIO_FORMATS
    return ext, ydl_format, is_audio


def get_format_name(format_id: str) -> str:
    """
    获取格式显示名称

    Args:
        format_id: 格式标识符

    Returns:
        格式显示名称
    """
    return FORMAT_NAMES.get(format_id, format_id.upper())


def requires_ffmpeg(format_id: str) -> bool:
    """
    检查格式是否需要 FFmpeg

    Args:
        format_id: 格式标识符

    Returns:
        是否需要 FFmpeg
    """
    return format_id in FFMPEG_REQUIRED_FORMATS


def get_available_formats(ffmpeg_available: bool = True) -> list[tuple[str, str]]:
    """
    根据 FFmpeg 可用性返回可用格式列表

    Args:
        ffmpeg_available: FFmpeg 是否可用

    Returns:
        可用格式选项列表
    """
    if ffmpeg_available:
        return SELECT_OPTIONS

    # 过滤掉需要 FFmpeg 的格式
    return [
        (label, value)
        for label, value in SELECT_OPTIONS
        if value not in FFMPEG_REQUIRED_FORMATS
    ]

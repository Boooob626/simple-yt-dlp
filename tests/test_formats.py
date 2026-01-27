"""
Test format configurations
"""
from simple_yt_dlp.download.formats import (
    FFMPEG_REQUIRED_FORMATS,
    AUDIO_FORMATS,
    get_format_config,
    get_format_name,
    get_available_formats,
    requires_ffmpeg,
)


def test_get_format_config():
    """Test format configuration retrieval"""
    # Video format
    ext, ydl_format, is_audio = get_format_config("mp4_best")
    assert ext == "mp4"
    assert "bestvideo" in ydl_format
    assert is_audio is False

    # Audio format
    ext, ydl_format, is_audio = get_format_config("mp3")
    assert ext == "mp3"
    assert "bestaudio" in ydl_format
    assert is_audio is True


def test_get_format_name():
    """Test format display names"""
    assert get_format_name("mp4_best") == "MP4 (4K)"
    assert get_format_name("flac") == "FLAC"
    assert get_format_name("unknown") == "UNKNOWN"


def test_requires_ffmpeg():
    """Test FFmpeg requirement detection"""
    assert requires_ffmpeg("mp3") is True  # Audio extraction
    assert requires_ffmpeg("mp4_best") is True  # Video merging
    assert requires_ffmpeg("mp4_360p") is False  # No FFmpeg needed


def test_get_available_formats():
    """Test available formats with FFmpeg check"""
    # With FFmpeg available
    all_formats = get_available_formats(ffmpeg_available=True)
    assert len(all_formats) == 13  # All formats

    # With FFmpeg unavailable
    limited_formats = get_available_formats(ffmpeg_available=False)
    assert len(limited_formats) < len(all_formats)  # Some formats disabled


def test_audio_formats_set():
    """Test audio format identification"""
    assert "mp3" in AUDIO_FORMATS
    assert "flac" in AUDIO_FORMATS
    assert "mp4_best" not in AUDIO_FORMATS


def test_ffmpeg_required_formats():
    """Test FFmpeg required formats set"""
    assert "mp3" in FFMPEG_REQUIRED_FORMATS
    assert "flac" in FFMPEG_REQUIRED_FORMATS
    assert "mp4_best" in FFMPEG_REQUIRED_FORMATS

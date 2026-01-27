"""
Test validation utilities
"""
import pytest
from simple_yt_dlp.utils.validation import (
    validate_youtube_url,
    sanitize_filename,
    is_valid_directory_path,
)


class TestValidateYoutubeUrl:
    """Test YouTube URL validation"""

    def test_valid_youtube_urls(self):
        """Test valid YouTube URLs"""
        valid_urls = [
            "https://www.youtube.com/watch?v=dQw4w9WgXcQ",
            "https://youtu.be/dQw4w9WgXcQ",
            "http://www.youtube.com/watch?v=dQw4w9WgXcQ",
            "www.youtube.com/watch?v=dQw4w9WgXcQ",
            "youtube.com/watch?v=dQw4w9WgXcQ",
        ]
        for url in valid_urls:
            valid, msg = validate_youtube_url(url)
            assert valid is True, f"URL should be valid: {url}"
            assert msg == ""

    def test_invalid_urls(self):
        """Test invalid URLs"""
        invalid_urls = [
            "",
            "https://google.com",
            "not a url",
            "https://vimeo.com/12345",
        ]
        for url in invalid_urls:
            valid, msg = validate_youtube_url(url)
            assert valid is False, f"URL should be invalid: {url}"
            assert msg != ""


class TestSanitizeFilename:
    """Test filename sanitization"""

    def test_remove_invalid_chars(self):
        """Test removal of invalid characters"""
        assert sanitize_filename("video<>:name?.mp4") == "videoname.mp4"
        assert sanitize_filename("file/with\\slashes") == "filewithslashes"

    def test_max_length(self):
        """Test filename length limit"""
        long_name = "a" * 100
        result = sanitize_filename(long_name, max_length=50)
        assert len(result) <= 53  # 50 + "..."

    def test_preserve_valid_chars(self):
        """Test preservation of valid characters"""
        assert sanitize_filename("My Video - 2024.mp4") == "My Video - 2024.mp4"
        assert sanitize_filename("file_name.tar.gz") == "file_name.tar.gz"


class TestIsValidDirectoryPath:
    """Test directory path validation"""

    def test_valid_paths(self):
        """Test valid directory paths"""
        assert is_valid_directory_path("/tmp") is True
        assert is_valid_directory_path("~/Downloads") is True
        assert is_valid_directory_path(".") is True

    def test_invalid_paths(self):
        """Test invalid paths"""
        # Paths with null bytes are invalid
        assert is_valid_directory_path("path\x00with\x00nulls") is False

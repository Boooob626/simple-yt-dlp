"""
主入口点 - Main entry point for pip install command
"""
from .app import PrivacyYouTubeDownloader


def main() -> None:
    """主入口点 - 被 pip install 后的命令调用"""
    app = PrivacyYouTubeDownloader()
    app.run()


if __name__ == "__main__":
    main()

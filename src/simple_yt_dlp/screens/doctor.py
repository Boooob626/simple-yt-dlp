"""
Doctor Screen - 系统诊断屏幕
System diagnostic screen showing tool status and configuration
"""
import os
import platform
import shutil
import subprocess
from pathlib import Path
from textual.app import ComposeResult
from textual.containers import Horizontal, Vertical
from textual.screen import Screen
from textual.widgets import Button, Label


class DoctorScreen(Screen):
    """
    Doctor 诊断屏幕 - 显示系统状态和诊断信息

    显示内容:
    - FFmpeg 状态（路径、版本）
    - yt-dlp 版本（是否最新）
    - 配置文件路径
    - 下载目录状态
    - 系统信息（Python 版本、OS）
    """

    CSS = """
    DoctorScreen {
        align: center middle;
    }

    .doctor-container {
        width: 80%;
        height: 90%;
        background: $panel;
        border: round $primary;
        padding: 2;
    }

    #doctor-title {
        text-align: center;
        text-style: bold;
        color: $primary;
        margin-bottom: 2;
        text-style: bold;
    }

    .section {
        margin: 1 0;
        padding: 1;
        background: $surface;
        border: round $primary-background;
    }

    .section-title {
        text-style: bold;
        color: $accent;
        margin-bottom: 1;
    }

    .info-row {
        height: 1;
        margin: 0 1;
    }

    .status-ok {
        color: $success;
    }

    .status-warning {
        color: $warning;
    }

    .status-error {
        color: $error;
    }

    .label {
        color: $text-muted;
        width: 30%;
    }

    .value {
        color: $text;
    }

    #close_btn {
        margin-top: 2;
        width: 20%;
    }
    """

    def __init__(
        self,
        ffmpeg_path: str | None = None,
        config_path: Path | None = None,
        download_dir: Path | None = None,
    ):
        super().__init__()
        self.ffmpeg_path = ffmpeg_path
        self.config_path = config_path
        self.download_dir = download_dir

        # 收集诊断信息
        self.diagnostic_info = self._collect_diagnostic_info()

    def _collect_diagnostic_info(self) -> dict:
        """收集系统诊断信息"""
        info = {
            "system": self._get_system_info(),
            "ffmpeg": self._get_ffmpeg_info(),
            "ytdlp": self._get_ytdlp_info(),
            "paths": self._get_path_info(),
        }
        return info

    def _get_system_info(self) -> dict:
        """获取系统信息"""
        return {
            "os": f"{platform.system()} {platform.release()}",
            "python": platform.python_version(),
            "arch": platform.machine(),
        }

    def _get_ffmpeg_info(self) -> dict:
        """获取 FFmpeg 信息"""
        ffmpeg_path = shutil.which("ffmpeg")
        if not ffmpeg_path:
            return {
                "status": "error",
                "message": "未安装 FFmpeg",
                "path": None,
                "version": None,
            }

        try:
            result = subprocess.run(
                [ffmpeg_path, "-version"],
                capture_output=True,
                text=True,
                timeout=5,
            )
            version_line = result.stdout.split("\n")[0]
            version = version_line.split("Copyright")[0].strip()
            return {
                "status": "ok",
                "message": "FFmpeg 已安装",
                "path": ffmpeg_path,
                "version": version,
            }
        except Exception as e:
            return {
                "status": "warning",
                "message": f"FFmpeg 检测失败: {e}",
                "path": ffmpeg_path,
                "version": None,
            }

    def _get_ytdlp_info(self) -> dict:
        """获取 yt-dlp 信息"""
        try:
            import yt_dlp
            version = yt_dlp.version.__version__
            return {
                "status": "ok",
                "message": "yt-dlp 已安装",
                "version": version,
            }
        except ImportError:
            return {
                "status": "error",
                "message": "yt-dlp 未安装",
                "version": None,
            }
        except Exception as e:
            return {
                "status": "warning",
                "message": f"yt-dlp 检测失败: {e}",
                "version": None,
            }

    def _get_path_info(self) -> dict:
        """获取路径信息"""
        paths = {}

        if self.config_path:
            exists = self.config_path.exists()
            paths["config"] = {
                "path": str(self.config_path),
                "status": "ok" if exists else "warning",
                "message": "存在" if exists else "不存在",
            }

        if self.download_dir:
            exists = self.download_dir.exists()
            writable = self.download_dir.exists() and os.access(self.download_dir, os.W_OK)
            paths["download_dir"] = {
                "path": str(self.download_dir),
                "status": "ok" if exists and writable else "error",
                "message": "可写" if writable else "不可写" if exists else "不存在",
            }

        return paths

    def compose(self) -> ComposeResult:
        """Compose the doctor screen"""
        yield Vertical(
            Label("🔍 系统诊断 / System Diagnostics", id="doctor-title"),
            self._create_system_section(),
            self._create_ffmpeg_section(),
            self._create_ytdlp_section(),
            self._create_paths_section(),
            Button("关闭 / Close", variant="primary", id="close_btn"),
            classes="doctor-container",
        )

    def _create_system_section(self) -> Vertical:
        """创建系统信息部分"""
        sys_info = self.diagnostic_info["system"]
        rows = [
            Label(f"操作系统 / OS: {sys_info['os']}", classes="info-row"),
            Label(f"Python 版本: {sys_info['python']}", classes="info-row"),
            Label(f"架构 / Arch: {sys_info['arch']}", classes="info-row"),
        ]

        return Vertical(
            Label("📊 系统信息 / System", classes="section-title"),
            *rows,
            classes="section",
        )

    def _create_ffmpeg_section(self) -> Vertical:
        """创建 FFmpeg 信息部分"""
        ffmpeg = self.diagnostic_info["ffmpeg"]
        status_class = f"status-{ffmpeg['status']}"

        rows = [
            Horizontal(
                Label("状态 / Status: ", classes="info-row label"),
                Label(ffmpeg["message"], classes=f"info-row value {status_class}"),
            ),
        ]

        if ffmpeg["path"]:
            rows.append(
                Label(f"路径 / Path: {ffmpeg['path']}", classes="info-row")
            )

        if ffmpeg["version"]:
            rows.append(
                Label(f"版本 / Version: {ffmpeg['version']}", classes="info-row")
            )

        return Vertical(
            Label("🎬 FFmpeg", classes="section-title"),
            *rows,
            classes="section",
        )

    def _create_ytdlp_section(self) -> Vertical:
        """创建 yt-dlp 信息部分"""
        ytdlp = self.diagnostic_info["ytdlp"]
        status_class = f"status-{ytdlp['status']}"

        rows = [
            Horizontal(
                Label("状态 / Status: ", classes="info-row label"),
                Label(ytdlp["message"], classes=f"info-row value {status_class}"),
            ),
        ]

        if ytdlp["version"]:
            rows.append(
                Label(f"版本 / Version: {ytdlp['version']}", classes="info-row")
            )

        return Vertical(
            Label("📺 yt-dlp", classes="section-title"),
            *rows,
            classes="section",
        )

    def _create_paths_section(self) -> Vertical:
        """创建路径信息部分"""
        paths = self.diagnostic_info["paths"]
        rows = []

        for key, info in paths.items():
            label_map = {
                "config": "配置文件",
                "download_dir": "下载目录",
            }
            label = label_map.get(key, key)
            status_class = f"status-{info['status']}"

            rows.append(
                Horizontal(
                    Label(f"{label}: ", classes="info-row label"),
                    Label(info["path"], classes="info-row value"),
                )
            )
            rows.append(
                Horizontal(
                    Label("状态 / Status: ", classes="info-row label"),
                    Label(info["message"], classes=f"info-row value {status_class}"),
                )
            )

        return Vertical(
            Label("📁 路径 / Paths", classes="section-title"),
            *rows,
            classes="section",
        )

    def on_button_pressed(self, event: Button.Pressed) -> None:
        """处理按钮点击"""
        if event.button.id == "close_btn":
            self.dismiss()

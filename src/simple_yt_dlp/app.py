"""
Main Application - 主应用类
Privacy-Focused YouTube Downloader Application
"""
import shutil
from datetime import datetime
from pathlib import Path
from typing import Optional

from textual.app import App, ComposeResult
from textual.binding import Binding
from textual.containers import Horizontal, ScrollableContainer, Vertical
from textual.widgets import Button, Footer, Input, Label, ProgressBar, Select, Static

from .config import Config
from .download import DownloadCore
from .download.formats import (
    FFMPEG_REQUIRED_FORMATS,
    FORMAT_NAMES,
    SELECT_OPTIONS,
    get_available_formats,
    get_format_config,
)
from .screens.directory import DirectorySelector
from .screens.doctor import DoctorScreen
from .styles import CSS
from .utils import CookieManager, setup_logging, validate_youtube_url


class PrivacyYouTubeDownloader(App):
    """
    隐私优先的 YouTube 视频下载器
    Privacy-focused YouTube video downloader with professional UI
    """

    # 加载 CSS 样式
    CSS = CSS

    # 键盘绑定
    BINDINGS = [
        Binding("ctrl+c", "quit", "Quit", show=True),
        Binding("ctrl+d", "clear", "Clear Form", show=True),
        Binding("ctrl+s", "select_directory", "Select Directory", show=True),
        Binding("f1", "show_doctor", "Doctor", show=True),
    ]

    def __init__(self):
        super().__init__()
        # 初始化日志
        self.logger = setup_logging()

        # 应用状态
        self.is_downloading = False
        self.download_history = []
        self.download_dir = Path.home() / "Downloads" / "PrivateDownloads"
        self.last_format = "mp4_best"

        # FFmpeg 检测 - 必须在配置加载之前完成
        self.ffmpeg_available = shutil.which("ffmpeg") is not None
        self.ffmpeg_location = shutil.which("ffmpeg") or "/usr/bin/ffmpeg"

        # 配置管理
        self.config = Config()
        self._load_config()
        self.download_dir.mkdir(parents=True, exist_ok=True)

        # Cookie 管理
        cookie_path = self.config.cookie_file
        self.cookie_manager = CookieManager(cookie_path)

        # 下载核心
        self.download_core = DownloadCore(
            download_dir=self.download_dir,
            ffmpeg_location=self.ffmpeg_location if self.ffmpeg_available else None,
            cookie_file=self.cookie_manager.cookie_path,
            progress_callback=self._progress_hook,
        )

        self.logger.info(f"应用初始化完成 (FFmpeg: {self.ffmpeg_available})")

    def _load_config(self) -> None:
        """从配置加载设置"""
        if self.config.download_dir:
            self.download_dir = self.config.download_dir

        # 验证并迁移格式配置（旧配置可能包含 yt-dlp 格式字符串）
        valid_format_ids = {
            "mp4_best", "mp4_1080p", "mp4_720p", "mp4_480p", "mp4_360p",
            "mkv_best", "webm_best", "mov_best",
            "flac", "wav", "m4a", "opus", "mp3",
        }

        if self.config.last_format:
            saved_format = self.config.last_format
            # 检查是否是有效的格式 ID
            if saved_format in valid_format_ids:
                self.last_format = saved_format
            else:
                # 旧配置包含 yt-dlp 格式字符串，迁移到默认格式
                self.logger.info(f"迁移旧格式配置: {saved_format} -> mp4_720p")
                self.last_format = "mp4_720p"
                # 保存新格式到配置
                self.config.last_format = "mp4_720p"

        # FFmpeg 优雅降级 - 如果保存的格式需要 FFmpeg 但 FFmpeg 不可用，选择不需要 FFmpeg 的格式
        from .download.formats import requires_ffmpeg

        if not self.ffmpeg_available and requires_ffmpeg(self.last_format):
            # 选择一个不需要 FFmpeg 的格式
            self.logger.info(f"FFmpeg 不可用，切换格式: {self.last_format} -> mp4_720p")
            self.last_format = "mp4_720p"
            # 保存新格式到配置
            self.config.last_format = "mp4_720p"

    def compose(self) -> ComposeResult:
        """Compose the main UI"""
        yield Label("🔒 Privacy-Focused Video Downloader", id="header")

        yield Vertical(
            Vertical(
                Label("Video URL:", classes="option-label"),
                Input(placeholder="https://www.youtube.com/watch?v=...", id="url_input"),
                id="url_container"
            ),
            Vertical(
                Horizontal(
                    Label("Format:", classes="option-label"),
                    Select(
                        get_available_formats(self.ffmpeg_available),
                        value=self.last_format,
                        id="format_select"
                    ),
                    classes="option-row"
                ),
                Horizontal(
                    Label("Save to:", classes="option-label"),
                    Select(
                        [
                            (str(self.download_dir), str(self.download_dir)),
                            ("Custom Directory...", "custom"),
                        ],
                        value=str(self.download_dir),
                        id="dir_select"
                    ),
                    classes="option-row"
                ),
                id="options_container"
            ),
            Vertical(
                Label("🛡️ Privacy Protection Enabled", id="privacy_label"),
                Label("• Downloads stored in isolated directory", classes="history-item"),
                Label("• Metadata stripped from files", classes="history-item"),
                Label("• No telemetry or external tracking", classes="history-item"),
                Label("• Auto transcoding to selected format", classes="history-item"),
                id="privacy_section"
            ),
            Static(id="title"),
            Static(id="status"),
            ProgressBar(id="progress_bar", show_percentage=True, total=100),
            Horizontal(
                Button("Download", variant="success", id="download_btn"),
                Button("Clear", variant="warning", id="clear_btn"),
                Button("Cancel", variant="error", id="cancel_btn"),
                id="controls"
            ),
            Vertical(
                Label("Download History", id="history_title"),
                ScrollableContainer(id="history_list"),
                id="history_container"
            ),
            Footer()
        )

    def on_mount(self) -> None:
        """应用挂载时的初始化"""
        self.query_one("#progress_bar").display = False
        self.query_one("#url_input").focus()
        self.update_history_display()

        # FFmpeg 优雅降级 - 显示警告
        if not self.ffmpeg_available:
            self.notify(
                "⚠️ FFmpeg 未检测到，已禁用需要合并/转码的格式",
                severity="warning"
            )
            self.logger.warning("FFmpeg 未检测到，部分格式不可用")

    def on_input_submitted(self, event: Input.Submitted) -> None:
        """处理输入提交"""
        if not self.is_downloading:
            self.action_start_download()

    def on_button_pressed(self, event: Button.Pressed) -> None:
        """处理按钮点击"""
        if event.button.id == "download_btn" and not self.is_downloading:
            self.action_start_download()
        elif event.button.id == "clear_btn" and not self.is_downloading:
            self.action_clear()
        elif event.button.id == "cancel_btn" and self.is_downloading:
            self.action_cancel_download()

    def on_select_changed(self, event: Select.Changed) -> None:
        """处理选择变化"""
        if event.select.id == "dir_select" and event.value == "custom":
            self.action_select_directory()
        elif event.select.id == "format_select":
            # 保存格式选择到配置
            self.config.last_format = event.value
            self.last_format = event.value

    def action_select_directory(self) -> None:
        """打开目录选择对话框"""
        def check_mount():
            if not self.is_mounted:
                return
            self.push_screen(DirectorySelector(self.download_dir), callback=self.directory_selected)

        self.set_timer(0.1, check_mount)

    def action_show_doctor(self) -> None:
        """显示 Doctor 诊断屏幕"""
        self.push_screen(DoctorScreen(
            ffmpeg_path=self.ffmpeg_location,
            config_path=self.config.config_path,
            download_dir=self.download_dir,
        ))

    def directory_selected(self, path: Optional[Path]) -> None:
        """目录选择回调"""
        if path:
            path.mkdir(parents=True, exist_ok=True)
            self.download_dir = path
            self.config.download_dir = path

            # 更新 Select 组件选项
            dir_select = self.query_one("#dir_select", Select)
            dir_select.set_options([
                (str(self.download_dir), str(self.download_dir)),
                ("Custom Directory...", "custom"),
            ])
            dir_select.value = str(self.download_dir)

            # 更新下载核心的目录
            self.download_core.download_dir = self.download_dir

            self.notify(f"Directory set to: {path}", severity="information")

    def action_start_download(self) -> None:
        """开始下载"""
        url = self.query_one("#url_input", Input).value.strip()

        # URL 验证
        valid, error_msg = validate_youtube_url(url)
        if not valid:
            self.query_one("#status", Static).update(f"❌ {error_msg}")
            return

        if self.is_downloading:
            self.query_one("#status", Static).update("⚠️ Already downloading a video")
            return

        # 重置 UI
        self.query_one("#title", Static).update("")
        self.query_one("#status", Static).update("⏳ Initializing secure download...")
        progress_bar = self.query_one("#progress_bar", ProgressBar)
        progress_bar.display = True
        progress_bar.update(progress=0)

        # 禁用控件
        self.query_one("#url_input", Input).disabled = True
        self.query_one("#download_btn", Button).disabled = True
        self.query_one("#clear_btn", Button).disabled = True
        self.query_one("#cancel_btn", Button).display = True
        self.is_downloading = True

        # 异步执行下载
        self.run_worker(self._download_video(url), thread=True, exclusive=True)

    def action_clear(self) -> None:
        """清除所有 UI 元素"""
        if self.is_downloading:
            self.query_one("#status", Static).update("⚠️ Cannot clear while downloading")
            return

        self.query_one("#url_input", Input).value = ""
        self.query_one("#title", Static).update("")
        self.query_one("#status", Static).update("")
        pb = self.query_one("#progress_bar", ProgressBar)
        pb.update(progress=0)
        pb.display = False
        self.query_one("#url_input", Input).disabled = False
        self.query_one("#download_btn", Button).disabled = False
        self.query_one("#clear_btn", Button).disabled = False
        self.query_one("#cancel_btn", Button).display = False
        self.query_one("#url_input", Input).focus()

    def action_cancel_download(self) -> None:
        """取消正在进行的下载"""
        if self.is_downloading:
            self.query_one("#status", Static).update("🛑 Canceling download...")
            self.is_downloading = False

    async def _download_video(self, url: str) -> None:
        """执行下载"""
        format_id = self.query_one("#format_select", Select).value

        def info_callback(msg: str) -> None:
            """信息回调"""
            self.call_from_thread(
                self.query_one("#status", Static).update,
                msg
            )

        success, title, error = await self.download_core.download(
            url=url,
            format_id=format_id,
            info_callback=info_callback,
        )

        if self.is_downloading:  # 检查是否被取消
            if success:
                # 添加到历史记录
                self.download_history.append({
                    "title": title,
                    "timestamp": datetime.now(),
                    "status": "success",
                    "path": self.download_dir
                })
                self.call_from_thread(self.update_history_display)

                ext, _, _ = get_format_config(format_id)
                format_name = FORMAT_NAMES.get(format_id, ext.upper())
                complete_msg = f"✅ {format_name} 转码完成！已保存到: {self.download_dir}"
                self.call_from_thread(
                    self.query_one("#status", Static).update,
                    complete_msg
                )
            else:
                # 下载失败
                self.download_history.append({
                    "title": title or "Unknown",
                    "timestamp": datetime.now(),
                    "status": "error",
                    "error": error
                })
                self.call_from_thread(self.update_history_display)
                self.call_from_thread(
                    self.query_one("#status", Static).update,
                    f"❌ Download failed: {error}"
                )

        self.call_from_thread(self._download_complete)

    def _download_complete(self) -> None:
        """下载完成后重置 UI"""
        self.is_downloading = False
        self.query_one("#url_input", Input).disabled = False
        self.query_one("#download_btn", Button).disabled = False
        self.query_one("#clear_btn", Button).disabled = False
        self.query_one("#cancel_btn", Button).display = False
        self.query_one("#url_input", Input).value = ""
        self.query_one("#url_input", Input).focus()

    def _progress_hook(self, d: dict) -> None:
        """yt-dlp 进度钩子"""
        if not self.is_downloading:
            return

        if d["status"] == "downloading":
            total_bytes = (
                d.get("total_bytes") or
                d.get("total_bytes_estimate") or
                d.get("filesize") or
                1
            )
            downloaded_bytes = d.get("downloaded_bytes", 0)
            percentage = (downloaded_bytes / total_bytes) * 100 if total_bytes > 0 else 0

            # 更新进度条
            self.call_from_thread(
                self.query_one("#progress_bar", ProgressBar).update,
                progress=min(percentage, 100)
            )

            # 格式化速度显示
            speed = d.get("speed", 0) or 0
            if speed >= 1024 * 1024:
                speed_str = f"{speed / 1024 / 1024:.2f} MB/s"
            elif speed >= 1024:
                speed_str = f"{speed / 1024:.1f} KB/s"
            else:
                speed_str = f"{speed:.0f} B/s" if speed > 0 else "0 B/s"

            # 格式化 ETA
            eta = d.get("eta")
            eta_str = f"{int(eta)}s" if eta is not None and eta > 0 else "-"

            # 更新状态
            status_text = f"⬇️ {speed_str} | ETA: {eta_str} | {percentage:.1f}%"
            self.call_from_thread(
                self.query_one("#status", Static).update,
                status_text
            )

        elif d["status"] == "finished":
            self.call_from_thread(
                self.query_one("#progress_bar", ProgressBar).update,
                progress=100
            )
            self.call_from_thread(
                self.query_one("#status", Static).update,
                "✅ 下载完成，正在转码和移除元数据..."
            )

    def update_history_display(self) -> None:
        """更新下载历史显示"""
        history_list = self.query_one("#history_list", ScrollableContainer)
        history_list.query("*").remove()

        if not self.download_history:
            history_list.mount(Static("No downloads yet", classes="history-item text-muted"))
            return

        # 显示最近 5 次下载
        for item in reversed(self.download_history[-5:]):
            timestamp = item["timestamp"].strftime("%H:%M:%S")
            status_icon = "✅" if item["status"] == "success" else "❌"
            status_class = "history-success" if item["status"] == "success" else "history-error"

            if item["status"] == "success":
                history_text = f"{status_icon} {timestamp} | {item['title']}"
            else:
                history_text = f"{status_icon} {timestamp} | {item.get('error', 'Download failed')}"

            history_list.mount(Static(history_text, classes=f"history-item {status_class}"))

    def action_quit(self) -> None:
        """退出应用"""
        if self.is_downloading:
            self.notify("⚠️ Download in progress. Press Ctrl+C again to force quit.", severity="warning")
            self.is_downloading = False
        else:
            self.exit()

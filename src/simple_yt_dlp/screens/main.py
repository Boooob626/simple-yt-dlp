"""
Main Screen - The primary download interface
"""
from textual.app import ComposeResult


class MainScreen:
    """
    Main screen mix-in class for PrivacyYouTubeDownloader

    This mix-in provides the compose method and UI structure for the main app.
    The actual App class in app.py will inherit from both textual.App and this mix-in.
    """

    def compose(self) -> ComposeResult:
        """Compose the main UI"""
        # Import here to avoid circular imports
        from textual.containers import Center, Horizontal, ScrollableContainer, Vertical
        from textual.widgets import Button, Footer, Input, Label, ProgressBar, Select, Static

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
                        [
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
                        ],
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

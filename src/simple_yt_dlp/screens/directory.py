"""
Directory Selector Screen - Modal screen for directory selection
"""
from pathlib import Path
from textual.app import ComposeResult
from textual.containers import Horizontal, Vertical
from textual.screen import Screen
from textual.widgets import Button, DirectoryTree, Input, Label


class DirectorySelector(Screen):
    """Modal screen for directory selection and manual path entry"""

    CSS = """
    .modal-container {
        width: 80%;
        height: 70%;
        align: center middle;
    }

    #modal-header {
        text-align: center;
        text-style: bold;
        color: $primary;
        margin-bottom: 1;
    }

    #path_input {
        width: 100%;
        margin: 1 0;
    }

    DirectoryTree {
        height: 1fr;
        border: round $primary-background;
    }

    .modal-buttons {
        width: 100%;
        align: center middle;
        height: 3;
        margin-top: 1;
    }

    Button {
        margin: 0 1;
    }
    """

    def __init__(self, initial_path: Path):
        super().__init__()
        self.initial_path = initial_path

    def compose(self) -> ComposeResult:
        yield Vertical(
            Label("📁 Enter or Select Download Directory", id="modal-header"),
            Input(value=str(self.initial_path), placeholder="Paste path here...", id="path_input"),
            DirectoryTree(self.initial_path.anchor),  # Start at root for flexibility
            Horizontal(
                Button("Save Path", variant="success", id="select_dir_btn"),
                Button("Cancel", variant="primary", id="cancel_dir_btn"),
                classes="modal-buttons"
            ),
            classes="modal-container"
        )

    def on_button_pressed(self, event: Button.Pressed) -> None:
        if event.button.id == "select_dir_btn":
            path_text = self.query_one("#path_input", Input).value
            self.dismiss(Path(path_text))
        elif event.button.id == "cancel_dir_btn":
            self.dismiss(None)

    def on_directory_tree_directory_selected(self, event: DirectoryTree.DirectorySelected) -> None:
        # Update the input field when a directory is clicked
        self.query_one("#path_input", Input).value = str(event.path)

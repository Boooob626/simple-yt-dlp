"""
Main Styles - CSS styles for the main application UI
"""

CSS = """
Screen {
    background: $surface;
}

#header {
    text-align: center;
    text-style: bold;
    padding: 1 0;
    color: $primary;
    margin-bottom: 1;
}

#url_container {
    width: 90%;
    margin: 1 0;
}

Input {
    width: 100%;
    border: tall $primary;
    padding: 0 1;
}

Input:focus {
    border: tall $accent;
}

#options_container {
    width: 90%;
    background: $panel;
    border: round $primary-background;
    padding: 1;
    margin: 1 0;
}

.option-label {
    color: $text-muted;
    width: 20%;
    text-align: right;
    padding-right: 1;
}

Select {
    width: 75%;
}

Horizontal.option-row {
    height: 3;
    align: center middle;
    width: 100%;
}

#privacy_section {
    background: $boost;
    border-left: thick $warning;
    padding: 1;
    margin-top: 1;
}

#title {
    width: 90%;
    margin: 1 0;
    text-align: center;
    text-style: bold;
    color: $text;
    height: auto;
}

#status {
    width: 90%;
    margin: 1 0;
    text-align: center;
    height: auto;
}

ProgressBar {
    width: 90%;
    margin: 1 0;
    height: 1;
    color: $success;
    background: $primary-background;
}

#controls {
    width: 90%;
    align: center middle;
    margin-top: 1;
    height: 3;
}

Button {
    margin: 0 1;
}

Button#download_btn {
    background: $success;
    color: $text;
}

Button#clear_btn {
    background: $warning;
    color: $text;
}

Button#cancel_btn {
    background: $error;
    color: $text;
    display: none;
}

#history_container {
    width: 90%;
    height: 8;
    margin-top: 2;
    border: round $primary-background;
    padding: 1;
}

#history_title {
    text-style: bold;
    color: $text-muted;
    margin-bottom: 1;
}

.history-item {
    padding: 0 1;
    height: 1;
}

.history-success {
    color: $success;
}

.history-error {
    color: $error;
}
"""

__all__ = ["CSS"]

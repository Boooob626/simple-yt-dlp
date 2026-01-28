"""
Main Styles - Responsive CSS styles for the main application UI
Works on all screen sizes using Textual's flexible layout system
"""

CSS = """
Screen {
    background: $surface;
    layout: vertical;
}

/* Header */
#header {
    text-align: center;
    text-style: bold;
    padding: 1;
    color: $primary;
    margin-bottom: 1;
}

/* URL Container - full width, auto height */
#url_container {
    width: 1fr;
    height: auto;
    margin: 0 1 1 1;
}

Input {
    width: 1fr;
    border: tall $primary;
    padding: 0 1;
    height: 1;
}

Input:focus {
    border: tall $accent;
}

/* Options Container */
#options_container {
    width: 1fr;
    height: auto;
    background: $panel;
    border: round $primary-background;
    padding: 1;
    margin: 0 1 1 1;
}

/* Option rows - horizontal layout with flexible widths */
Horizontal.option-row {
    width: 1fr;
    height: 3;
    align: center middle;
}

.option-label {
    color: $text-muted;
    min-width: 10;
    text-align: right;
    padding-right: 1;
}

Select {
    width: 1fr;
}

/* Privacy Section */
#privacy_section {
    background: $boost;
    border-left: thick $warning;
    padding: 1;
    margin: 0 1 1 1;
    height: auto;
}

/* Title and Status - auto height, full width */
#title {
    width: 1fr;
    margin: 0 1;
    text-align: center;
    text-style: bold;
    color: $text;
    height: auto;
}

#status {
    width: 1fr;
    margin: 0 1;
    text-align: center;
    height: auto;
}

/* Progress Bar - full width */
ProgressBar {
    width: 1fr;
    margin: 0 1 1 1;
    height: 1;
    color: $success;
    background: $primary-background;
}

/* Controls - horizontal button layout */
#controls {
    width: 1fr;
    align: center middle;
    margin: 0 1 1 1;
    height: 3;
}

Button {
    margin: 0 1;
    min-width: 12;
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

/* History Container - flexible height */
#history_container {
    width: 1fr;
    height: 1fr;
    margin: 0 1 1 1;
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
    width: 1fr;
}

.history-success {
    color: $success;
}

.history-error {
    color: $error;
}

/* Note: Textual's flexible layout (1fr, auto) naturally handles different screen sizes */
"""

__all__ = ["CSS"]

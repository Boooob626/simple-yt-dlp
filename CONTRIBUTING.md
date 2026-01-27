# Contributing to Simple YouTube Downloader

First off, thank you for considering contributing to Simple YouTube Downloader! It's people like you that make open source amazing.

## How to Contribute

### Reporting Bugs

Before creating bug reports, please check existing issues to avoid duplicates. When creating a bug report, include:

- **OS and Python version**
- **Steps to reproduce** the issue
- **Expected behavior** vs **actual behavior**
- **Debug log** from `~/.cache/simple-yt-dlp/debug.log` if applicable

### Suggesting Features

Feature suggestions are welcome! Please consider:
- Does this fit the project's privacy-first philosophy?
- Is this something many users would benefit from?
- Would you be willing to implement it?

### Development Setup

```bash
# Clone the repository
git clone https://github.com/yourname/simple-yt-dlp.git
cd simple-yt-dlp

# Create virtual environment
python -m venv .venv
source .venv/bin/activate

# Install with dev dependencies
pip install -e ".[dev]"

# Run tests
pytest

# Format code
ruff format .
ruff check .
```

### Pull Request Process

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Make your changes
4. Run tests and linting
5. Commit your changes (`git commit -m 'Add amazing feature'`)
6. Push to the branch (`git push origin feature/amazing-feature`)
7. Open a Pull Request

### Code Style

- Follow PEP 8 guidelines
- Use `ruff` for formatting and linting
- Add type hints where appropriate
- Write docstrings for new functions

## Adding Features

When adding new features, please ensure:

- [ ] Privacy is maintained (no new telemetry)
- [ ] Configuration is persisted
- [ ] Error messages are user-friendly
- [ ] Code is tested (if possible)
- [ ] README is updated (if needed)

## Questions?

Feel free to open an issue with the "question" label.

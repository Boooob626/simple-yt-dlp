# 📋 Simple YouTube Downloader - 渐进式改进计划

**日期:** 2026-01-27
**阶段:** 第一阶段 - 基础设施配置
**目标:** 将单文件脚本重构为专业级开源项目

---

## 项目目标

将 `simple-yt-dlp` 从单文件脚本重构为专业级开源项目，保持项目始终可用的同时逐步提升质量。

**核心理念:**
- 🔄 **渐进式改进** - 每个阶段项目都保持可用状态
- 🛡️ **风险控制** - 代码重构独立于配置改进
- 📈 **质量优先** - 打造能获得 Star 的精品项目

---

## 第一阶段：基础设施配置（今天执行）

### 新增文件列表

```
simple-yt-dlp/
├── pyproject.toml          # ✨ 新增 - 现代 Python 打包配置
├── README.md               # ✨ 新增 - 精品项目文档
├── LICENSE                 # ✨ 新增 - MIT 许可证
├── CONTRIBUTING.md         # ✨ 新增 - 贡献指南
├── .gitignore              # ✨ 新增 - Git 忽略规则
├── requirements.txt        # ✨ 新增 - pip 依赖列表
├── requirements-dev.txt    # ✨ 新增 - 开发依赖
│
├── .github/
│   └── workflows/
│       └── lint.yml        # ✨ 新增 - GitHub Actions 自动化
│
├── simple_yt_dlp.py        # 保持不变
├── begin.py                # 保持不变（后续归档）
├── config.py               # 保持不变
├── check_tools.py          # 保持不变
├── simple_yt_dlp.py.bak    # 保持不变
└── .venv/                  # 保持不变
```

### 关键决策

- ✅ **不移动**现有代码到 `src/` 目录，保持项目可运行
- ✅ **不修改**任何 Python 代码
- ✅ 只添加配置文件和文档
- ✅ 为未来的代码重构打好基础

---

## 配置文件内容

### 专业改进建议 💡

> 以下是来自 GitHub 社区的实战建议，帮助项目获得更多 Stars 和用户信任。

**关键改进点：**
1. 📦 **动态 yt-dlp 版本** - YouTube 频繁变化，用户需要最新版本
2. 🤖 **GitHub Actions** - 自动化 lint 检查，增加项目可信度
3. 📝 **日志系统** - 文件日志便于用户报告问题
4. 🍪 **Cookie 支持** - 支持受年龄限制的视频下载
5. 🎬 **动画演示** - GIF 比静态截图更能展示 TUI 交互
6. 🛡️ **优雅降级** - FFmpeg 缺失时自动禁用相关功能

---

### 1. pyproject.toml

```toml
[build-system]
requires = ["setuptools>=61.0", "wheel"]
build-backend = "setuptools.build_meta"

[project]
name = "simple-yt-dlp"
version = "1.0.0"
description = "Privacy-focused YouTube downloader with beautiful TUI"
readme = "README.md"
license = {text = "MIT"}
authors = [
    {name = "Your Name", email = "your.email@example.com"}
]
classifiers = [
    "Development Status :: 4 - Beta",
    "Environment :: Console",
    "Intended Audience :: End Users/Desktop",
    "License :: OSI Approved :: MIT License",
    "Programming Language :: Python :: 3.9",
    "Programming Language :: Python :: 3.10",
    "Programming Language :: Python :: 3.11",
    "Programming Language :: Python :: 3.12",
    "Topic :: Multimedia :: Video",
    "Topic :: Utilities",
]
keywords = ["youtube", "downloader", "tui", "textual", "privacy"]
requires-python = ">=3.9"
dependencies = [
    "textual>=0.80.0",
    "yt-dlp",                     # 🔥 无版本限制 - YouTube 频繁变化，用户需要最新版
    "colorama; platform_system == 'Windows'",  # Windows 颜色支持
]

[project.optional-dependencies]
dev = ["pytest>=7.0", "pytest-asyncio", "ruff>=0.1.0"]

[project.urls]
Homepage = "https://github.com/yourname/simple-yt-dlp"
Repository = "https://github.com/yourname/simple-yt-dlp"
Issues = "https://github.com/yourname/simple-yt-dlp/issues"

[project.scripts]
simple-yt-dlp = "simple_yt_dlp:main"

[tool.setuptools]
py-modules = ["simple_yt_dlp", "config", "check_tools", "begin"]

# 🔥 为第二阶段 src 布局准备的配置（当前阶段注释掉）
# [tool.setuptools.packages.find]
# where = ["src"]

[tool.ruff]
line-length = 100
target-version = "py39"
# 🔥 帮助 Ruff 理解项目结构（第二阶段启用）
# src = ["src"]

[tool.ruff.lint]
select = ["E", "F", "W", "I"]
```

**重要提示：**
- `[project.scripts]` 入口点配置：`simple-yt-dlp = "simple_yt_dlp:main"`
- 这允许安装后直接运行 `simple-yt-dlp` 命令
- `simple_yt_dlp.py` 需要添加 `main()` 函数作为入口点

**🔥 入口点实现（重要）：**
```python
# simple_yt_dlp.py 底部修改为：

def main() -> None:
    """主入口点 - 被 pip install 后的命令调用"""
    app = PrivacyYouTubeDownloader()
    app.run()

if __name__ == "__main__":
    main()
```

这样设计的好处：
- 支持直接运行：`python simple_yt_dlp.py`
- 支持安装后命令：`simple-yt-dlp`
- 便于测试和模块导入

### 2. GitHub Actions - .github/workflows/lint.yml

```yaml
name: Lint

on:
  push:
    branches: [main, develop]
  pull_request:
    branches: [main, develop]

jobs:
  ruff:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - uses: chartboost/ruff-action@v1
        with:
          args: check --output-format=github
```

### 3. .gitignore

```gitignore
# Byte-compiled / optimized / DLL files
__pycache__/
*.py[cod]
*$py.class

# C extensions
*.so

# Distribution / packaging
.Python
build/
develop-eggs/
dist/
downloads/
eggs/
.eggs/
lib/
lib64/
parts/
sdist/
var/
wheels/
pip-wheel-metadata/
share/python-wheels/
*.egg-info/
.installed.cfg
*.egg
MANIFEST

# PyInstaller
*.manifest
*.spec

# Unit test / coverage reports
htmlcov/
.tox/
.nox/
.coverage
.coverage.*
.cache
nosetests.xml
coverage.xml
*.cover
*.py,cover
.hypothesis/
.pytest_cache/

# Translations
*.mo
*.pot

# Django stuff:
*.log
local_settings.py
db.sqlite3
db.sqlite3-journal

# Flask stuff:
instance/
.webassets-cache

# Scrapy stuff:
.scrapy

# Sphinx documentation
docs/_build/

# PyBuilder
target/

# Jupyter Notebook
.ipynb_checkpoints

# IPython
profile_default/
ipython_config.py

# pyenv
.python-version

# pipenv
Pipfile.lock

# PEP 582
__pypackages__/

# Celery stuff
celerybeat-schedule
celerybeat.pid

# SageMath parsed files
*.sage.py

# Environments
.env
.venv
env/
venv/
ENV/
env.bak/
venv.bak/

# Spyder project settings
.spyderproject
.spyproject

# Rope project settings
.ropeproject

# mkdocs documentation
/site

# mypy
.mypy_cache/
.dmypy.json
dmypy.json

# Pyre type checker
.pyre/

# IDE
.vscode/
.idea/
*.swp
*.swo
*~

# Project specific
*.bak
config.json
.simple_yt_dlp_config.json
Downloads/
PrivateDownloads/

# 🔥 Cookie support - NEVER commit user credentials!
cookies.txt
*.cookies.txt

# Serena
.serena/
.spec-workflow/
```

### 4. requirements.txt

```txt
# Core dependencies
textual>=0.80.0
yt-dlp           # 🔥 无版本限制 - YouTube 频繁变化，用户需要最新版
colorama; sys_platform == 'win32'  # Windows 颜色支持
```

### 5. requirements-dev.txt

```txt
-r requirements.txt

# Development tools
pytest>=7.0
pytest-asyncio
ruff>=0.1.0
```

### 6. LICENSE (MIT)

```
MIT License

Copyright (c) 2026 Your Name

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.
```

### 7. CONTRIBUTING.md

```markdown
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
```

---

## README.md 内容

```markdown
# 🔒 Simple YouTube Downloader

> A privacy-focused YouTube video downloader with a beautiful terminal UI

[![Python](https://img.shields.io/badge/python-3.9+-blue.svg)](https://python.org)
[![Textual](https://img.shields.io/badge/textual-0.80+-green.svg)](https://textual.textualize.io)
[![License](https://img.shields.io/badge/license-MIT-purple.svg)](LICENSE)
[![Lint](https://github.com/yourname/simple-yt-dlp/actions/workflows/lint.yml/badge.svg)](https://github.com/yourname/simple-yt-dlp/actions/workflows/lint.yml)

## 🎯 Why This Exists?

In a world where every download tool tracks your usage, **simple-yt-dlp** takes a different approach:

**🔒 Privacy by Design:**
- **Zero telemetry** - No analytics, no phone-home, ever
- **Metadata stripping** - Downloads are cleaned of all identifying information
- **Isolated storage** - Downloads go to a dedicated private directory
- **No leftovers** - No infojson files or temporary metadata

**🎨 Beautiful Experience:**
- Modern TUI that's a joy to use
- Visual progress with speed and ETA
- Remember your preferences between sessions

Unlike web-based downloaders that track what you watch, or clunky command-line tools that require memorizing options, simple-yt-dlp gives you a clean, private, and beautiful way to save videos.

---

## ✨ Features

- 🎨 **Beautiful TUI** - Modern terminal interface built with [Textual](https://textual.textualize.io)
- 🛡️ **Privacy-First** - Strips metadata, no telemetry, isolated downloads
- ⚡ **Fast & Responsive** - Async execution, non-blocking UI
- 📁 **Smart Formats** - Video (MP4/MKV/WebM) & Audio (FLAC/MP3/OPUS)
- 💾 **Persistent Config** - Remembers your settings
- 📜 **Download History** - Track your recent downloads
- 🗂️ **Directory Selection** - Easy save location management
- 🍪 **Cookie Support** - Download age-restricted and private videos
- 📝 **Debug Logging** - Easy troubleshooting with file-based logs

## 📸 Screenshots

### Main Interface
<!-- TODO: Add screenshot -->
![Main Interface](assets/screenshots/main.png)

### Download in Progress
<!-- TODO: Add screenshot -->
![Downloading](assets/screenshots/downloading.png)

### Directory Selection
<!-- TODO: Add screenshot -->
![Directory Selection](assets/screenshots/directory.png)

## 🚀 Quick Start

### Prerequisites

- **Python 3.9+** - [Download Python](https://python.org)
- **FFmpeg** - Required for video merging and format conversion
  - **Linux**: `sudo apt install ffmpeg`
  - **macOS**: `brew install ffmpeg`
  - **Windows**: `winget install ffmpeg`

### Installation

#### Using pip (Recommended)

```bash
# Clone the repository
git clone https://github.com/yourname/simple-yt-dlp.git
cd simple-yt-dlp

# Install in editable mode
pip install -e .

# Run the app
simple-yt-dlp
```

#### Using uv (Faster)

```bash
# Install uv if you haven't already
pip install uv

# Clone and run
git clone https://github.com/yourname/simple-yt-dlp.git
cd simple-yt-dlp
uv run simple_yt_dlp.py
```

#### Run directly

```bash
python simple_yt_dlp.py
```

## 📋 Supported Formats

### Video Formats
| Format | Quality | Description |
|--------|---------|-------------|
| MP4 | 4K/1080p/720p/480p/360p | Universal compatibility |
| MKV | Best | Maximum quality |
| WebM | Best | High compression |
| MOV | Best | Apple compatible |

### Audio Formats
| Format | Quality | Description |
|--------|---------|-------------|
| FLAC | Lossless | Perfect for archiving |
| WAV | Lossless | Uncompressed audio |
| M4A | High | Apple AAC format |
| OPUS | High | Modern compression |
| MP3 | 192kbps | Universal compatibility |

## 🔒 Privacy Features

- ✅ Metadata stripped from all downloads
- ✅ No telemetry or phone-home
- ✅ Isolated download directory
- ✅ No infojson files saved
- ✅ User agent spoofing for bot protection
- ✅ Clean filenames with restricted characters removed

## ⌨️ Keyboard Shortcuts

| Key | Action |
|-----|--------|
| `Ctrl+C` | Quit |
| `Ctrl+D` | Clear form |
| `Ctrl+S` | Select directory |
| `Ctrl+P` | Open command palette |
| `Tab` | Navigate between fields |

## 🛠️ Development

### Setting up development environment

```bash
# Clone the repository
git clone https://github.com/yourname/simple-yt-dlp.git
cd simple-yt-dlp

# Create virtual environment
python -m venv .venv
source .venv/bin/activate  # On Windows: .venv\Scripts\activate

# Install with development dependencies
pip install -e ".[dev]"

# Run tests
pytest
```

### Code formatting

```bash
# Format code with ruff
ruff format .

# Lint code
ruff check .
```

## 🔧 Troubleshooting

### "FFmpeg not found" error

Install FFmpeg for your platform:
- **Linux**: `sudo apt install ffmpeg` (Debian/Ubuntu) or `sudo dnf install ffmpeg` (Fedora)
- **macOS**: `brew install ffmpeg`
- **Windows**: Download from [ffmpeg.org](https://ffmpeg.org/download.html) or run `winget install ffmpeg`

### "No module named 'yt_dlp'" error

```bash
pip install yt-dlp
```

### Update yt-dlp (Important!)

YouTube frequently changes its architecture, which can break older versions of yt-dlp.

```bash
# Update to the latest version
pip install -U yt-dlp

# Or if using uv
uv pip install -U yt-dlp
```

### Verify your setup

Run the included check script:

```bash
python check_tools.py
```

This will verify:
- yt-dlp installation
- FFmpeg availability
- Optional dependencies

## 📝 License

This project is licensed under the [MIT License](LICENSE).

## 🙏 Acknowledgments

- [yt-dlp](https://github.com/yt-dlp/yt-dlp) - YouTube downloader core
- [Textual](https://textual.textualize.io) - Beautiful TUI framework
- [FFmpeg](https://ffmpeg.org) - Video processing

## 🤝 Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

1. Fork the repository
2. Create your feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

## 📧 Contact

- GitHub Issues: [github.com/yourname/simple-yt-dlp/issues](https://github.com/yourname/simple-yt-dlp/issues)

---

Made with ❤️ and [Textual](https://textual.textualize.io)
```

---

## 第二阶段：代码模块化重构（后续任务）

### 🎯 专业改进目标

**基础设施增强:**
- 📝 **日志系统** - 文件日志替代 print，便于调试
- 🍪 **Cookie 支持** - 支持受年龄限制的视频
- 🛡️ **优雅降级** - FFmpeg 缺失时自动禁用相关功能

**代码质量:**
- 🧪 **单元测试** - 核心功能测试覆盖
- 📊 **类型提示** - 完整的类型注解
- 🔧 **错误处理** - 详细的异常捕获和用户友好的错误消息

---

### 目标结构

```
simple-yt-dlp/
├── pyproject.toml
├── README.md
├── LICENSE
├── .gitignore
├── requirements.txt
├── requirements-dev.txt
│
├── src/
│   └── simple_yt_dlp/
│       ├── __init__.py
│       ├── __main__.py           # 入口点
│       ├── app.py                # 主应用类 (迁移 simple_yt_dlp.py)
│       ├── screens/
│       │   ├── __init__.py
│       │   ├── main.py           # 主下载界面
│       │   └── directory.py      # 目录选择界面
│       ├── widgets/
│       │   ├── __init__.py
│       │   └── progress.py       # 自定义进度条
│       ├── styles/
│       │   ├── __init__.py
│       │   └── main.css          # 抽离的 CSS
│       ├── download/
│       │   ├── __init__.py
│       │   ├── core.py           # yt-dlp 封装
│       │   └── formats.py        # 格式配置
│       ├── config/
│       │   ├── __init__.py
│       │   └── manager.py        # 配置管理 (迁移 config.py)
│       └── utils/
│           ├── __init__.py
│           ├── validation.py     # URL 验证
│           ├── logging.py        # 日志系统
│           └── cookies.py        # Cookie 处理
│
├── scripts/
│   └── check_tools.py            # 依赖检测脚本
│
├── tests/
│   ├── __init__.py
│   ├── test_config.py
│   ├── test_download.py
│   └── test_validation.py
│
├── assets/
│   └── screenshots/
│       ├── main.png
│       ├── downloading.png
│       └── directory.png
│
└── docs/
    └── plans/
        └── 2026-01-27-refactor-design.md
```

### 重构步骤

1. **创建包结构**
   - 创建 `src/simple_yt_dlp/` 目录
   - 添加 `__init__.py` 文件

2. **迁移主应用**
   - 将 `simple_yt_dlp.py` 迁移到 `src/simple_yt_dlp/app.py`
   - 拆分 CSS 到独立文件
   - 分离 Screen 类到 `screens/` 模块

3. **模块化下载逻辑**
   - 创建 `download/core.py` 封装 yt-dlp 调用
   - 创建 `download/formats.py` 存储格式配置

4. **迁移配置管理**
   - 将 `config.py` 迁移到 `config/manager.py`
   - 添加类型提示

   **🔥 配置迁移策略（重要）：**
   - 检测旧配置文件 `~/.simple_yt_dlp_config.json`
   - 自动读取并"升级"到新格式
   - 保持向后兼容，不丢失用户设置
   ```python
   def migrate_old_config(old_path: Path, new_config: Config) -> None:
       """从旧配置迁移用户设置"""
       if old_path.exists():
           try:
               with open(old_path) as f:
                   old_data = json.load(f)
               # 迁移关键字段
               if "download_dir" in old_data:
                   new_config.download_dir = Path(old_data["download_dir"])
               # 保留旧文件作为备份
               old_path.rename(old_path.with_suffix('.json.bak'))
           except Exception as e:
               logger.warning(f"配置迁移失败: {e}")
   ```

5. **添加工具函数**
   - URL 验证逻辑
   - 文件名清理逻辑

6. **更新 pyproject.toml**
   - 修改包发现路径为 `src/`
   - 更新入口点

7. **实现日志系统** (`utils/logging.py`)
   ```python
   import logging
   from pathlib import Path

   def setup_logging() -> logging.Logger:
       """配置文件日志系统 - 用于 yt-dlp 核心逻辑"""
       log_dir = Path.home() / ".cache" / "simple-yt-dlp"
       log_dir.mkdir(parents=True, exist_ok=True)

       logger = logging.getLogger("simple-yt-dlp")
       logger.setLevel(logging.DEBUG)

       handler = logging.FileHandler(log_dir / "debug.log")
       handler.setFormatter(logging.Formatter(
           '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
       ))
       logger.addHandler(handler)

       return logger
   ```

   **🔥 日志分离策略（重要）：**
   - **UI 事件** → 使用 `self.log()` （Textual 内置）
   - **yt-dlp 核心逻辑** → 使用自定义 logger（写入文件）
   - 这样保持关注点分离，便于调试

8. **添加 Cookie 支持** (`utils/cookies.py`)
   - 支持 `cookies.txt` 文件路径配置
   - 集成到 yt-dlp 选项中
   - 添加到 .gitignore 防止意外提交

9. **添加系统诊断 "Doctor" 屏幕** (`screens/doctor.py`)
   - **快捷键：** `Ctrl+D` 或菜单按钮
   - **显示内容：**
     - FFmpeg 状态（路径、版本）
     - yt-dlp 版本（是否最新）
     - 配置文件路径
     - 下载目录状态
     - 系统信息（Python 版本、OS）

10. **实现 FFmpeg 优雅降级**
   - 检测 FFmpeg 可用性
   - 禁用需要 FFmpeg 的格式选项
   - 添加 UI 警告提示

   **🔥 具体实现代码：**
   ```python
   import shutil
   from textual.widgets import Select

   class DownloaderApp(App):
       def on_mount(self) -> None:
           self.ffmpeg_available = shutil.which('ffmpeg') is not None
           self._update_format_options()

       def _update_format_options(self) -> None:
           """根据 FFmpeg 可用性动态更新格式选项"""
           format_select = self.query_one("#format_select", Select)

           if not self.ffmpeg_available:
               # 禁用需要 FFmpeg 的格式
               # MP3, FLAC, WAV, OPUS, M4A (音频提取)
               # MP4 高质量 (需要合并音视频)
               disabled_formats = {
                   "mp3", "flac", "wav", "opus", "m4a",  # 音频
                   "mp4_best", "mkv_best", "webm_best", "mov_best"  # 高质量视频
               }

               # 过滤选项
               allowed_options = [
                   (label, value)
                   for label, value in format_select.options
                   if value not in disabled_formats
               ]
               format_select.set_options(allowed_options)

               # 显示警告
               self.notify(
                   "⚠️ FFmpeg 未检测到，已禁用需要合并/转码的格式",
                   severity="warning"
               )
   ```

---

## 第三阶段：截图制作（上线前）

### 推荐工具

**vhs** (推荐 - Charmbracelet)
```bash
# 安装 vhs
go install github.com/charmbracelet/vhs@latest

# 创建演示脚本
cat > demo.tape << 'EOF'
Output demo.gif
Set FontSize 32
Set Width 1200
Set Height 600

Sleep 1s
Type "simple-yt-dlp" Enter
Sleep 2s

# 🔥 使用 Creative Commons 视频，确保长期有效且合规
Type "https://www.youtube.com/watch?v=jNQXAC9IVRw" Enter  # "Me at the zoo" - 第一个 YouTube 视频
Sleep 5s
# ... 继续脚本
EOF

# 生成 GIF
vhs demo.tape
```

**🔥 vhs 录制建议：**
- 使用无版权/Creative Commons 视频
- 确保演示视频长期有效
- 避免使用可能被删除的热门视频
- 推荐使用 YouTube 首个视频 "Me at the zoo" (永久有效)

**terminalizer** (跨平台)
```bash
npm install -g terminalizer
terminalizer record demo
terminalizer render demo
```

**asciinema** (Linux/macOS)
```bash
pip install asciinema-cli
asciinema rec demo.cast
```

### 需要的截图

1. **主界面** - 展示完整的 TUI 界面
2. **下载中** - 展示进度条和速度显示
3. **目录选择** - 展示目录树选择界面
4. **完成状态** - 展示成功提示和历史记录

---

## 执行检查清单

### 第一阶段：今天完成

- [ ] 创建 `pyproject.toml`（包含动态 yt-dlp 版本）
- [ ] 创建 `README.md`（含 "Why This Exists" 和隐私 USP）
- [ ] 创建 `LICENSE` (MIT)
- [ ] 创建 `CONTRIBUTING.md`
- [ ] 创建 `.gitignore`
- [ ] 创建 `requirements.txt`
- [ ] 创建 `requirements-dev.txt`
- [ ] 创建 `.github/workflows/lint.yml`
- [ ] 验证 `pip install -e .` 可行
- [ ] 验证 `simple-yt-dlp` 命令可用
- [ ] 验证项目可正常运行

### 第二阶段：代码重构

- [ ] 创建 `src/simple_yt_dlp/` 结构
- [ ] 迁移主应用代码
- [ ] 拆分 Screen 模块
- [ ] 抽离 CSS 样式
- [ ] 模块化下载逻辑
- [ ] 实现日志系统 (`utils/logging.py`)
- [ ] 添加 Cookie 支持 (`utils/cookies.py`)
- [ ] 实现 Doctor 诊断屏幕 (`screens/doctor.py`)
- [ ] 实现 FFmpeg 优雅降级（动态 UI 更新）
- [ ] 实现配置迁移（向后兼容）
- [ ] 添加单元测试
- [ ] 更新文档

### 第三阶段：上线前

- [ ] 制作界面截图（静态）
- [ ] 制作 GIF 动画演示（使用 vhs + 无版权视频）
- [ ] 更新 README 截图占位符
- [ ] 添加 GitHub Actions badge 到 README
- [ ] 推送到 GitHub
- [ ] 创建 GitHub Release v1.0.0
- [ ] 编写 Release Notes

---

## 设计决策记录

| 决策 | 选择 | 理由 |
|------|------|------|
| Python 版本 | 3.9+ | 跟随 Textual 要求，覆盖最广用户 |
| 许可证 | MIT | 简单宽松，精品项目常用 |
| 依赖管理 | pip + uv | 兼容性优先，推荐现代工具 |
| 项目名称 | simple-yt-dlp | 保持现有品牌，准确传达定位 |
| 改进策略 | 渐进式 | 保持项目可用，风险可控 |
| yt-dlp 版本 | 无限制 | YouTube 频繁变化，用户需要最新版 |
| CI/CD | GitHub Actions | 自动化 lint，增加可信度 |
| 日志方式 | 文件日志 | 便于用户报告问题，不干扰 TUI |
| 截图工具 | vhs (推荐) | 可编写脚本，生成高质量 GIF |

---

## 专业改进总结

本计划整合了来自 GitHub 开源社区的深度实战建议：

### 基础设施（第一阶段）
1. **动态依赖管理** - yt-dlp 无版本限制，确保用户始终使用最新版本
2. **自动化质量保障** - GitHub Actions 自动 lint，建立项目可信度
3. **贡献文化** - CONTRIBUTING.md 鼓励社区参与
4. **隐私 USP** - README 中 "Why This Exists" 强调隐私定位
5. **入口点实现** - `main()` 函数包装，支持命令行和直接运行
6. **安全防护** - .gitignore 阻止 cookies.txt 意外提交

### 代码质量（第二阶段）
7. **生产级日志** - 文件日志 + Textual 内置日志分离
8. **功能完整性** - Cookie 支持解锁更多内容
9. **诊断能力** - "Doctor" 屏幕便于问题排查
10. **用户体验优化** - FFmpeg 优雅降级，动态禁用不可用格式
11. **向后兼容** - 配置迁移确保用户设置不丢失
12. **项目结构** - setuptools.packages.find 和 ruff src 配置

### 视觉与发布（第三阶段）
13. **视觉吸引力** - vhs 生成高质量 GIF，比静态截图更能展示 TUI 交互
14. **演示合规** - 使用无版权视频，确保长期有效
15. **专业发布** - GitHub Releases v1.0.0 正式版本

---

## "渐进式改进" 哲学

本计划的核心理念是 **"项目永远可用"**：

| 阶段 | 状态 | 可运行 | 用户影响 |
|------|------|--------|----------|
| 阶段 1 前 | 单文件脚本 | ✅ | - |
| 阶段 1 完成后 | + 配置文件 | ✅ | 更好的安装体验 |
| 阶段 2 进行中 | 模块化重构 | ✅ | 保持可用 |
| 阶段 2 完成后 | 专业架构 | ✅ | 新功能 + 更稳定 |
| 阶段 3 完成后 | 正式发布 | ✅ | 可分享的精品 |

**每个阶段结束，用户都能立即使用改进后的项目。**

---

## 参考资源

- [Python Packaging User Guide](https://packaging.python.org/)
- [Textual Documentation](https://textual.textualize.io/)
- [PEP 621 - Storing project metadata in pyproject.toml](https://peps.python.org/pep-0621/)
- [uv - Fast Python package manager](https://github.com/astral-sh/uv)

---

**文档版本:** 4.0 (整合 GitHub 社区三轮深度专业建议)
**最后更新:** 2026-01-27
**包含改进:** 15 项专业增强建议
**核心理念:** "项目永远可用" - 渐进式改进哲学

---

## 致谢

特别感谢 GitHub 开源社区提供的专业建议，这些实战经验让本计划从"代码重构"升级为"品牌建设"：
- 动态依赖管理策略
- 隐私优先的品牌定位
- 系统诊断屏幕设计
- 入口点最佳实践
- 安全防护意识

**本计划的价值不仅在于代码改进，更在于打造一个值得信赖的开源项目。**

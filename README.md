# Screenshot Tool

<div align="center">

![GitHub release](https://img.shields.io/github/v/release/liubowyf/screenshot_tool)
![GitHub](https://img.shields.io/github/license/liubowyf/screenshot_tool)
![Platform](https://img.shields.io/badge/platform-Windows-blue)
![Python](https://img.shields.io/badge/python-3.8+-blue)

**Lightweight Windows screenshot tool with multiple storage backend support**

[Features](#features) • [Quick Start](#quick-start) • [Documentation](#documentation) • [FAQ](#faq) • [中文文档](#chinese)

</div>

---

## Features

- 🚀 **Multiple Storage Backends** - HTTP, S3/MinIO, FTP, SFTP, Local filesystem
- 💾 **Memory-Only Processing** - No local file retention, screenshots deleted after upload
- 🔒 **Secure** - HTTPS support, API key authentication, configurable encryption
- ⚡ **Lightweight** - ~3MB executable, minimal resource usage
- 🎯 **Configurable** - JSON-based configuration, no code changes needed
- 📊 **Comprehensive Logging** - Detailed logs for debugging and monitoring
- 🔄 **Auto-Retry** - Intelligent retry logic with exponential backoff
- 🎨 **Flexible** - Configurable intervals, quality, and storage options

## Table of Contents

- [Quick Start](#quick-start)
- [Installation](#installation)
- [Configuration](#configuration)
- [Storage Backends](#storage-backends)
- [Usage Examples](#usage-examples)
- [Documentation](#documentation)
- [FAQ](#faq)
- [Contributing](#contributing)
- [License](#license)

## Quick Start

### Download

```bash
# Download latest release
wget https://github.com/liubowyf/screenshot_tool/releases/latest/download/ScreenCapture-Windows-exe.zip

# Or visit releases page
https://github.com/liubowyf/screenshot_tool/releases
```

### Configure

Create `config.json`:

```json
{
    "storage_type": "http",
    "interval_seconds": 5,
    "jpeg_quality": 70,
    "http": {
        "server_url": "https://your-api.com/upload",
        "api_key": "your-secret-key"
    }
}
```

### Run

```powershell
# Double-click or run
.\ScreenCapture.exe
```

That's it! Screenshots will be captured every 5 seconds and uploaded automatically.

## Installation

### Option 1: Binary Release (Recommended)

1. Download from [Releases](https://github.com/liubowyf/screenshot_tool/releases)
2. Extract to desired location
3. Edit `config.json`
4. Run `ScreenCapture.exe`

### Option 2: Build from Source

```bash
# Clone repository
git clone https://github.com/liubowyf/screenshot_tool.git
cd screenshot_tool

# Install dependencies
pip install -r requirements.txt

# Run directly
python screenshot_tool.py

# Or build executable
pip install pyinstaller
cd scripts
./build.sh  # Linux/macOS
build.bat   # Windows
```

## Configuration

### Basic Configuration

```json
{
    "storage_type": "http",
    "interval_seconds": 5,
    "jpeg_quality": 70,
    "log_level": "INFO"
}
```

### Configuration Options

| Option | Type | Default | Description |
|--------|------|---------|-------------|
| `storage_type` | string | `http` | Storage backend: `http`, `s3`, `ftp`, `sftp`, `local` |
| `interval_seconds` | integer | `5` | Screenshot interval in seconds |
| `jpeg_quality` | integer | `70` | JPEG quality (1-100) |
| `log_level` | string | `INFO` | Log level: `DEBUG`, `INFO`, `WARNING`, `ERROR` |

See [STORAGE_BACKENDS.md](docs/STORAGE_BACKENDS.md) for storage-specific options.

## Storage Backends

### HTTP/HTTPS

Perfect for REST APIs and webhooks.

```json
{
    "storage_type": "http",
    "http": {
        "server_url": "https://api.example.com/screenshots",
        "api_key": "your-api-key",
        "max_retries": 3
    }
}
```

### S3/MinIO

Ideal for cloud storage and object storage systems.

```json
{
    "storage_type": "s3",
    "s3": {
        "endpoint_url": "https://s3.amazonaws.com",
        "bucket": "my-screenshots",
        "access_key": "YOUR_ACCESS_KEY",
        "secret_key": "YOUR_SECRET_KEY"
    }
}
```

### FTP/FTPS

For traditional file servers.

```json
{
    "storage_type": "ftp",
    "ftp": {
        "host": "ftp.example.com",
        "username": "user",
        "password": "pass",
        "remote_path": "/screenshots/"
    }
}
```

📖 **[View all storage backend options →](docs/STORAGE_BACKENDS.md)**

## Usage Examples

### Automated Monitoring

```json
{
    "storage_type": "s3",
    "interval_seconds": 300,  // Every 5 minutes
    "jpeg_quality": 60,       // Lower quality for storage
    "s3": {
        "bucket": "monitoring-screenshots",
        "path_prefix": "workstation-01/"
    }
}
```

### High-Quality Archival

```json
{
    "storage_type": "local",
    "interval_seconds": 60,
    "jpeg_quality": 95,
    "local": {
        "save_path": "D:\\Archives\\Screenshots\\"
    }
}
```

### Multi-Environment Setup

Development:
```json
{
    "storage_type": "local",
    "interval_seconds": 10,
    "local": { "save_path": "./screenshots/" }
}
```

Production:
```json
{
    "storage_type": "s3",
    "interval_seconds": 5,
    "s3": { "bucket": "prod-screenshots" }
}
```

## Documentation

| Document | Description |
|----------|-------------|
| [DEPLOYMENT.md](docs/DEPLOYMENT.md) | Installation and deployment guide |
| [STORAGE_BACKENDS.md](docs/STORAGE_BACKENDS.md) | Storage configuration details |
| [TECHNICAL.md](docs/TECHNICAL.md) | Technical implementation |
| [ANTIVIRUS.md](docs/ANTIVIRUS.md) | Handling false positives |
| [CONTRIBUTING.md](CONTRIBUTING.md) | Contribution guidelines |
| [CHANGELOG.md](CHANGELOG.md) | Version history |

## FAQ

<details>
<summary><b>Does this work on Windows 7?</b></summary>

Yes, Windows 7 SP1 and later are supported.
</details>

<details>
<summary><b>How do I stop the program?</b></summary>

Open Task Manager (Ctrl+Shift+Esc), find `ScreenCapture.exe` in the Details tab, and end the process.
</details>

<details>
<summary><b>Where are the logs stored?</b></summary>

Logs are stored in `logs/screenshot_YYYYMMDD.log` in the same directory as the executable.
</details>

<details>
<summary><b>Can I capture multiple monitors?</b></summary>

Currently only the primary monitor is captured. Multi-monitor support is planned for a future release.
</details>

<details>
<summary><b>Why is my antivirus flagging this?</b></summary>

Screenshot and network functionality can trigger heuristic detection. See [ANTIVIRUS.md](docs/ANTIVIRUS.md) for solutions including code signing and whitelisting.
</details>

<details>
<summary><b>How do I auto-start on boot?</b></summary>

Use Windows Task Scheduler to create a task that runs at system startup. See [DEPLOYMENT.md](docs/DEPLOYMENT.md#auto-start) for detailed instructions.
</details>

## Performance

| Metric | Value |
|--------|-------|
| Executable Size | ~3 MB |
| Memory Usage | <50 MB |
| CPU Usage | <5% (idle) |
| Screenshot Time | <500ms |
| Startup Time | <2s |

## Roadmap

- [ ] Multi-monitor support
- [ ] Video recording mode
- [ ] Hotkey configuration
- [ ] GUI configuration tool
- [ ] Cloud service integrations (Dropbox, Google Drive)
- [ ] macOS and Linux support

## Contributing

Contributions are welcome! Please read [CONTRIBUTING.md](CONTRIBUTING.md) for details.

### Quick Start for Contributors

```bash
git clone https://github.com/liubowyf/screenshot_tool.git
cd screenshot_tool
pip install -r requirements.txt
python screenshot_tool.py
```

## Security

- Always use HTTPS for uploads
- Store API keys securely
- Regularly rotate credentials
- Review server logs for unauthorized access

## Legal Notice

⚠️ **Important:** This software is intended for legitimate monitoring purposes only.

**Requirements:**
- Obtain explicit authorization from device owners
- Comply with local privacy protection laws
- Use only for lawful purposes

**Prohibited uses:**
- Unauthorized surveillance
- Privacy invasion
- Data theft

Users are solely responsible for compliance with applicable laws.

## License

Apache License 2.0 - see [LICENSE](LICENSE)

## Acknowledgments

- [mss](https://github.com/BoboTiG/python-mss) - Fast screenshot library
- [Pillow](https://python-pillow.org/) - Image processing
- [requests](https://requests.readthedocs.io/) - HTTP client
- [boto3](https://boto3.amazonaws.com/v1/documentation/api/latest/index.html) - AWS SDK
- [paramiko](https://www.paramiko.org/) - SSH implementation

---

<div align="center">

Made with ❤️ for secure and efficient screenshot management

[⬆ Back to Top](#screenshot-tool)

</div>

---

<a name="chinese"></a>

# 截图工具

<div align="center">

![GitHub release](https://img.shields.io/github/v/release/liubowyf/screenshot_tool)
![GitHub](https://img.shields.io/github/license/liubowyf/screenshot_tool)
![Platform](https://img.shields.io/badge/platform-Windows-blue)
![Python](https://img.shields.io/badge/python-3.8+-blue)

**轻量级Windows截图工具，支持多种存储后端**

[功能特性](#功能特性) • [快速开始](#快速开始) • [文档](#文档-1) • [常见问题](#常见问题) • [English](#screenshot-tool)

</div>

---

## 功能特性

- 🚀 **多种存储后端** - HTTP、S3/MinIO、FTP、SFTP、本地文件系统
- 💾 **仅内存处理** - 本地不留存，上传后立即删除
- 🔒 **安全可靠** - HTTPS支持、API密钥认证、可配置加密
- ⚡ **轻量高效** - ~3MB可执行文件，资源占用极低
- 🎯 **灵活配置** - JSON配置，无需修改代码
- 📊 **完整日志** - 详细日志记录，便于调试监控
- 🔄 **自动重试** - 智能重试机制，指数退避
- 🎨 **高度可定制** - 可配置间隔、质量、存储方式

## 目录

- [快速开始](#快速开始)
- [安装](#安装)
- [配置](#配置-1)
- [存储后端](#存储后端)
- [使用示例](#使用示例)
- [文档](#文档-1)
- [常见问题](#常见问题)
- [贡献](#贡献)
- [许可证](#许可证)

## 快速开始

### 下载

```bash
# 下载最新版本
wget https://github.com/liubowyf/screenshot_tool/releases/latest/download/ScreenCapture-Windows-exe.zip

# 或访问发布页面
https://github.com/liubowyf/screenshot_tool/releases
```

### 配置

创建 `config.json`：

```json
{
    "storage_type": "http",
    "interval_seconds": 5,
    "jpeg_quality": 70,
    "http": {
        "server_url": "https://your-api.com/upload",
        "api_key": "your-secret-key"
    }
}
```

### 运行

```powershell
# 双击或运行
.\ScreenCapture.exe
```

完成！程序将每5秒自动截图并上传。

## 安装

### 方式一：二进制版本（推荐）

1. 从[Releases](https://github.com/liubowyf/screenshot_tool/releases)下载
2. 解压到目标位置
3. 编辑`config.json`
4. 运行`ScreenCapture.exe`

### 方式二：从源码构建

```bash
# 克隆仓库
git clone https://github.com/liubowyf/screenshot_tool.git
cd screenshot_tool

# 安装依赖
pip install -r requirements.txt

# 直接运行
python screenshot_tool.py

# 或构建可执行文件
pip install pyinstaller
cd scripts
./build.sh  # Linux/macOS
build.bat   # Windows
```

## 配置

### 基础配置

```json
{
    "storage_type": "http",
    "interval_seconds": 5,
    "jpeg_quality": 70,
    "log_level": "INFO"
}
```

### 配置选项

| 选项 | 类型 | 默认值 | 描述 |
|------|------|--------|------|
| `storage_type` | string | `http` | 存储后端：`http`、`s3`、`ftp`、`sftp`、`local` |
| `interval_seconds` | integer | `5` | 截图间隔（秒） |
| `jpeg_quality` | integer | `70` | JPEG质量（1-100） |
| `log_level` | string | `INFO` | 日志级别：`DEBUG`、`INFO`、`WARNING`、`ERROR` |

存储特定选项见[STORAGE_BACKENDS.md](docs/STORAGE_BACKENDS.md)。

## 存储后端

### HTTP/HTTPS

适用于REST API和Webhook。

```json
{
    "storage_type": "http",
    "http": {
        "server_url": "https://api.example.com/screenshots",
        "api_key": "your-api-key",
        "max_retries": 3
    }
}
```

### S3/MinIO

适用于云存储和对象存储系统。

```json
{
    "storage_type": "s3",
    "s3": {
        "endpoint_url": "https://s3.amazonaws.com",
        "bucket": "my-screenshots",
        "access_key": "YOUR_ACCESS_KEY",
        "secret_key": "YOUR_SECRET_KEY"
    }
}
```

### FTP/FTPS

适用于传统文件服务器。

```json
{
    "storage_type": "ftp",
    "ftp": {
        "host": "ftp.example.com",
        "username": "user",
        "password": "pass",
        "remote_path": "/screenshots/"
    }
}
```

📖 **[查看所有存储选项 →](docs/STORAGE_BACKENDS.md)**

## 使用示例

### 自动监控

```json
{
    "storage_type": "s3",
    "interval_seconds": 300,  // 每5分钟
    "jpeg_quality": 60,       // 降低质量节省存储
    "s3": {
        "bucket": "monitoring-screenshots",
        "path_prefix": "workstation-01/"
    }
}
```

### 高质量归档

```json
{
    "storage_type": "local",
    "interval_seconds": 60,
    "jpeg_quality": 95,
    "local": {
        "save_path": "D:\\Archives\\Screenshots\\"
    }
}
```

## 文档

| 文档 | 说明 |
|------|------|
| [DEPLOYMENT.md](docs/DEPLOYMENT.md) | 安装部署指南 |
| [STORAGE_BACKENDS.md](docs/STORAGE_BACKENDS.md) | 存储配置详情 |
| [TECHNICAL.md](docs/TECHNICAL.md) | 技术实现 |
| [ANTIVIRUS.md](docs/ANTIVIRUS.md) | 误报处理 |
| [CONTRIBUTING.md](CONTRIBUTING.md) | 贡献指南 |
| [CHANGELOG.md](CHANGELOG.md) | 版本历史 |

## 常见问题

<details>
<summary><b>支持Windows 7吗？</b></summary>

支持Windows 7 SP1及更高版本。
</details>

<details>
<summary><b>如何停止程序？</b></summary>

打开任务管理器（Ctrl+Shift+Esc），在"详细信息"选项卡中找到`ScreenCapture.exe`，结束进程。
</details>

<details>
<summary><b>日志存储在哪里？</b></summary>

日志存储在可执行文件同目录的`logs/screenshot_YYYYMMDD.log`。
</details>

<details>
<summary><b>可以捕获多个显示器吗？</b></summary>

当前仅捕获主显示器。多显示器支持计划在未来版本中实现。
</details>

<details>
<summary><b>为什么杀毒软件报警？</b></summary>

截图和网络功能可能触发启发式检测。解决方案见[ANTIVIRUS.md](docs/ANTIVIRUS.md)，包括代码签名和白名单。
</details>

<details>
<summary><b>如何开机自启动？</b></summary>

使用Windows任务计划程序创建系统启动时运行的任务。详细步骤见[DEPLOYMENT.md](docs/DEPLOYMENT.md#auto-start)。
</details>

## 性能

| 指标 | 数值 |
|------|------|
| 可执行文件大小 | ~3 MB |
| 内存占用 | <50 MB |
| CPU占用 | <5% (空闲) |
| 截图耗时 | <500ms |
| 启动时间 | <2s |

## 路线图

- [ ] 多显示器支持
- [ ] 视频录制模式
- [ ] 快捷键配置
- [ ] GUI配置工具
- [ ] 云服务集成（Dropbox、Google Drive）
- [ ] macOS和Linux支持

## 贡献

欢迎贡献！详情请阅读[CONTRIBUTING.md](CONTRIBUTING.md)。

## 安全

- 始终使用HTTPS上传
- 安全存储API密钥
- 定期轮换凭证
- 审查服务器日志

## 法律声明

⚠️ **重要：** 本软件仅用于合法监控目的。

**要求：**
- 获得设备所有者明确授权
- 遵守当地隐私保护法律
- 仅用于合法目的

**禁止用途：**
- 未授权监控
- 侵犯隐私
- 数据窃取

用户需自行确保遵守相关法律。

## 许可证

Apache License 2.0 - 见[LICENSE](LICENSE)

## 致谢

- [mss](https://github.com/BoboTiG/python-mss) - 快速截图库
- [Pillow](https://python-pillow.org/) - 图像处理
- [requests](https://requests.readthedocs.io/) - HTTP客户端
- [boto3](https://boto3.amazonaws.com/v1/documentation/api/latest/index.html) - AWS SDK
- [paramiko](https://www.paramiko.org/) - SSH实现

---

<div align="center">

用 ❤️ 打造的安全高效截图管理工具

[⬆ 返回顶部](#截图工具)

</div>

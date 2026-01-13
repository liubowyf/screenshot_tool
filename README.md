# Screenshot Tool / 截图工具

<div align="center">

![GitHub release](https://img.shields.io/github/v/release/liubowyf/screenshot_tool)
![GitHub](https://img.shields.io/github/license/liubowyf/screenshot_tool)
![Platform](https://img.shields.io/badge/platform-Windows-blue)
![Python](https://img.shields.io/badge/python-3.8+-blue)

**轻量级Windows截图工具，支持多种存储后端**

[中文](#chinese) • [English](#english)

</div>

---

<a name="chinese"></a>

# 中文文档

## 功能特性

- 🚀 **多种存储后端** - HTTP、S3/MinIO、FTP、SFTP、本地文件系统
- 💾 **仅内存处理** - 本地不留存，上传后立即删除
- 🔒 **安全可靠** - HTTPS支持、API密钥认证
- ⚡ **轻量高效** - ~3MB可执行文件，资源占用极低
- 🎯 **灵活配置** - JSON配置，无需修改代码
- 📊 **完整日志** - 详细日志记录，便于调试监控
- 🔄 **自动重试** - 智能重试机制，指数退避
- 🎨 **高度可定制** - 可配置间隔、质量、存储方式

## 目录

- [快速开始](#快速开始)
- [安装](#安装)
- [配置](#配置-1)
- [存储后端](#存储后端-1)
- [使用示例](#使用示例)
- [文档](#文档-1)
- [常见问题](#常见问题)
- [贡献](#贡献-1)
- [许可证](#许可证-1)

## 快速开始

### 下载

访问 [Releases](https://github.com/liubowyf/screenshot_tool/releases) 下载最新版本

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

双击 `ScreenCapture.exe` 或在命令行运行。

## 安装

### 方式一：使用预编译版本（推荐）

1. 从 [Releases](https://github.com/liubowyf/screenshot_tool/releases) 下载
2. 解压到目标位置
3. 编辑 `config.json`
4. 运行 `ScreenCapture.exe`

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
| `storage_type` | string | `http` | 存储后端类型 |
| `interval_seconds` | integer | `5` | 截图间隔（秒） |
| `jpeg_quality` | integer | `70` | JPEG质量（1-100） |
| `log_level` | string | `INFO` | 日志级别 |

详细存储配置见 [STORAGE_BACKENDS.md](docs/STORAGE_BACKENDS.md)

## 存储后端

### HTTP/HTTPS

适用于REST API和Webhook：

```json
{
    "storage_type": "http",
    "http": {
        "server_url": "https://api.example.com/screenshots",
        "api_key": "your-api-key"
    }
}
```

### S3/MinIO

适用于云存储和对象存储：

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

适用于传统文件服务器：

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
    "jpeg_quality": 60,
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

打开任务管理器（Ctrl+Shift+Esc），在"详细信息"选项卡找到 `ScreenCapture.exe`，结束进程。
</details>

<details>
<summary><b>日志存储在哪里？</b></summary>

日志存储在可执行文件同目录的 `logs/screenshot_YYYYMMDD.log`。
</details>

<details>
<summary><b>可以捕获多个显示器吗？</b></summary>

当前仅捕获主显示器。多显示器支持计划在未来版本实现。
</details>

<details>
<summary><b>为什么杀毒软件报警？</b></summary>

截图和网络功能可能触发启发式检测。解决方案见 [ANTIVIRUS.md](docs/ANTIVIRUS.md)。
</details>

<details>
<summary><b>如何开机自启动？</b></summary>

使用Windows任务计划程序创建系统启动时运行的任务。详见 [DEPLOYMENT.md](docs/DEPLOYMENT.md)。
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

欢迎贡献！详情请阅读 [CONTRIBUTING.md](CONTRIBUTING.md)。

### 开发者快速开始

```bash
git clone https://github.com/liubowyf/screenshot_tool.git
cd screenshot_tool
pip install -r requirements.txt
python screenshot_tool.py
```

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

Apache License 2.0 - 见 [LICENSE](LICENSE)

## 致谢

- [mss](https://github.com/BoboTiG/python-mss) - 快速截图库
- [Pillow](https://python-pillow.org/) - 图像处理
- [requests](https://requests.readthedocs.io/) - HTTP客户端
- [boto3](https://boto3.amazonaws.com/v1/documentation/api/latest/index.html) - AWS SDK
- [paramiko](https://www.paramiko.org/) - SSH实现

---

<div align="center">

用 ❤️ 打造的安全高效截图管理工具

[⬆ 返回顶部](#screenshot-tool--截图工具)

</div>

---

<a name="english"></a>

# English Documentation

## Features

- 🚀 **Multiple Storage Backends** - HTTP, S3/MinIO, FTP, SFTP, Local filesystem
- 💾 **Memory-Only Processing** - No local file retention
- 🔒 **Secure** - HTTPS support, API key authentication
- ⚡ **Lightweight** - ~3MB executable, minimal resource usage
- 🎯 **Configurable** - JSON-based configuration
- 📊 **Comprehensive Logging** - Detailed logs for debugging
- 🔄 **Auto-Retry** - Intelligent retry logic with exponential backoff
- 🎨 **Flexible** - Configurable intervals, quality, and storage options

## Table of Contents

- [Quick Start](#quick-start-1)
- [Installation](#installation-1)
- [Configuration](#configuration-1)
- [Storage Backends](#storage-backends-2)
- [Usage Examples](#usage-examples-1)
- [Documentation](#documentation-1)
- [FAQ](#faq-1)
- [Contributing](#contributing-1)
- [License](#license-1)

## Quick Start

### Download

Visit [Releases](https://github.com/liubowyf/screenshot_tool/releases) to download the latest version.

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

Double-click `ScreenCapture.exe` or run from command line.

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
| `storage_type` | string | `http` | Storage backend type |
| `interval_seconds` | integer | `5` | Screenshot interval in seconds |
| `jpeg_quality` | integer | `70` | JPEG quality (1-100) |
| `log_level` | string | `INFO` | Log level |

See [STORAGE_BACKENDS.md](docs/STORAGE_BACKENDS.md) for storage-specific options.

## Storage Backends

### HTTP/HTTPS

Perfect for REST APIs and webhooks:

```json
{
    "storage_type": "http",
    "http": {
        "server_url": "https://api.example.com/screenshots",
        "api_key": "your-api-key"
    }
}
```

### S3/MinIO

Ideal for cloud storage and object storage:

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

For traditional file servers:

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
    "jpeg_quality": 60,
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

## Documentation

| Document | Description |
|----------|-------------|
| [DEPLOYMENT.md](docs/DEPLOYMENT.md) | Installation and deployment |
| [STORAGE_BACKENDS.md](docs/STORAGE_BACKENDS.md) | Storage configuration |
| [TECHNICAL.md](docs/TECHNICAL.md) | Technical details |
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

Open Task Manager (Ctrl+Shift+Esc), find `ScreenCapture.exe` in Details tab, and end the process.
</details>

<details>
<summary><b>Where are the logs stored?</b></summary>

Logs are in `logs/screenshot_YYYYMMDD.log` in the same directory as the executable.
</details>

<details>
<summary><b>Can I capture multiple monitors?</b></summary>

Currently only the primary monitor is captured. Multi-monitor support is planned.
</details>

<details>
<summary><b>Why is my antivirus flagging this?</b></summary>

Screenshot and network functionality can trigger heuristic detection. See [ANTIVIRUS.md](docs/ANTIVIRUS.md) for solutions.
</details>

<details>
<summary><b>How do I auto-start on boot?</b></summary>

Use Windows Task Scheduler to create a task that runs at system startup. See [DEPLOYMENT.md](docs/DEPLOYMENT.md) for details.
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

[⬆ Back to Top](#screenshot-tool--截图工具)

</div>

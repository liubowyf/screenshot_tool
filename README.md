# Screenshot Tool / 截图工具

[English](#english) | [中文](#chinese)

<a name="english"></a>
## English

A lightweight Windows screenshot tool with automatic upload capabilities.

### Features

- Automatic screenshot capture at configurable intervals
- Multiple storage backend support (HTTP, S3, FTP, SFTP, Local)
- Memory-only processing - no local file retention
- Stealthy operation with no visible console
- Configurable image quality and upload retry logic
- Comprehensive logging

### Quick Start

**Download:** [Latest Release](https://github.com/liubowyf/screenshot_tool/releases)

**Configure** `config.json`:
```json
{
    "storage_type": "http",
    "interval_seconds": 5,
    "jpeg_quality": 70,
    "http": {
        "server_url": "https://your-server.com/upload",
        "api_key": "your-api-key"
    }
}
```

**Run:** Double-click `ScreenCapture.exe`

### Storage Backends

See [STORAGE_BACKENDS.md](docs/STORAGE_BACKENDS.md) for detailed configuration.

**HTTP/HTTPS** - Web API endpoints  
**S3/MinIO** - Object storage  
**FTP/FTPS** - File servers  
**SFTP** - Secure SSH transfer  
**Local** - Local filesystem

### Building from Source

```bash
pip install -r requirements.txt
pip install pyinstaller
```

Windows: `build.bat`  
Linux/macOS: `./build.sh`

### Documentation

- [DEPLOYMENT.md](docs/DEPLOYMENT.md) - Deployment guide
- [STORAGE_BACKENDS.md](docs/STORAGE_BACKENDS.md) - Storage configuration
- [TECHNICAL.md](docs/TECHNICAL.md) - Technical details
- [ANTIVIRUS.md](docs/ANTIVIRUS.md) - Handling false positives

### Legal Notice

This software is intended for legitimate monitoring purposes only. Users must obtain proper authorization and comply with applicable privacy laws.

### License

Apache License 2.0

---

<a name="chinese"></a>
## 中文

轻量级Windows自动截图工具，支持多种存储方式。

### 功能特性

- 可配置间隔的自动截图
- 多种存储后端支持（HTTP、S3、FTP、SFTP、本地）
- 仅内存处理，本地不留存
- 后台静默运行
- 可配置图片质量和重试逻辑
- 完整的日志记录

### 快速开始

**下载：** [最新版本](https://github.com/liubowyf/screenshot_tool/releases)

**配置** `config.json`：
```json
{
    "storage_type": "http",
    "interval_seconds": 5,
    "jpeg_quality": 70,
    "http": {
        "server_url": "https://your-server.com/upload",
        "api_key": "your-api-key"
    }
}
```

**运行：** 双击 `ScreenCapture.exe`

### 存储后端

详细配置见 [STORAGE_BACKENDS.md](docs/STORAGE_BACKENDS.md)

**HTTP/HTTPS** - Web API接口  
**S3/MinIO** - 对象存储  
**FTP/FTPS** - 文件服务器  
**SFTP** - SSH安全传输  
**Local** - 本地文件系统

### 从源码构建

```bash
pip install -r requirements.txt
pip install pyinstaller
```

Windows: `build.bat`  
Linux/macOS: `./build.sh`

### 文档

- [DEPLOYMENT.md](docs/DEPLOYMENT.md) - 部署指南
- [STORAGE_BACKENDS.md](docs/STORAGE_BACKENDS.md) - 存储配置
- [TECHNICAL.md](docs/TECHNICAL.md) - 技术细节
- [ANTIVIRUS.md](docs/ANTIVIRUS.md) - 误报处理

### 法律声明

本软件仅用于合法监控目的。使用前必须获得适当授权并遵守相关隐私法律。

### 开源协议

Apache License 2.0

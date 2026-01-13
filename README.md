# Windows Screenshot Tool

[English](#english) | [中文](#chinese)

<a name="english"></a>
## 🎯 Overview

A lightweight, stealthy Windows screenshot automation tool that captures screenshots at regular intervals and uploads them to a remote server.

**Key Features:**
- ✅ **Stealth Mode**: No console window, no popups
- ✅ **No Local Storage**: Screenshots processed in memory only, deleted after upload
- ✅ **Standalone**: Exe includes all runtime dependencies, no Python installation needed
- ✅ **Lightweight**: Packed exe only 2-4 MB
- ✅ **High Performance**: Fast screenshot capture (<500ms using mss library)
- ✅ **Reliable**: Network retry mechanism with exponential backoff
- ✅ **Configurable**: JSON-based configuration, no code modification needed
- ✅ **Smart Naming**: Filenames include computer name and timestamp for easy identification
- ✅ **Compatible**: Works on Windows 7/8/10/11 without admin privileges

## 📦 Project Structure

```
screenshot_tool/
├── .github/
│   └── workflows/
│       └── build-windows.yml    # GitHub Actions CI/CD
├── screenshot_tool.py           # Main program
├── config.json                  # Configuration file
├── requirements.txt             # Python dependencies
├── version_info.txt             # Windows exe metadata
├── .gitignore                   # Git ignore rules
├── LICENSE                      # MIT License
├── README.md                    # This file
└── docs/                        # Documentation
    ├── DEPLOYMENT.md            # Deployment guide
    ├── TECHNICAL.md             # Technical implementation details
    ├── BUILD_ON_MACOS.md        # Build on macOS guide
    ├── ANTIVIRUS.md             # Antivirus false positive solutions
    └── PACKAGING_COMPARISON.md  # Packaging methods comparison
```

## 🚀 Quick Start

### Method 1: Use Pre-built Exe (Recommended)

1. Download the latest release from [Releases](https://github.com/yourusername/screenshot_tool/releases)
2. Edit `config.json`:
   ```json
   {
       "server_url": "https://your-server.com/upload",
       "api_key": "your-api-key",
       "interval_seconds": 5
   }
   ```
3. Double-click `ScreenCapture.exe` to run

### Method 2: Build from Source

**On Windows:**
```cmd
pip install -r requirements.txt
pip install pyinstaller
build.bat
```

**On macOS/Linux:**
```bash
chmod +x build.sh
./build.sh  # Generates macOS/Linux executable
```

**Cross-platform (macOS → Windows exe):**
See [BUILD_ON_MACOS.md](docs/BUILD_ON_MACOS.md) for Docker or GitHub Actions solutions

## 🔧 Configuration

Edit `config.json`:

| Parameter | Description | Default |
|-----------|-----------|---------|
| `storage_type` | Storage backend type (http/s3/ftp/sftp/local) | http |
| `interval_seconds` | Screenshot interval (seconds) | 5 |
| `jpeg_quality` | JPEG compression quality (1-100) | 70 |
| `log_level` | Log level (DEBUG/INFO/WARNING/ERROR) | INFO |

### Storage Backend Options

Choose your preferred storage method by setting `storage_type`:

#### HTTP/HTTPS (Default)
```json
{
    "storage_type": "http",
    "http": {
        "server_url": "https://your-server.com/upload",
        "api_key": "your-api-key",
        "max_retries": 3
    }
}
```

#### S3/MinIO (Object Storage)
```json
{
    "storage_type": "s3",
    "s3": {
        "endpoint_url": "http://localhost:9000",
        "access_key": "minioadmin",
        "secret_key": "minioadmin",
        "bucket": "screenshots"
    }
}
```

#### FTP/FTPS
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

#### Local File System
```json
{
    "storage_type": "local",
    "local": {
        "save_path": "C:\\\\Screenshots\\\\"
    }
}
```

**See [STORAGE_BACKENDS.md](docs/STORAGE_BACKENDS.md) for detailed configuration guide.**

## 🌐 Server Requirements

Your server needs to accept HTTP POST with multipart/form-data:

```http
POST /upload HTTP/1.1
Content-Type: multipart/form-data
X-API-Key: your-api-key

file: COMPUTERNAME-20260113091530.jpg
```

### Simple Flask Server Example

```python
from flask import Flask, request
import os

app = Flask(__name__)

@app.route('/upload', methods=['POST'])
def upload():
    if request.headers.get('X-API-Key') != 'your-api-key':
        return {'error': 'Unauthorized'}, 401
    
    file = request.files['file']
    file.save(f'uploads/{file.filename}')
    return {'status': 'success'}, 200

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
```

## 📊 Performance

| Metric | Value |
|--------|-------|
| Exe Size | 2-4 MB |
| Memory Usage | < 50 MB |
| CPU Usage | < 5% (idle) |
| Screenshot Time | < 500 ms |
| Upload Time | 1-3 s (depends on network) |

## ⚠️ Legal Notice

> [!CAUTION]
> **Important Legal Requirements**
> 
> Before using this tool, you MUST:
> 1. ✅ Obtain explicit written authorization from device owner
> 2. ✅ Comply with local privacy protection laws (GDPR, etc.)
> 3. ✅ Use only for legitimate monitoring purposes (parental control, employee monitoring with consent, etc.)
> 
> **Prohibited Uses:**
> - ❌ Unauthorized surveillance
> - ❌ Stealing trade secrets
> - ❌ Privacy invasion
> 
> Users are solely responsible for all legal consequences.

## 🛡️ Antivirus False Positives

Due to screenshot and network upload functionality, some antivirus software may flag this as suspicious.

**Solutions:**
1. Add exe to antivirus whitelist
2. Use code signing certificate (recommended for production)
3. Build with Nuitka instead of PyInstaller (lower false positive rate)

See [ANTIVIRUS.md](docs/ANTIVIRUS.md) for detailed solutions.

## 📚 Documentation

- [DEPLOYMENT.md](docs/DEPLOYMENT.md) - Detailed deployment guide
- [TECHNICAL.md](docs/TECHNICAL.md) - Technical implementation details
- [STORAGE_BACKENDS.md](docs/STORAGE_BACKENDS.md) - **Storage backend configuration guide**
- [BUILD_ON_MACOS.md](docs/BUILD_ON_MACOS.md) - Cross-platform build guide
- [ANTIVIRUS.md](docs/ANTIVIRUS.md) - Antivirus solutions
- [PACKAGING_COMPARISON.md](docs/PACKAGING_COMPARISON.md) - Packaging methods comparison

## 🤝 Contributing

Contributions are welcome! Please feel free to submit issues and pull requests.

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 🙏 Acknowledgments

- [mss](https://github.com/BoboTiG/python-mss) - Fast screenshot library
- [Pillow](https://python-pillow.org/) - Image processing
- [requests](https://requests.readthedocs.io/) - HTTP client
- [PyInstaller](https://www.pyinstaller.org/) - Python to exe packaging

---

<a name="chinese"></a>
## 🎯 项目概述

一个轻量级、隐蔽的Windows自动截图工具，定时截图并上传到远程服务器。

**核心特性：**
- ✅ **无感运行**：无控制台窗口、无弹窗提示
- ✅ **本地不留存**：截图仅在内存中处理，上传后立即删除
- ✅ **完全独立**：exe自带所有运行时，无需安装Python
- ✅ **轻量级**：打包后exe大小仅2-4 MB
- ✅ **高性能**：快速截图（<500ms，使用mss库）
- ✅ **稳定可靠**：网络重试机制，指数退避
- ✅ **灵活配置**：JSON配置文件，无需修改代码
- ✅ **智能命名**：文件名包含计算机名和时间戳
- ✅ **兼容性强**：支持Windows 7/8/10/11，无需管理员权限

## 🚀 快速开始

### 方式一：使用预编译exe（推荐）

1. 从 [Releases](https://github.com/yourusername/screenshot_tool/releases) 下载最新版本
2. 编辑 `config.json`：
   ```json
   {
       "server_url": "https://your-server.com/upload",
       "api_key": "your-api-key",
       "interval_seconds": 5
   }
   ```
3. 双击运行 `ScreenCapture.exe`

### 方式二：从源码构建

**Windows系统：**
```cmd
pip install -r requirements.txt
pip install pyinstaller
build.bat
```

**macOS/Linux系统：**
```bash
chmod +x build.sh
./build.sh  # 生成macOS/Linux可执行文件
```

**跨平台构建（macOS → Windows exe）：**
查看 [BUILD_ON_MACOS.md](docs/BUILD_ON_MACOS.md) 了解Docker或GitHub Actions方案

## 🔧 配置说明

编辑 `config.json`：

| 参数 | 说明 | 默认值 |
|------|------|--------|
| `storage_type` | 存储后端类型 (http/s3/ftp/sftp/local) | http |
| `interval_seconds` | 截图间隔（秒） | 5 |
| `jpeg_quality` | JPEG压缩质量（1-100） | 70 |
| `log_level` | 日志级别 | INFO |

### 存储后端选项

通过设置 `storage_type` 选择存储方式：

#### HTTP/HTTPS（默认）
```json
{
    "storage_type": "http",
    "http": {
        "server_url": "https://your-server.com/upload",
        "api_key": "your-api-key"
    }
}
```

#### S3/MinIO（对象存储）
```json
{
    "storage_type": "s3",
    "s3": {
        "endpoint_url": "http://localhost:9000",
        "bucket": "screenshots"
    }
}
```

#### FTP/FTPS
```json
{
    "storage_type": "ftp",
    "ftp": {
        "host": "ftp.example.com",
        "remote_path": "/screenshots/"
    }
}
```

#### 本地文件系统
```json
{
    "storage_type": "local",
    "local": {
        "save_path": "C:\\\\Screenshots\\\\"
    }
}
```

**详细配置说明见 [STORAGE_BACKENDS.md](docs/STORAGE_BACKENDS.md)**

## ⚠️ 法律声明

> [!CAUTION]
> **重要法律提示**
> 
> 使用前必须：
> 1. ✅ 获得设备所有者的明确书面授权
> 2. ✅ 遵守当地隐私保护法律法规
> 3. ✅ 仅用于合法监控目的
> 
> **禁止用于**：
> - ❌ 未经授权监控
> - ❌ 窃取商业机密
> - ❌ 侵犯个人隐私

## 📄 开源协议

本项目采用 MIT 协议 - 详见 [LICENSE](LICENSE) 文件

## 📚 更多文档

- [部署指南](docs/DEPLOYMENT.md)
- [技术实现](docs/TECHNICAL.md)
- [**存储后端配置**](docs/STORAGE_BACKENDS.md)
- [macOS构建指南](docs/BUILD_ON_MACOS.md)
- [杀毒软件误报解决方案](docs/ANTIVIRUS.md)

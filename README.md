# Screenshot Tool

A lightweight Windows screenshot tool with automatic upload capabilities.

## Features

- Automatic screenshot capture at configurable intervals
- Multiple storage backend support (HTTP, S3, FTP, SFTP, Local)
- Memory-only processing - no local file retention
- Stealthy operation with no visible console
- Configurable image quality and upload retry logic
- Comprehensive logging

## Quick Start

### Download

Download the latest release from [Releases](https://github.com/liubowyf/screenshot_tool/releases).

### Configuration

Create or edit `config.json`:

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

### Run

```cmd
ScreenCapture.exe
```

## Storage Backends

### HTTP/HTTPS
```json
{
    "storage_type": "http",
    "http": {
        "server_url": "https://api.example.com/upload",
        "api_key": "your-key",
        "max_retries": 3
    }
}
```

### S3/MinIO
```json
{
    "storage_type": "s3",
    "s3": {
        "endpoint_url": "http://localhost:9000",
        "access_key": "your-access-key",
        "secret_key": "your-secret-key",
        "bucket": "screenshots"
    }
}
```

### FTP
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

### Local Storage
```json
{
    "storage_type": "local",
    "local": {
        "save_path": "C:\\Screenshots\\"
    }
}
```

See [STORAGE_BACKENDS.md](docs/STORAGE_BACKENDS.md) for detailed configuration.

## Server Example

Simple Flask server to receive uploads:

```python
from flask import Flask, request

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

## Building from Source

### Windows
```cmd
pip install -r requirements.txt
pip install pyinstaller
build.bat
```

### Linux/macOS
```bash
pip install -r requirements.txt
pip install pyinstaller
chmod +x build.sh
./build.sh
```

Note: Building on non-Windows platforms will produce executables for that platform only. Use GitHub Actions for automated Windows builds.

## Documentation

- [DEPLOYMENT.md](docs/DEPLOYMENT.md) - Deployment guide
- [STORAGE_BACKENDS.md](docs/STORAGE_BACKENDS.md) - Storage configuration
- [TECHNICAL.md](docs/TECHNICAL.md) - Technical details
- [ANTIVIRUS.md](docs/ANTIVIRUS.md) - Handling false positives

## Requirements

- Python 3.8+ (for building)
- Windows 7+ (for running the exe)

### Dependencies

- `mss` - Screenshot capture
- `Pillow` - Image processing
- `requests` - HTTP uploads
- `boto3` - S3 support (optional)
- `paramiko` - SFTP support (optional)

## Legal Notice

This software is intended for legitimate monitoring purposes only. Users must:

1. Obtain explicit authorization from device owners
2. Comply with local privacy laws and regulations
3. Use only for lawful purposes

Users are solely responsible for ensuring compliance with applicable laws.

## License

Apache License 2.0 - see [LICENSE](LICENSE) for details.

## Contributing

Contributions are welcome. Please feel free to submit issues and pull requests.

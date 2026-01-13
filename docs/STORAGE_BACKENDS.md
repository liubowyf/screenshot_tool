# 存储后端配置 / Storage Backend Configuration

[中文](#chinese) | [English](#english)

<a name="chinese"></a>
## 中文

### 概述

截图工具支持多种存储后端以适应不同部署场景。

### 配置方法

在 `config.json` 中设置 `storage_type`：

- `http` - HTTP/HTTPS API接口
- `s3` - S3兼容对象存储
- `ftp` - FTP/FTPS服务器
- `sftp` - SSH文件传输
- `local` - 本地文件系统

### HTTP/HTTPS

```json
{
    "storage_type": "http",
    "http": {
        "server_url": "https://api.example.com/upload",
        "api_key": "your-api-key",
        "max_retries": 3
    }
}
```

**要求：** 接受 `multipart/form-data` POST请求，成功时返回HTTP 200。

### S3/MinIO

```json
{
    "storage_type": "s3",
    "s3": {
        "endpoint_url": "http://minio.example.com:9000",
        "access_key": "ACCESS_KEY",
        "secret_key": "SECRET_KEY",
        "bucket": "screenshots",
        "region": "us-east-1",
        "path_prefix": "daily/"
    }
}
```

兼容AWS S3、MinIO及其他S3兼容服务。

### FTP/FTPS

```json
{
    "storage_type": "ftp",
    "ftp": {
        "host": "ftp.example.com",
        "port": 21,
        "username": "ftpuser",
        "password": "ftppass",
        "remote_path": "/screenshots/",
        "use_tls": false
    }
}
```

### SFTP

```json
{
    "storage_type": "sftp",
    "sftp": {
        "host": "sftp.example.com",
        "port": 22,
        "username": "user",
        "password": "pass",
        "remote_path": "/home/user/screenshots/"
    }
}
```

**SSH密钥：** 使用 `private_key_path` 代替 `password`。

### 本地存储

```json
{
    "storage_type": "local",
    "local": {
        "save_path": "C:\\Screenshots\\"
    }
}
```

### 依赖包

| 后端 | 包名 | 安装方式 |
|------|------|----------|
| HTTP | `requests` | 已包含 |
| S3 | `boto3` | `pip install boto3` |
| FTP | 内置 | 无需安装 |
| SFTP | `paramiko` | `pip install paramiko` |
| Local | 内置 | 无需安装 |

---

<a name="english"></a>
## English

### Overview

The screenshot tool supports multiple storage backends for different deployment scenarios.

### Configuration

Set `storage_type` in `config.json`:

- `http` - HTTP/HTTPS API endpoints
- `s3` - S3-compatible object storage
- `ftp` - FTP/FTPS servers
- `sftp` - SSH file transfer
- `local` - Local filesystem

### HTTP/HTTPS

```json
{
    "storage_type": "http",
    "http": {
        "server_url": "https://api.example.com/upload",
        "api_key": "your-api-key",
        "max_retries": 3
    }
}
```

**Requirements:** Accepts `multipart/form-data` POST, returns HTTP 200 on success.

### S3/MinIO

```json
{
    "storage_type": "s3",
    "s3": {
        "endpoint_url": "http://minio.example.com:9000",
        "access_key": "ACCESS_KEY",
        "secret_key": "SECRET_KEY",
        "bucket": "screenshots",
        "region": "us-east-1",
        "path_prefix": "daily/"
    }
}
```

Compatible with AWS S3, MinIO, and other S3-compatible services.

### FTP/FTPS

```json
{
    "storage_type": "ftp",
    "ftp": {
        "host": "ftp.example.com",
        "port": 21,
        "username": "ftpuser",
        "password": "ftppass",
        "remote_path": "/screenshots/",
        "use_tls": false
    }
}
```

### SFTP

```json
{
    "storage_type": "sftp",
    "sftp": {
        "host": "sftp.example.com",
        "port": 22,
        "username": "user",
        "password": "pass",
        "remote_path": "/home/user/screenshots/"
    }
}
```

**SSH keys:** Use `private_key_path` instead of `password`.

### Local Storage

```json
{
    "storage_type": "local",
    "local": {
        "save_path": "C:\\Screenshots\\"
    }
}
```

### Dependencies

| Backend | Package | Installation |
|---------|---------|--------------|
| HTTP | `requests` | Included |
| S3 | `boto3` | `pip install boto3` |
| FTP | Built-in | None |
| SFTP | `paramiko` | `pip install paramiko` |
| Local | Built-in | None |

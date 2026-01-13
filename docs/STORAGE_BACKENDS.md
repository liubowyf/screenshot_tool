# 存储后端配置指南

## 🎯 概述

screenshot_tool支持多种存储后端，您可以根据实际需求选择最适合的方式：

| 存储类型 | 适用场景 | 复杂度 | 推荐度 |
|---------|----------|--------|--------|
| **HTTP/HTTPS** | API服务器、云函数 | ⭐ | ⭐⭐⭐⭐⭐ |
| **S3/MinIO** | 对象存储、大规模存储 | ⭐⭐ | ⭐⭐⭐⭐⭐ |
| **FTP/FTPS** | 传统文件服务器 | ⭐⭐ | ⭐⭐⭐ |
| **SFTP** | SSH文件传输、安全性要求高 | ⭐⭐⭐ | ⭐⭐⭐⭐ |
| **本地** | 测试、离线场景 | ⭐ | ⭐⭐ |

## 📝 配置方法

### 1. HTTP/HTTPS（默认）

最常用的方式，上传到Web服务器API。

**配置示例**：
```json
{
    "storage_type": "http",
    "interval_seconds": 5,
    "jpeg_quality": 70,
    
    "http": {
        "server_url": "https://your-server.com/upload",
        "api_key": "your-api-key",
        "max_retries": 3,
        "timeout_connect": 5,
        "timeout_read": 10
    }
}
```

**服务器端示例**（Flask）：
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
```

---

### 2. S3/MinIO

适用于AWS S3、阿里云OSS、MinIO等S3兼容的对象存储。

**配置示例**：
```json
{
    "storage_type": "s3",
    "interval_seconds": 5,
    "jpeg_quality": 70,
    
    "s3": {
        "endpoint_url": "http://localhost:9000",
        "access_key": "minioadmin",
        "secret_key": "minioadmin",
        "bucket": "screenshots",
        "region": "us-east-1",
        "path_prefix": "daily/",
        "use_ssl": false
    }
}
```

**参数说明**：
- `endpoint_url`: S3端点URL（MinIO必填，AWS S3可省略）
- `access_key`: 访问密钥ID
- `secret_key`: 秘密访问密钥
- `bucket`: 存储桶名称
- `region`: 区域（默认us-east-1）
- `path_prefix`: 文件路径前缀（可选）
- `use_ssl`: 是否使用SSL（默认true）

**MinIO快速搭建**：
```bash
docker run -p 9000:9000 -p 9001:9001 \
    -e "MINIO_ROOT_USER=minioadmin" \
    -e "MINIO_ROOT_PASSWORD=minioadmin" \
    minio/minio server /data --console-address ":9001"
```

访问 http://localhost:9001 创建bucket "screenshots"

**AWS S3示例**：
```json
{
    "storage_type": "s3",
    "s3": {
        "access_key": "AKIAIOSFODNN7EXAMPLE",
        "secret_key": "wJalrXUtnFEMI/K7MDENG/bPxRfiCYEXAMPLEKEY",
        "bucket": "my-screenshots",
        "region": "ap-southeast-1",
        "use_ssl": true
    }
}
```

---

### 3. FTP/FTPS

适用于传统FTP文件服务器。

**配置示例**：
```json
{
    "storage_type": "ftp",
    "interval_seconds": 5,
    "jpeg_quality": 70,
    
    "ftp": {
        "host": "ftp.example.com",
        "port": 21,
        "username": "ftpuser",
        "password": "ftppassword",
        "remote_path": "/screenshots/",
        "use_tls": false
    }
}
```

**参数说明**：
- `host`: FTP服务器地址
- `port`: 端口（默认21）
- `username`: 用户名
- `password`: 密码
- `remote_path`: 远程保存路径
- `use_tls`: 是否使用FTPS加密（默认false）

**FTP服务器搭建**（Docker）：
```bash
docker run -d -p 21:21 -p 21000-21010:21000-21010 \
    -e FTP_USER=testuser \
    -e FTP_PASS=testpass \
    fauria/vsftpd
```

---

### 4. SFTP

基于SSH的文件传输，安全性更高。

**配置示例**：
```json
{
    "storage_type": "sftp",
    "interval_seconds": 5,
    "jpeg_quality": 70,
    
    "sftp": {
        "host": "sftp.example.com",
        "port": 22,
        "username": "sftpuser",
        "password": "sftppassword",
        "remote_path": "/home/user/screenshots/"
    }
}
```

**使用SSH密钥**：
```json
{
    "sftp": {
        "host": "sftp.example.com",
        "port": 22,
        "username": "sftpuser",
        "private_key_path": "C:\\\\Users\\\\You\\\\.ssh\\\\id_rsa",
        "password": "",
        "remote_path": "/screenshots/"
    }
}
```

---

### 5. 本地文件系统

保存到本地文件夹，适用于测试或离线场景。

**配置示例**：
```json
{
    "storage_type": "local",
    "interval_seconds": 5,
    "jpeg_quality": 70,
    
    "local": {
        "save_path": "C:\\\\Screenshots\\\\"
    }
}
```

**Windows路径注意**：使用双反斜杠 `\\\\` 或正斜杠 `/`

---

## 🔄 切换存储后端

只需修改`config.json`中的`storage_type`字段，无需修改代码：

```bash
# 使用S3
cp config.s3.example.json config.json

# 使用FTP
cp config.ftp.example.json config.json

# 使用本地
cp config.local.example.json config.json
```

## 📦 依赖安装

不同存储后端需要不同的Python库：

| 存储类型 | 需要安装 |
|---------|---------|
| HTTP | ✅ 默认包含（requests） |
| S3 | `pip install boto3` |
| FTP | ✅ Python标准库 |
| SFTP | `pip install paramiko` |
| Local | ✅ Python标准库 |

**安装所有依赖**：
```bash
pip install -r requirements.txt
```

## ⚠️ 向后兼容

旧版配置文件会自动兼容：

**旧配置**（仍然有效）：
```json
{
    "server_url": "https://example.com/upload",
    "api_key": "xxx",
    "interval_seconds": 5
}
```

程序会自动检测并使用HTTP后端。

**新配置**（推荐）：
```json
{
    "storage_type": "http",
    "http": {
        "server_url": "https://example.com/upload",
        "api_key": "xxx"
    }
}
```

## 🔍 故障排查

### S3连接失败

1. 检查endpoint_url是否正确
2. 确认access_key和secret_key
3. 确保bucket已创建
4. 检查网络连接

### FTP上传失败

1. 确认防火墙允许21端口
2. 检查被动模式端口范围
3. 验证远程路径是否存在

### SFTP认证失败

1. 检查SSH密钥格式（RSA/Ed25519）
2. 确认密钥文件路径正确
3. 验证用户权限

查看日志文件 `logs/screenshot_YYYYMMDD.log` 获取详细错误信息。

---

**更多示例**：查看 `config.*.example.json` 文件

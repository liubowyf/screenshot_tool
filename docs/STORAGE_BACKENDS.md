# Storage Backend Configuration

## Overview

The screenshot tool supports multiple storage backends for flexibility in different deployment scenarios.

## Configuration

Set the `storage_type` field in `config.json` to choose your backend:

- `http` - HTTP/HTTPS API endpoints
- `s3` - S3-compatible object storage
- `ftp` - FTP/FTPS servers
- `sftp` - SSH file transfer
- `local` - Local filesystem

## HTTP/HTTPS

Standard web API uploads.

```json
{
    "storage_type": "http",
    "http": {
        "server_url": "https://api.example.com/upload",
        "api_key": "your-api-key",
        "max_retries": 3,
        "timeout_connect": 5,
        "timeout_read": 10
    }
}
```

**Server Requirements:**
- Accept `multipart/form-data` POST requests
- Optional API key authentication via `X-API-Key` header
- Return HTTP 200 on success

## S3/MinIO

Compatible with AWS S3, MinIO, and other S3-compatible services.

```json
{
    "storage_type": "s3",
    "s3": {
        "endpoint_url": "http://minio.example.com:9000",
        "access_key": "ACCESS_KEY",
        "secret_key": "SECRET_KEY",
        "bucket": "screenshots",
        "region": "us-east-1",
        "path_prefix": "daily/",
        "use_ssl": false
    }
}
```

**Parameters:**
- `endpoint_url` - S3 endpoint (required for MinIO, optional for AWS)
- `access_key` - AWS access key ID
- `secret_key` - AWS secret access key
- `bucket` - Target bucket name
- `region` - AWS region (default: us-east-1)
- `path_prefix` - Optional path prefix for uploaded files
- `use_ssl` - Use HTTPS (default: true)

**MinIO Setup:**
```bash
docker run -p 9000:9000 -p 9001:9001 \
    -e "MINIO_ROOT_USER=admin" \
    -e "MINIO_ROOT_PASSWORD=password" \
    minio/minio server /data --console-address ":9001"
```

## FTP/FTPS

Traditional FTP file servers.

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

**Parameters:**
- `host` - FTP server hostname
- `port` - Port number (default: 21)
- `username` - FTP username
- `password` - FTP password
- `remote_path` - Remote directory path
- `use_tls` - Enable FTPS encryption (default: false)

## SFTP

Secure file transfer over SSH.

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

**Using SSH keys:**
```json
{
    "sftp": {
        "host": "sftp.example.com",
        "username": "user",
        "private_key_path": "C:\\Users\\You\\.ssh\\id_rsa",
        "remote_path": "/screenshots/"
    }
}
```

## Local Filesystem

Save directly to local disk. Useful for testing.

```json
{
    "storage_type": "local",
    "local": {
        "save_path": "C:\\Screenshots\\"
    }
}
```

## Dependencies

Different backends require different Python packages:

| Backend | Required Package | Installation |
|---------|-----------------|--------------|
| HTTP | `requests` | Included |
| S3 | `boto3` | `pip install boto3` |
| FTP | Built-in | None |
| SFTP | `paramiko` | `pip install paramiko` |
| Local | Built-in | None |

Install all optional dependencies:
```bash
pip install -r requirements.txt
```

## Switching Backends

To switch between backends, simply update the `storage_type` field in `config.json` and restart the application. No code changes required.

## Troubleshooting

Check `logs/screenshot_YYYYMMDD.log` for detailed error messages.

**S3 Connection Issues:**
- Verify endpoint URL and credentials
- Ensure bucket exists and is accessible
- Check network connectivity

**FTP Upload Failures:**
- Confirm firewall allows port 21 (or configured port)
- Verify remote path exists or script has permission to create it
- Check passive mode compatibility

**SFTP Authentication:**
- Ensure SSH key format is correct (RSA recommended)
- Verify key file permissions
- Check username and host are correct

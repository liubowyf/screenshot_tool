# 项目结构说明

## 📁 文件结构

```
screenshot_tool/
├── .github/
│   └── workflows/
│       └── build-windows.yml    # GitHub Actions自动构建
│
├── docs/                        # 文档目录
│   ├── DEPLOYMENT.md            # 部署指南
│   ├── TECHNICAL.md             # 技术实现详解
│   ├── BUILD_ON_MACOS.md        # macOS构建指南
│   ├── ANTIVIRUS.md             # 杀毒软件误报解决
│   ├── PACKAGING_COMPARISON.md  # 打包方案对比
│   ├── CROSS_PLATFORM.md        # 跨平台构建说明
│   └── GITHUB_ACTIONS.md        # GitHub Actions使用教程
│
├── screenshot_tool.py           # 主程序（核心代码）
├── config.json                  # 配置文件模板
├── requirements.txt             # Python依赖
├── version_info.txt             # Windows exe元数据
│
├── build.bat                    # Windows打包脚本
├── build.sh                     # macOS/Linux打包脚本
├── build_nuitka.bat             # Windows Nuitka编译脚本
├── build_nuitka.sh              # macOS/Linux Nuitka编译脚本
├── build_windows_on_mac.sh      # macOS上构建Windows exe（Docker）
│
├── .gitignore                   # Git忽略规则
├── LICENSE                      # MIT开源协议
└── README.md                    # 项目说明（中英双语）
```

## 🗂️ 文件说明

### 核心文件

- **screenshot_tool.py**: 主程序，包含所有核心功能
  - 截图模块（mss）
  - 网络上传模块（requests）
  - 配置管理
  - 日志系统
  - 无感运行控制

- **config.json**: 配置文件，用户需要修改
  - 服务器URL
  - API密钥
  - 截图间隔
  - 图片质量等

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

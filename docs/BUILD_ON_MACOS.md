# 在 macOS 上构建 Windows exe - 完整指南

## 🎯 三种方案对比

| 方案 | 难度 | 速度 | 可靠性 | 推荐度 |
|------|------|------|--------|--------|
| **1. GitHub Actions** | ⭐ | 快 | ⭐⭐⭐⭐⭐ | ⭐⭐⭐⭐⭐ **最推荐** |
| **2. Docker + Wine** | ⭐⭐⭐ | 中 | ⭐⭐⭐ | ⭐⭐⭐⭐ 本地构建 |
| **3. 虚拟机** | ⭐⭐⭐⭐ | 慢 | ⭐⭐⭐⭐⭐ | ⭐⭐⭐ 完全控制 |

---

## 🚀 方案1: GitHub Actions（云端构建，最推荐）

### 优点
- ✅ **完全免费**（公开仓库）
- ✅ **零配置**（无需本地Windows环境）
- ✅ **自动化**（推送即构建）
- ✅ **高可靠**（真实Windows环境）

### 快速开始

```bash
# 1. 推送代码到GitHub
cd /Users/liubo/Downloads/截图脚本
git init
git add .
git commit -m "Add screenshot tool"

# 2. 创建GitHub仓库（在网页上操作）
# 访问: https://github.com/new

# 3. 推送
git remote add origin https://github.com/YOUR_USERNAME/screenshot-tool.git
git push -u origin main

# 4. 等待构建完成（2-5分钟）
# 5. 下载 artifact: ScreenCapture-Windows-exe.zip
```

**详细教程**: 查看 [GITHUB_ACTIONS.md](file:///Users/liubo/Downloads/截图脚本/GITHUB_ACTIONS.md)

---

## 🐳 方案2: Docker + Wine（本地构建）

### 原理

使用Docker运行包含Wine的Linux容器，Wine模拟Windows环境运行PyInstaller。

```
macOS
  └─ Docker 容器（Linux）
       └─ Wine（Windows模拟器）
            └─ Python + PyInstaller
                 └─ 生成 .exe
```

### 前提条件

1. **安装 Docker Desktop**:
   ```bash
   brew install --cask docker
   ```
   或访问: https://www.docker.com/products/docker-desktop

2. **启动 Docker Desktop** 应用

### 使用步骤

```bash
cd /Users/liubo/Downloads/截图脚本

# 运行Docker构建脚本
./build_windows_on_mac.sh

# 首次运行会下载Docker镜像（约500MB），需要10-15分钟
# 后续运行只需2-5分钟

# 完成后，exe在 dist/ 目录
ls -lh dist/ScreenCapture.exe
```

### 优缺点

**优点**:
- ✅ 完全在macOS本地完成
- ✅ 无需GitHub账号
- ✅ 离线可用（镜像下载后）
- ✅ 重复构建快

**缺点**:
- ⚠️ 首次下载镜像慢（500MB+）
- ⚠️ exe体积较大（15-20MB vs 2-4MB）
- ⚠️ Wine兼容性问题可能导致构建失败
- ⚠️ 需要占用磁盘空间

### 故障排查

**问题1: Docker镜像下载慢**
```bash
# 使用国内镜像加速（可选）
# 打开 Docker Desktop → Settings → Docker Engine
# 添加:
{
  "registry-mirrors": [
    "https://mirror.ccs.tencentyun.com"
  ]
}
```

**问题2: Wine运行失败**
```bash
# 查看详细日志
docker run --rm -v "$(pwd):/app" -w /app screenshot-builder:windows \
    bash -c "wine python --version"
```

**问题3: exe不能运行**
- Wine生成的exe可能不够稳定
- 建议使用GitHub Actions或真实Windows环境

---

## 💻 方案3: Windows虚拟机（完全控制）

### 适用场景
- 需要频繁调试Windows特定问题
- 需要测试Windows环境兼容性
- 对构建有严格要求

### 选项A: Parallels Desktop（推荐，M1+兼容）

```bash
# 1. 购买 Parallels Desktop (约¥600/年)
# 访问: https://www.parallels.com/

# 2. 安装Windows 11 ARM（M1/M2/M3 Mac）
#    或Windows 10/11 x64（Intel Mac）

# 3. 在虚拟机中运行 build.bat
```

### 选项B: VirtualBox（免费，仅Intel Mac）

```bash
# 1. 安装 VirtualBox
brew install --cask virtualbox

# 2. 下载Windows 10 ISO
# 访问: https://www.microsoft.com/software-download/windows10

# 3. 创建虚拟机并安装Windows

# 4. 共享文件夹，在虚拟机中打包
```

---

## 📊 方案选择指南

### 场景1: 偶尔打包（每周1-2次）

**推荐**: GitHub Actions

```bash
git push  # 自动触发构建
# 等待5分钟，下载exe
```

**理由**:
- 无需本地环境
- 完全免费
- 最省事

---

### 场景2: 频繁开发调试（每天多次）

**推荐**: Docker + Wine

```bash
./build_windows_on_mac.sh  # 本地2分钟完成
```

**理由**:
- 本地快速迭代
- 无需推送到GitHub
- 离线可用

**备用**: 如果Docker方案不稳定，使用虚拟机

---

### 场景3: 生产部署（严格要求）

**推荐**: GitHub Actions + 代码签名

```bash
# 1. GitHub Actions 构建
# 2. 自动签名（配置证书）
# 3. 自动发布 Release
```

**理由**:
- 可追溯
- 可自动化签名
- 可CI/CD集成

---

## 🛠️ 立即开始

### 快速方案（GitHub Actions）

1. 已创建工作流文件: `.github/workflows/build-windows.yml` ✅
2. 运行以下命令:

```bash
cd /Users/liubo/Downloads/截图脚本

# 推送到GitHub（首次需要创建仓库）
git init
git add .
git commit -m "Windows screenshot tool with GitHub Actions"

# 创建仓库: https://github.com/new
# 然后执行:
git remote add origin <您的仓库URL>
git push -u origin main

# 访问 GitHub → Actions 查看构建
# 完成后下载 artifact
```

### 本地方案（Docker）

1. 已创建构建脚本: `build_windows_on_mac.sh` ✅
2. 运行以下命令:

```bash
cd /Users/liubo/Downloads/截图脚本

# 确保Docker Desktop已启动
open -a Docker

# 等待Docker启动完成，然后:
./build_windows_on_mac.sh

# 首次运行约10-15分钟（下载镜像）
# 后续只需2-5分钟
```

---

## ⚡ 性能对比

| 方案 | 首次时间 | 后续时间 | 磁盘占用 | 网络需求 |
|------|----------|----------|----------|----------|
| GitHub Actions | 5分钟 | 5分钟 | 0 MB | 上传+下载 |
| Docker + Wine | 15分钟 | 2分钟 | 500 MB | 仅首次 |
| 虚拟机 | 2小时+ | 2分钟 | 20+ GB | 下载ISO |

---

## 🎯 我的建议

**对于您的场景**，建议：

1. **首选**: GitHub Actions
   - 最简单、最可靠
   - 真实Windows环境
   - 误报率最低

2. **备选**: Docker + Wine
   - 如需快速本地迭代
   - 但要注意Wine兼容性

3. **不推荐**: 虚拟机
   - 除非需要频繁测试Windows特定功能

---

## 📞 需要帮助？

**GitHub Actions遇到问题**:
查看 [GITHUB_ACTIONS.md](file:///Users/liubo/Downloads/截图脚本/GITHUB_ACTIONS.md)

**Docker构建失败**:
```bash
# 查看详细日志
docker logs <container_id>

# 清理重建
docker system prune -a
./build_windows_on_mac.sh
```

**其他问题**:
查看 [CROSS_PLATFORM.md](file:///Users/liubo/Downloads/截图脚本/CROSS_PLATFORM.md)

---

**您想先试哪个方案？**
1. GitHub Actions（推荐，我已配置好）
2. Docker本地构建（我已创建脚本）

# 跨平台打包指南

## 🖥️ 核心问题

**PyInstaller的限制**：
- 在 macOS 上打包 → 只能生成 macOS 可执行文件
- 在 Windows 上打包 → 只能生成 Windows exe 文件
- 在 Linux 上打包 → 只能生成 Linux 可执行文件

**结论**：PyInstaller **不支持交叉编译**，必须在目标平台上打包。

---

## 💡 解决方案

### 方案1: 使用 Windows 虚拟机（推荐）

在macOS上安装Windows虚拟机：

#### 选项A: Parallels Desktop（商业软件，性能最好）

1. **下载安装**：
   - 访问 https://www.parallels.com/
   - 购买许可证（约¥600/年）
   - 安装 Windows 10/11 虚拟机

2. **在虚拟机中打包**：
   ```cmd
   REM 在 Windows 虚拟机中
   cd /path/to/截图脚本
   build.bat
   ```

3. **优点**：
   - ✅ 性能好，几乎无延迟
   - ✅ 与macOS文件共享方便
   - ✅ 可以测试Windows环境

#### 选项B: VirtualBox（免费）

1. **安装**：
   ```bash
   brew install --cask virtualbox
   ```

2. **创建Windows虚拟机**：
   - 下载 Windows 10 ISO
   - 创建虚拟机并安装

3. **在虚拟机中打包**

#### 选项C: UTM（免费，Apple Silicon原生）

如果您使用M1/M2/M3 Mac：
```bash
brew install --cask utm
```

---

### 方案2: 使用云服务器（灵活）

租用云服务器打包：

#### 阿里云/腾讯云 Windows 服务器

1. **购买按量付费Windows服务器**：
   - CPU: 1核
   - 内存: 2GB
   - 费用: 约¥1-2/小时

2. **远程连接**：
   ```bash
   # macOS 使用 RDP 客户端
   brew install --cask microsoft-remote-desktop
   ```

3. **上传代码打包**：
   - 通过RDP复制文件
   - 或使用Git克隆代码
   - 运行 `build.bat`

4. **下载exe文件**

5. **关闭服务器**（避免持续计费）

**成本分析**：
```
打包一次约需: 30分钟
费用: ¥1-2
适合: 偶尔打包
```

---

### 方案3: GitHub Actions CI/CD（免费，自动化）

利用GitHub的Windows runner自动打包：

#### 配置步骤

1. **创建GitHub仓库**：
   ```bash
   cd /Users/liubo/Downloads/截图脚本
   git init
   git add .
   git commit -m "Initial commit"
   git remote add origin https://github.com/yourusername/screenshot-tool.git
   git push -u origin main
   ```

2. **创建GitHub Actions工作流**：

创建文件 `.github/workflows/build.yml`：

```yaml
name: Build Windows Exe

on:
  push:
    branches: [ main ]
  workflow_dispatch:  # 手动触发

jobs:
  build:
    runs-on: windows-latest
    
    steps:
    - uses: actions/checkout@v3
    
    - name: Set up Python
      uses: actions/setup-python@v4
      with:
        python-version: '3.10'
    
    - name: Install dependencies
      run: |
        python -m pip install --upgrade pip
        pip install -r requirements.txt
        pip install pyinstaller
    
    - name: Build with PyInstaller
      run: |
        build.bat
    
    - name: Upload artifact
      uses: actions/upload-artifact@v3
      with:
        name: ScreenCapture-Windows
        path: dist/ScreenCapture.exe
```

3. **触发构建**：
   - 推送代码到GitHub
   - 或在Actions页面手动触发
   - 等待构建完成（约2-5分钟）
   - 下载构建好的exe文件

**优点**：
- ✅ 完全免费（每月2000分钟免费额度）
- ✅ 自动化，每次更新自动打包
- ✅ 无需本地Windows环境

---

### 方案4: Docker + Wine（复杂，不推荐）

使用Wine在容器中运行Windows PyInstaller：

**缺点**：
- ❌ 配置复杂
- ❌ 兼容性问题多
- ❌ 打包成功率低

**不推荐此方案**

---

### 方案5: 在 macOS 上测试（仅限测试）

虽然不能生成Windows exe，但可以在macOS上测试代码逻辑：

```bash
# 在macOS上运行（测试功能）
chmod +x build.sh
./build.sh

# 生成macOS可执行文件
./dist/ScreenCapture
```

**用途**：
- ✅ 测试截图功能
- ✅ 测试网络上传
- ✅ 验证逻辑正确性
- ❌ 不能用于Windows部署

---

## 🎯 推荐方案对比

| 方案 | 成本 | 便利性 | 自动化 | 推荐度 |
|------|------|--------|--------|--------|
| **GitHub Actions** | 免费 | ⭐⭐⭐⭐⭐ | ⭐⭐⭐⭐⭐ | ⭐⭐⭐⭐⭐ |
| Parallels Desktop | ¥600/年 | ⭐⭐⭐⭐⭐ | ⭐⭐⭐ | ⭐⭐⭐⭐ |
| 云服务器 | ¥1-2/次 | ⭐⭐⭐⭐ | ⭐⭐ | ⭐⭐⭐⭐ |
| VirtualBox | 免费 | ⭐⭐⭐ | ⭐⭐⭐ | ⭐⭐⭐ |
| macOS测试 | 免费 | ⭐⭐⭐⭐⭐ | N/A | ⭐⭐（仅测试） |

---

## 🚀 快速开始（推荐：GitHub Actions）

### 完整步骤

1. **在macOS上准备代码**：
   ```bash
   cd /Users/liubo/Downloads/截图脚本
   ```

2. **创建GitHub Actions工作流**：

我可以帮您创建完整的CI/CD配置！

3. **推送到GitHub**：
   ```bash
   git init
   git add .
   git commit -m "Add screenshot tool"
   # 在GitHub创建仓库后
   git remote add origin <your-repo-url>
   git push -u origin main
   ```

4. **查看构建**：
   - 访问 GitHub → Actions 页面
   - 等待构建完成
   - 下载 `ScreenCapture-Windows` artifact

5. **获取exe文件**：
   - 解压下载的zip
   - 得到 `ScreenCapture.exe`

---

## 📋 我能帮您做什么

### 选项1: 创建GitHub Actions工作流（推荐）

我可以立即为您创建：
- `.github/workflows/build.yml` - Windows打包
- `.github/workflows/build-all.yml` - 多平台打包（Win/Mac/Linux）
- 自动版本号管理
- 自动发布到Releases

### 选项2: 在macOS上测试

运行以下命令测试功能（不生成Windows exe）：
```bash
cd /Users/liubo/Downloads/截图脚本
./build.sh  # 生成macOS版本测试
```

### 选项3: 云服务器打包指导

我可以提供详细的云服务器打包教程。

---

## ⚠️ 重要提醒

> [!WARNING]
> **截图工具的平台限制**
> 
> 即使在Windows上打包成exe：
> - ✅ exe只能在Windows上运行
> - ❌ 不能在macOS/Linux运行
> 
> 这是操作系统API的限制，因为：
> - 截图使用Windows API
> - 隐藏窗口使用Windows API

---

您希望我帮您：
1. ✅ **创建GitHub Actions工作流**（免费自动化）
2. 在macOS上测试代码
3. 提供云服务器详细教程

请告诉我您的选择！

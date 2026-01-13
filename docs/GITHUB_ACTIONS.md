# GitHub Actions 使用指南

## 🎯 什么是 GitHub Actions？

GitHub Actions 是 GitHub 提供的免费 CI/CD 服务，可以在云端自动化构建、测试和部署。

**核心优势**：
- ✅ **完全免费**（公开仓库无限制，私有仓库每月2000分钟）
- ✅ **自动化**（推送代码即自动打包）
- ✅ **多平台**（Windows/macOS/Linux runner）
- ✅ **无需本地环境**（在GitHub服务器上运行）

---

## 🚀 快速开始

### 步骤1: 创建GitHub仓库

1. **访问GitHub**：https://github.com/new

2. **创建新仓库**：
   - Repository name: `screenshot-tool`（或任意名称）
   - Description: `Windows screenshot automation tool`
   - 选择 Public（公开）或 Private（私有）
   - 不要勾选 "Add a README file"
   - 点击 "Create repository"

### 步骤2: 推送代码到GitHub

在您的macOS终端中运行：

```bash
cd /Users/liubo/Downloads/截图脚本

# 初始化Git仓库（如果还没有）
git init

# 添加所有文件
git add .

# 提交
git commit -m "Initial commit: Screenshot automation tool"

# 关联远程仓库（替换为您的仓库地址）
git remote add origin https://github.com/YOUR_USERNAME/screenshot-tool.git

# 推送到GitHub
git branch -M main
git push -u origin main
```

**注意**：将 `YOUR_USERNAME` 替换为您的GitHub用户名。

### 步骤3: 查看自动构建

1. **访问仓库页面** → 点击 "Actions" 标签

2. **查看工作流运行**：
   - 应该能看到 "Build Windows Executable" 工作流
   - 点击最新的运行记录

3. **等待构建完成**（约2-5分钟）：
   - 绿色 ✅ = 成功
   - 红色 ❌ = 失败（查看日志排错）

### 步骤4: 下载构建好的exe

1. **在Actions页面** → 点击成功的运行记录

2. **滚动到底部** → Artifacts 部分

3. **下载** `ScreenCapture-Windows-exe.zip`

4. **解压缩**：
   ```
   ScreenCapture.exe
   config.json
   ```

5. **完成！**现在您有了Windows可执行文件。

---

## 📝 工作流说明

### 触发条件

工作流会在以下情况自动运行：

1. **推送代码到main分支**：
   ```bash
   git push origin main
   ```

2. **创建Pull Request**（自动测试）

3. **手动触发**：
   - Actions页面 → 选择工作流
   - 点击 "Run workflow"

4. **创建版本标签**（自动发布）：
   ```bash
   git tag v1.0.0
   git push origin v1.0.0
   ```

### 构建流程

```mermaid
graph LR
    A[推送代码] --> B[GitHub Actions触发]
    B --> C[启动Windows虚拟机]
    C --> D[安装Python 3.10]
    D --> E[安装依赖]
    E --> F[运行PyInstaller]
    F --> G[上传exe文件]
    G --> H[完成 - 可下载]
```

---

## 🔧 自定义配置

### 修改Python版本

编辑 `.github/workflows/build-windows.yml`：

```yaml
- name: Set up Python
  uses: actions/setup-python@v5
  with:
    python-version: '3.11'  # 改为其他版本
```

### 添加代码签名

如果您有代码签名证书：

```yaml
- name: Sign executable
  run: |
    signtool sign /f cert.pfx /p ${{ secrets.CERT_PASSWORD }} dist/ScreenCapture.exe
```

**注意**：需要在GitHub仓库设置中添加 `CERT_PASSWORD` secret。

### 修改打包参数

在 `build-windows.yml` 中修改 PyInstaller 参数。

---

## 🎁 版本发布

### 创建Release

当您打标签时，自动创建GitHub Release：

```bash
# 打标签
git tag v1.0.0 -m "Release version 1.0.0"
git push origin v1.0.0

# GitHub Actions 会自动：
# 1. 构建exe
# 2. 创建Release
# 3. 上传exe到Release页面
```

用户可以直接从 Releases 页面下载。

---

## 💰 成本说明

### 免费额度

**公开仓库**：
- ✅ 无限制免费使用
- ✅ 所有功能可用

**私有仓库**：
- ✅ 每月2000分钟免费
- ✅ 额外费用：$0.008/分钟

### 单次构建消耗

- Windows runner: 约2-5分钟
- 每月可构建：400-1000次（私有仓库）

**结论**：对于大多数用途，完全免费够用！

---

## 🔍 故障排查

### Q: 构建失败？

**查看错误日志**：
1. Actions页面 → 点击失败的运行
2. 点击红色的步骤查看详细错误

**常见问题**：
- Python版本不兼容 → 检查 `python-version`
- 依赖安装失败 → 检查 `requirements.txt`
- PyInstaller错误 → 查看详细日志

### Q: 找不到Artifacts？

**可能原因**：
- 构建失败 → 检查运行日志
- 保留期已过 → 默认30天

**解决方法**：
- 重新运行工作流
- 增加 `retention-days`

### Q: 下载的文件不能运行？

**检查**：
- 文件是否完整（约2-4 MB）
- Windows Defender是否拦截
- 是否解压缩

---

## 🌟 高级功能

### 多平台构建

创建 `.github/workflows/build-all.yml`（已准备好，可选）：

```yaml
strategy:
  matrix:
    os: [windows-latest, macos-latest, ubuntu-latest]
```

一次构建Windows/macOS/Linux三个版本。

### 自动测试

在打包前运行测试：

```yaml
- name: Run tests
  run: |
    python -m pytest tests/
```

### 构建通知

集成Slack/Email通知构建结果。

---

## 📚 进一步学习

- [GitHub Actions 文档](https://docs.github.com/en/actions)
- [PyInstaller 文档](https://pyinstaller.org/)
- [工作流语法](https://docs.github.com/en/actions/reference/workflow-syntax-for-github-actions)

---

## ✅ 总结

使用GitHub Actions的优势：

| 对比项 | 本地Windows | 虚拟机 | 云服务器 | GitHub Actions |
|--------|-------------|--------|----------|----------------|
| 成本 | 需要Windows | ¥600/年 | ¥1-2/次 | ✅ **免费** |
| 便利性 | 取决于环境 | ⭐⭐⭐⭐ | ⭐⭐⭐⭐ | ✅ **⭐⭐⭐⭐⭐** |
| 自动化 | ❌ | ⭐⭐⭐ | ⭐⭐ | ✅ **⭐⭐⭐⭐⭐** |
| 多版本 | 手动 | 手动 | 手动 | ✅ **自动** |

**推荐**：GitHub Actions 是最优解！

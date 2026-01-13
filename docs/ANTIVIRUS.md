# 杀毒软件误报 / Antivirus False Positives

[中文](#chinese) | [English](#english)

<a name="chinese"></a>
## 中文

### 误报原因

截图和网络功能可能触发杀毒软件启发式检测。

### 解决方案

**1. 代码签名证书（最有效）**

供应商：DigiCert（约$200-500/年）、Sectigo（约$100-300/年）

```cmd
signtool sign /f cert.pfx /p password /t http://timestamp.digicert.com ScreenCapture.exe
```

预期降低：80-95%误报率

**2. 文件元数据（免费）**

已通过 `version_info.txt` 包含。可按需自定义。

**3. 构建优化（免费）**

当前构建已使用：
- `--noupx` - 不使用UPX压缩
- `--strip` - 移除调试符号
- 版本元数据

**4. 白名单申请（免费）**

- Windows Defender: https://www.microsoft.com/wdsi/filesubmission
- 卡巴斯基: https://opentip.kaspersky.com/

响应时间：1-7天

**5. Nuitka编译器（免费，效果更好）**

```bash
pip install nuitka
nuitka --standalone --onefile --windows-disable-console screenshot_tool.py
```

预期降低：比PyInstaller减少30-50%误报

### 推荐方案

**生产环境：** 代码签名 + 当前优化

**测试使用：** 手动添加白名单

---

<a name="english"></a>
## English

### Why False Positives Occur

Screenshot and network functionality can trigger antivirus heuristics.

### Solutions

**1. Code Signing Certificate (Most Effective)**

Providers: DigiCert (~$200-500/year), Sectigo (~$100-300/year)

```cmd
signtool sign /f cert.pfx /p password /t http://timestamp.digicert.com ScreenCapture.exe
```

Expected reduction: 80-95%

**2. File Metadata (Free)**

Already included via `version_info.txt`. Customize as needed.

**3. Build Optimizations (Free)**

Current build already uses:
- `--noupx` - No UPX compression
- `--strip` - Remove debug symbols
- Version metadata

**4. Whitelist Submission (Free)**

- Windows Defender: https://www.microsoft.com/wdsi/filesubmission
- Kaspersky: https://opentip.kaspersky.com/

Response time: 1-7 days

**5. Nuitka Compiler (Free, Better)**

```bash
pip install nuitka
nuitka --standalone --onefile --windows-disable-console screenshot_tool.py
```

Expected reduction: 30-50% vs PyInstaller

### Recommended

**Production:** Code signing + current optimizations

**Testing:** Manual whitelist addition

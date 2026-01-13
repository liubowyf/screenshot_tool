# Windows 自动截图工具 - 部署指南

## 📋 部署前准备

### 1. 环境要求

**Windows系统**：
- Windows 7 SP1 及以上版本
- .NET Framework 4.5+（通常已预装）

**Python环境**（仅开发/打包时需要）：
- Python 3.8 - 3.11
- pip 包管理器

### 2. 服务器端准备

您需要准备一个能够接收HTTP POST请求的服务器端点。

**推荐方案**：
- Flask/Django（Python）
- Express.js（Node.js）
- Spring Boot（Java）
- 云存储服务（阿里云OSS、腾讯云COS等）

## 🚀 部署步骤

### 方案A：使用预编译exe（推荐）

#### Step 1: 准备文件

将以下文件复制到目标Windows电脑：
```
目标文件夹/
├── ScreenCapture.exe    # 主程序
└── config.json          # 配置文件
```

#### Step 2: 配置服务器信息

编辑 `config.json`：

```json
{
    "server_url": "https://your-domain.com/api/upload",
    "api_key": "your-secret-api-key",
    "interval_seconds": 5,
    "jpeg_quality": 70,
    "max_retries": 3,
    "timeout_connect": 5,
    "timeout_read": 10,
    "log_level": "INFO"
}
```

**参数说明**：
- `server_url`: 完整的上传接口地址（必须包含 http:// 或 https://）
- `api_key`: 认证密钥（如果服务器不需要认证，留空即可）
- `interval_seconds`: 截图间隔时间（秒）
- `jpeg_quality`: JPEG压缩质量，范围1-100，建议50-80

#### Step 3: 启动程序

**手动启动**：
- 双击 `ScreenCapture.exe` 运行
- 程序会自动隐藏到后台，无窗口显示

**开机自启动**（可选）：

方法1：使用任务计划程序
1. 按 `Win + R`，输入 `taskschd.msc`
2. 创建基本任务
3. 触发器：系统启动时
4. 操作：启动程序 → 选择 `ScreenCapture.exe`
5. 设置：允许任务按需运行

方法2：注册表启动项（不推荐，可能被杀毒软件拦截）
```
注册表路径：
HKEY_CURRENT_USER\Software\Microsoft\Windows\CurrentVersion\Run
添加字符串值：
名称：ScreenCapture
数据：C:\path\to\ScreenCapture.exe
```

#### Step 4: 验证运行

1. 打开任务管理器（Ctrl + Shift + Esc）
2. 在"详细信息"选项卡中查找 `ScreenCapture.exe` 进程
3. 检查服务器端是否收到截图

#### Step 5: 查看日志

程序会自动在同目录下创建 `logs/` 文件夹：
```
目标文件夹/
├── ScreenCapture.exe
├── config.json
└── logs/
    └── screenshot_20260112.log  # 按日期命名
```

日志内容示例：
```
2026-01-12 10:15:30 [INFO] Windows 自动截图工具启动
2026-01-12 10:15:30 [INFO] 服务器地址: https://example.com/upload
2026-01-12 10:15:30 [INFO] 截图间隔: 5 秒
2026-01-12 10:15:35 [INFO] 截图成功: DESKTOP-ABC123-20260112101535.jpg (124.5 KB)
2026-01-12 10:15:36 [INFO] 上传成功: DESKTOP-ABC123-20260112101535.jpg
```

---

### 方案B：从源码打包

适用于需要自定义功能或修改代码的场景。

#### Step 1: 克隆/下载代码

```bash
# 下载项目文件到本地
cd /path/to/project
```

#### Step 2: 安装依赖

```bash
pip install -r requirements.txt
pip install pyinstaller
```

#### Step 3: 测试运行

```bash
# 先配置 config.json
# 然后运行测试
python screenshot_tool.py
```

按 `Ctrl + C` 停止程序。

#### Step 4: 打包为exe

**Windows系统**：
```bash
build.bat
```

**Linux/Mac（交叉编译）**：
```bash
pyinstaller --onefile \
            --noconsole \
            --strip \
            --exclude-module matplotlib \
            --exclude-module numpy \
            --exclude-module pandas \
            --exclude-module tkinter \
            --name ScreenCapture \
            screenshot_tool.py
```

打包完成后，exe文件位于 `dist/ScreenCapture.exe`

#### Step 5: 分发部署

将 `dist/` 目录下的文件复制到目标电脑，参考方案A的步骤3-5。

---

## 🛠️ 服务器端配置示例

### Python Flask

```python
from flask import Flask, request, jsonify
import os
from datetime import datetime

app = Flask(__name__)
UPLOAD_FOLDER = 'screenshots'
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

@app.route('/api/upload', methods=['POST'])
def upload():
    # API Key验证
    api_key = request.headers.get('X-API-Key')
    if api_key != 'your-secret-api-key':
        return jsonify({'error': 'Unauthorized'}), 401
    
    # 接收文件
    if 'file' not in request.files:
        return jsonify({'error': 'No file'}), 400
    
    file = request.files['file']
    filepath = os.path.join(UPLOAD_FOLDER, file.filename)
    file.save(filepath)
    
    return jsonify({'status': 'success'}), 200

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, ssl_context='adhoc')
```

运行：
```bash
pip install flask pyopenssl
python server.py
```

### Node.js Express

```javascript
const express = require('express');
const multer = require('multer');
const path = require('path');

const app = express();
const upload = multer({ dest: 'screenshots/' });

app.post('/api/upload', upload.single('file'), (req, res) => {
    const apiKey = req.headers['x-api-key'];
    if (apiKey !== 'your-secret-api-key') {
        return res.status(401).json({ error: 'Unauthorized' });
    }
    
    res.json({ status: 'success' });
});

app.listen(5000, () => {
    console.log('Server running on port 5000');
});
```

运行：
```bash
npm install express multer
node server.js
```

---

## 🔧 故障排除

### 问题1: 程序启动后立即退出

**可能原因**：
- 缺少依赖库（源码运行时）
- 配置文件格式错误

**解决方法**：
1. 检查 `config.json` 是否是有效的JSON格式
2. 查看 `logs/` 目录下的日志文件
3. 在命令行中运行exe，查看错误信息：
   ```cmd
   ScreenCapture.exe
   ```

### 问题2: 截图成功但上传失败

**可能原因**：
- 服务器地址错误
- 网络连接问题
- 服务器端拒绝请求

**解决方法**：
1. 检查 `server_url` 是否正确（包括 http:// 或 https://）
2. 在浏览器中访问服务器地址，确认可达
3. 查看日志文件中的错误信息：
   ```
   上传失败 (尝试 1/3): HTTP 403 - Forbidden
   ```
4. 确认 `api_key` 是否正确

### 问题3: 杀毒软件报警

**可能原因**：
- 截图和网络功能被误判为恶意行为

**解决方法**：
1. 将程序添加到杀毒软件白名单
2. 使用代码签名证书签名exe（需购买证书）
3. 提交误报给杀毒软件厂商

### 问题4: 内存占用过高

**可能原因**：
- JPEG质量设置过高
- 截图频率过高

**解决方法**：
在 `config.json` 中调整参数：
```json
{
    "jpeg_quality": 50,        // 降低质量
    "interval_seconds": 10     // 增加间隔
}
```

### 问题5: 无法隐藏控制台窗口

**可能原因**：
- 使用了未经 `--noconsole` 打包的exe

**解决方法**：
重新打包时确保使用 `--noconsole` 参数：
```bash
pyinstaller --noconsole --onefile screenshot_tool.py
```

---

## 📊 性能优化建议

### 1. 网络传输优化

**降低带宽占用**：
```json
{
    "jpeg_quality": 50,        // 降低质量（文件更小）
    "interval_seconds": 10     // 降低频率
}
```

**预期效果**：
- 质量70 → 50：文件大小减少约30-40%
- 间隔5秒 → 10秒：带宽占用减半

### 2. 磁盘空间优化

如果服务器存储空间有限，建议：
- 定期清理旧截图
- 使用云存储服务的生命周期策略自动删除
- 服务器端再次压缩

### 3. 多显示器支持

当前版本仅截取主显示器。如需截取所有显示器，修改代码：

```python
# 原代码（仅主显示器）
monitor = self.sct.monitors[1]

# 修改为（所有显示器）
monitor = self.sct.monitors[0]  # 0 表示所有显示器的组合
```

---

## 🔒 安全建议

### 1. 使用HTTPS

务必使用HTTPS协议上传：
```json
{
    "server_url": "https://your-domain.com/upload"  // 注意是 https
}
```

### 2. API Key管理

- 不要在代码中硬编码API Key
- 定期更换API Key
- 使用强随机字符串作为API Key

生成强API Key（Linux/Mac）：
```bash
openssl rand -hex 32
```

生成强API Key（Windows PowerShell）：
```powershell
-join ((48..57) + (65..90) + (97..122) | Get-Random -Count 32 | % {[char]$_})
```

### 3. 传输加密（可选）

如需额外安全性，可在上传前加密图片：
- AES加密
- 服务器端解密后保存

---

## 📞 技术支持

如遇到问题，请提供以下信息：
1. Windows版本
2. 错误日志（`logs/` 目录下的文件）
3. `config.json` 内容（隐藏敏感信息）
4. 具体错误现象描述

---

**部署完成后，记得测试验证功能是否正常！**

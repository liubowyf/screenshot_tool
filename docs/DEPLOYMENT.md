# Deployment Guide / 部署指南

[English](#english) | [中文](#chinese)

<a name="english"></a>
## English

### Prerequisites

- Windows 7 SP1 or later
- Network connectivity

### Installation

1. Download from [Releases](https://github.com/liubowyf/screenshot_tool/releases)
2. Extract to target directory
3. Edit `config.json`
4. Run `ScreenCapture.exe`

### Configuration

```json
{
    "storage_type": "http",
    "interval_seconds": 5,
    "jpeg_quality": 70,
    "http": {
        "server_url": "https://your-server.com/upload",
        "api_key": "your-api-key"
    }
}
```

### Auto-Start

**Task Scheduler (Recommended):**
1. Open Task Scheduler (`Win + R` → `taskschd.msc`)
2. Create Basic Task → At system startup
3. Action: Start `ScreenCapture.exe`
4. Enable "Run whether user is logged on or not"

### Server Example

```python
from flask import Flask, request

app = Flask(__name__)

@app.route('/upload', methods=['POST'])
def upload():
    if request.headers.get('X-API-Key') != 'your-api-key':
        return {'error': 'Unauthorized'}, 401
    file = request.files['file']
    file.save(f'uploads/{file.filename}')
    return {'status': 'success'}, 200

app.run(host='0.0.0.0', port=5000)
```

### Troubleshooting

**Program exits:** Check `config.json` syntax and `logs/`

**Upload fails:** Verify server URL and API key

**Antivirus alerts:** Add to whitelist or use code signing

### Building

```bash
pip install -r requirements.txt pyinstaller
build.bat  # Windows
./build.sh  # Linux/macOS
```

---

<a name="chinese"></a>
## 中文

### 系统要求

- Windows 7 SP1 或更高版本
- 网络连接

### 安装步骤

1. 从[Releases](https://github.com/liubowyf/screenshot_tool/releases)下载
2. 解压到目标目录
3. 编辑`config.json`
4. 运行`ScreenCapture.exe`

### 配置文件

```json
{
    "storage_type": "http",
    "interval_seconds": 5,
    "jpeg_quality": 70,
    "http": {
        "server_url": "https://your-server.com/upload",
        "api_key": "your-api-key"
    }
}
```

### 开机自启动

**任务计划程序（推荐）：**
1. 打开任务计划程序（`Win + R` → `taskschd.msc`）
2. 创建基本任务 → 系统启动时
3. 操作：启动`ScreenCapture.exe`
4. 勾选"不管用户是否登录都要运行"

### 服务器示例

```python
from flask import Flask, request

app = Flask(__name__)

@app.route('/upload', methods=['POST'])
def upload():
    if request.headers.get('X-API-Key') != 'your-api-key':
        return {'error': 'Unauthorized'}, 401
    file = request.files['file']
    file.save(f'uploads/{file.filename}')
    return {'status': 'success'}, 200

app.run(host='0.0.0.0', port=5000)
```

### 故障排查

**程序退出：** 检查`config.json`语法和`logs/`日志

**上传失败：** 验证服务器URL和API密钥

**杀毒报警：** 添加到白名单或使用代码签名

### 从源码构建

```bash
pip install -r requirements.txt pyinstaller
build.bat  # Windows
./build.sh  # Linux/macOS
```

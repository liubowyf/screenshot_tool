# Deployment Guide

## Prerequisites

- Windows 7 SP1 or later
- Network connectivity to upload server

## Installation

1. Download release from [Releases](https://github.com/liubowyf/screenshot_tool/releases)
2. Extract files to target directory
3. Edit `config.json` with your settings
4. Run `ScreenCapture.exe`

## Configuration

Edit `config.json`:

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

See [STORAGE_BACKENDS.md](STORAGE_BACKENDS.md) for other storage options.

## Auto-Start on Boot

### Method 1: Task Scheduler (Recommended)

1. Open Task Scheduler (`Win + R` → `taskschd.msc`)
2. Create Basic Task
3. Trigger: At system startup
4. Action: Start program → select `ScreenCapture.exe`
5. Check "Run whether user is logged on or not"

### Method 2: Startup Folder

Create shortcut in:
```
C:\Users\<Username>\AppData\Roaming\Microsoft\Windows\Start Menu\Programs\Startup
```

## Verification

1. Open Task Manager (`Ctrl + Shift + Esc`)
2. Find `ScreenCapture.exe` in Details tab
3. Check server logs for incoming uploads
4. Review `logs/screenshot_YYYYMMDD.log`

## Server Setup

### Flask Example

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

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, ssl_context='adhoc')
```

### Node.js Example

```javascript
const express = require('express');
const multer = require('multer');

const app = express();
const upload = multer({ dest: 'uploads/' });

app.post('/upload', upload.single('file'), (req, res) => {
    if (req.headers['x-api-key'] !== 'your-api-key') {
        return res.status(401).json({ error: 'Unauthorized' });
    }
    res.json({ status: 'success' });
});

app.listen(5000);
```

## Troubleshooting

### Program Exits Immediately

- Check `config.json` syntax
- Review `logs/screenshot_YYYYMMDD.log`
- Run from command line to see error messages

### Upload Failures

- Verify `server_url` is correct
- Check network connectivity
- Confirm API key matches server configuration
- Review server logs

### Antivirus Alerts

- Add exe to antivirus whitelist
- Use code signing certificate (reduces false positives)
- Submit false positive report to AV vendor

### High Memory Usage

Reduce in `config.json`:
```json
{
    "jpeg_quality": 50,
    "interval_seconds": 10
}
```

## Security

- Always use HTTPS for uploads
- Use strong random API keys
- Rotate API keys regularly
- Monitor server logs for unauthorized access

## Building from Source

```bash
pip install -r requirements.txt
pip install pyinstaller
```

Windows:
```cmd
build.bat
```

Linux/macOS:
```bash
chmod +x build.sh
./build.sh
```

Output exe will be in `dist/` directory.

# Screenshot Tool

```
screenshot_tool/
├── README.md              # Project overview and quick start
├── LICENSE                # Apache 2.0 license
├── CHANGELOG.md           # Version history
├── CONTRIBUTING.md        # Contribution guidelines
├── requirements.txt       # Python dependencies
├── .gitignore            # Git ignore rules
│
├── screenshot_tool.py     # Main application
├── storage_backends.py    # Storage backend implementations
├── version_info.txt       # Executable metadata
│
├── scripts/              # Build and utility scripts
│   ├── build.bat         # Windows build script
│   ├── build.sh          # Linux/macOS build script
│   ├── build_nuitka.bat  # Nuitka compiler (Windows)
│   ├── build_nuitka.sh   # Nuitka compiler (Linux/macOS)
│   └── build_windows_on_mac.sh  # Cross-platform build
│
├── examples/             # Configuration examples
│   ├── config.http.example.json
│   ├── config.s3.example.json
│   ├── config.ftp.example.json
│   └── config.local.example.json
│
├── docs/                 # Documentation
│   ├── DEPLOYMENT.md     # Installation and deployment
│   ├── STORAGE_BACKENDS.md  # Storage configuration
│   ├── TECHNICAL.md      # Technical details
│   └── ANTIVIRUS.md      # False positive handling
│
└── .github/
    └── workflows/
        └── build-windows.yml  # CI/CD automation
```

## Directory Structure

### Root Level

**Core Files:**
- `screenshot_tool.py` - Main application entry point
- `storage_backends.py` - Storage backend module
- `config.json` - User configuration (not in repo)

**Documentation:**
- `README.md` - Project overview, quick start, and FAQ
- `CHANGELOG.md` - Version history and release notes
- `CONTRIBUTING.md` - Guidelines for contributors
- `LICENSE` - Apache 2.0 license text

**Configuration:**
- `requirements.txt` - Python package dependencies
- `version_info.txt` - Windows executable metadata
- `.gitignore` - Files to exclude from version control

### scripts/

Build and compilation scripts for different platforms and methods.

**Files:**
- `build.bat` - Standard Windows build (PyInstaller)
- `build.sh` - Linux/macOS build (PyInstaller)
- `build_nuitka.bat` - Windows build with Nuitka (lower false positives)
- `build_nuitka.sh` - Linux/macOS build with Nuitka
- `build_windows_on_mac.sh` - Cross-platform Windows build using Docker

**Usage:**
```bash
cd scripts
./build.sh            # Build on current platform
./build_nuitka.sh     # Build with Nuitka
```

### examples/

Sample configuration files for different storage backends.

**Files:**
- `config.http.example.json` - HTTP/HTTPS upload example
- `config.s3.example.json` - S3/MinIO example
- `config.ftp.example.json` - FTP/FTPS example
- `config.local.example.json` - Local storage example

**Usage:**
```bash
cp examples/config.http.example.json config.json
# Edit config.json with your settings
```

### docs/

Comprehensive documentation for users and developers.

**Files:**
- `DEPLOYMENT.md` - Installation, configuration, and auto-start
- `STORAGE_BACKENDS.md` - Detailed storage backend configuration
- `TECHNICAL.md` - Technical implementation details
- `ANTIVIRUS.md` - Handling antivirus false positives

### .github/

GitHub-specific configuration.

**workflows/** - GitHub Actions CI/CD pipelines
- `build-windows.yml` - Automatic Windows executable builds

## Quick Reference

### For Users

1. Download release or clone repository
2. Copy example config: `cp examples/config.http.example.json config.json`
3. Edit `config.json` with your settings
4. Run: `python screenshot_tool.py` or `ScreenCapture.exe`

### For Developers

1. Clone repository
2. Install dependencies: `pip install -r requirements.txt`
3. Run: `python screenshot_tool.py`
4. Build: `cd scripts && ./build.sh`

### For Contributors

1. Read `CONTRIBUTING.md` for guidelines
2. Check `CHANGELOG.md` for version history
3. Review `docs/TECHNICAL.md` for architecture details

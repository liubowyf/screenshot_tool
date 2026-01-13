# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [Unreleased]

### Planned
- Multi-monitor support
- Video recording mode
- macOS and Linux support
- GUI configuration tool

## [1.1.0] - 2026-01-13

### Added
- **S3/MinIO storage backend** - Support for AWS S3, MinIO, and S3-compatible object storage
- **FTP/FTPS storage backend** - Support for traditional FTP file servers
- **SFTP storage backend** - Secure file transfer over SSH
- **Local filesystem storage** - Save screenshots to local directory
- **Multi-storage backend architecture** - Flexible storage backend system with factory pattern
- **Configuration examples** - Example configs for all storage types in `examples/` directory
- **Chinese-first documentation** - All documentation reorganized with Chinese content before English
- **Comprehensive storage guide** - Detailed STORAGE_BACKENDS.md documentation

### Changed
- **Project structure optimization** - Build scripts moved to `scripts/`, examples to `examples/`
- **Enhanced README** - GitHub badges, FAQ section, roadmap, performance metrics
- **Improved documentation** - CONTRIBUTING.md, CHANGELOG.md, PROJECT_STRUCTURE.md added
- **Bilingual documentation** - All docs now support Chinese and English

### Fixed
- GitHub Actions workflow paths updated for new directory structure
- .gitignore optimized for better file handling

## [1.0.0] - 2026-01-13

### Added
- Initial release
- Windows screenshot automation
- Multiple storage backends:
  - HTTP/HTTPS upload
  - S3/MinIO object storage
  - FTP/FTPS file transfer
  - SFTP secure file transfer
  - Local filesystem storage
- Memory-only processing (no local file retention)
- Configurable screenshot intervals
- Configurable JPEG quality
- Intelligent retry mechanism with exponential backoff
- Comprehensive logging system
- GitHub Actions CI/CD for automated builds
- Complete bilingual documentation (English/Chinese)

### Security
- HTTPS support for secure uploads
- API key authentication
- Secure credential storage in configuration

### Documentation
- README with quick start guide
- Storage backend configuration guide
- Deployment guide
- Antivirus false positive handling guide
- Technical implementation details
- Contributing guidelines
- Apache 2.0 license

### Build
- PyInstaller packaging for Windows
- Nuitka compilation option for reduced false positives
- Optimized build parameters (--noupx, --strip)
- Version metadata inclusion
- GitHub Actions automated builds

---

## Versioning

This project uses [Semantic Versioning](https://semver.org/):

- **MAJOR** version for incompatible API changes
- **MINOR** version for new functionality (backwards-compatible)
- **PATCH** version for backwards-compatible bug fixes

## Links

- [Releases](https://github.com/liubowyf/screenshot_tool/releases)
- [Issues](https://github.com/liubowyf/screenshot_tool/issues)
- [Pull Requests](https://github.com/liubowyf/screenshot_tool/pulls)

# Contributing to Screenshot Tool

First off, thank you for considering contributing to Screenshot Tool! It's people like you that make this tool better for everyone.

## Table of Contents

- [Code of Conduct](#code-of-conduct)
- [How Can I Contribute?](#how-can-i-contribute)
- [Development Setup](#development-setup)
- [Coding Guidelines](#coding-guidelines)
- [Commit Guidelines](#commit-guidelines)
- [Pull Request Process](#pull-request-process)

## Code of Conduct

This project adheres to a code of conduct. By participating, you are expected to uphold this code. Please report unacceptable behavior to the project maintainers.

## How Can I Contribute?

### Reporting Bugs

Before creating bug reports, please check existing issues to avoid duplicates. When creating a bug report, include:

- **Clear title and description**
- **Steps to reproduce**
- **Expected vs actual behavior**
- **Screenshots** (if applicable)
- **Environment details** (OS version, Python version, etc.)
- **Log files** from `logs/` directory

### Suggesting Enhancements

Enhancement suggestions are tracked as GitHub issues. When creating an enhancement suggestion, include:

- **Clear use case**
- **Expected behavior**
- **Current limitations**
- **Possible implementation** (if you have ideas)

### Pull Requests

1. Fork the repo and create your branch from `main`
2. Add tests for new functionality
3. Ensure the test suite passes
4. Update documentation
5. Issue the pull request

## Development Setup

### Prerequisites

- Python 3.8 or higher
- Git
- (Optional) Virtual environment tool

### Setup Steps

```bash
# Clone your fork
git clone https://github.com/YOUR_USERNAME/screenshot_tool.git
cd screenshot_tool

# Create virtual environment (recommended)
python -m venv venv
source venv/bin/activate  # Linux/macOS
venv\Scripts\activate     # Windows

# Install development dependencies
pip install -r requirements.txt
pip install -r requirements-dev.txt  # If available

# Run the tool
python screenshot_tool.py
```

### Testing

```bash
# Run tests (when available)
pytest

# Manual testing
python screenshot_tool.py
```

## Coding Guidelines

### Python Style

- Follow [PEP 8](https://www.python.org/dev/peps/pep-0008/)
- Use meaningful variable names
- Add docstrings to functions and classes
- Keep functions focused and small

### Code Example

```python
def upload_screenshot(image_data: bytes, filename: str) -> bool:
    """
    Upload screenshot to configured storage backend.
    
    Args:
        image_data: Screenshot image data in bytes
        filename: Desired filename for the screenshot
        
    Returns:
        bool: True if upload successful, False otherwise
    """
    try:
        # Implementation
        return True
    except Exception as e:
        logging.error(f"Upload failed: {e}")
        return False
```

### Documentation

- Update README.md for user-facing changes
- Update relevant docs in `docs/` directory
- Add inline comments for complex logic
- Keep documentation in sync with code

## Commit Guidelines

### Commit Message Format

```
<type>(<scope>): <subject>

<body>

<footer>
```

### Types

- `feat`: New feature
- `fix`: Bug fix
- `docs`: Documentation only
- `style`: Code style changes (formatting, etc.)
- `refactor`: Code refactoring
- `test`: Adding tests
- `chore`: Maintenance tasks

### Examples

```bash
feat(storage): add WebDAV storage backend

Implemented WebDAV storage backend to support additional
storage options for enterprise users.

Closes #123
```

```bash
fix(upload): correct retry logic for network errors

Fixed issue where network errors weren't properly retried
due to incorrect exception handling.

Fixes #456
```

## Pull Request Process

1. **Update Documentation**: Ensure README and relevant docs are updated
2. **Add Tests**: Add tests for new functionality
3. **Follow Style Guide**: Ensure code follows project conventions
4. **Update Changelog**: Add entry to CHANGELOG.md
5. **One Feature Per PR**: Keep pull requests focused
6. **Descriptive Title**: Use clear, descriptive title
7. **Link Issues**: Reference related issues in description

### PR Template

```markdown
## Description
Brief description of changes

## Type of Change
- [ ] Bug fix
- [ ] New feature
- [ ] Documentation update
- [ ] Code refactoring

## Testing
How was this tested?

## Checklist
- [ ] Code follows project style guidelines
- [ ] Documentation updated
- [ ] Tests added/updated
- [ ] CHANGELOG.md updated
```

## Development Workflow

```bash
# Create feature branch
git checkout -b feature/amazing-feature

# Make changes
# ... edit files ...

# Test changes
python screenshot_tool.py

# Commit changes
git add .
git commit -m "feat: add amazing feature"

# Push to your fork
git push origin feature/amazing-feature

# Create pull request on GitHub
```

## Areas for Contribution

### High Priority

- Multi-monitor support
- macOS/Linux compatibility
- GUI configuration tool
- Unit tests
- Integration tests

### Medium Priority

- Video recording mode
- Cloud service integrations
- Hotkey configuration
- Performance optimizations

### Documentation

- Tutorial videos
- More usage examples
- Translation to other languages
- Architecture diagrams

## Questions?

Feel free to open a GitHub issue with the `question` label, or reach out to the maintainers.

## License

By contributing, you agree that your contributions will be licensed under the Apache License 2.0.

---

Thank you for contributing! 🎉

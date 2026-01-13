#!/bin/bash
# macOS/Linux 打包脚本
# 注意：在 macOS 上打包只能生成 macOS 可执行文件
# 要生成 Windows exe，需要在 Windows 系统上运行

echo "========================================"
echo "Screenshot Tool - macOS Build Script"
echo "========================================"
echo ""

# 检查 Python
if ! command -v python3 &> /dev/null; then
    echo "[错误] Python3 未安装"
    echo "请运行: brew install python3"
    exit 1
fi

echo "Python 版本:"
python3 --version

# 检查 PyInstaller
if ! python3 -m pip show pyinstaller &> /dev/null; then
    echo "[提示] PyInstaller 未安装，正在安装..."
    python3 -m pip install pyinstaller
    if [ $? -ne 0 ]; then
        echo "[错误] PyInstaller 安装失败"
        exit 1
    fi
fi

echo ""
echo "⚠️  重要提示："
echo "此脚本会在 macOS 上打包，生成的是 macOS 可执行程序"
echo "如需生成 Windows exe 文件，请："
echo "  1. 使用 Windows 虚拟机"
echo "  2. 使用云服务器 Windows 环境"
echo "  3. 使用 GitHub Actions CI/CD"
echo ""
read -p "按 Enter 继续打包 macOS 版本，或 Ctrl+C 退出..."

echo "[1/3] 清理旧的构建文件..."
rm -rf build dist *.spec

echo "[2/3] 开始打包（macOS 版本）..."
python3 -m PyInstaller --onefile \
            --noconsole \
            --strip \
            --noupx \
            --exclude-module matplotlib \
            --exclude-module numpy \
            --exclude-module pandas \
            --exclude-module tkinter \
            --exclude-module unittest \
            --exclude-module test \
            --exclude-module scipy \
            --exclude-module PyQt5 \
            --exclude-module PyQt6 \
            --exclude-module PySide2 \
            --exclude-module PySide6 \
            --exclude-module IPython \
            --exclude-module jupyter \
            --name ScreenCapture \
            screenshot_tool.py

if [ $? -ne 0 ]; then
    echo "[错误] 打包失败"
    exit 1
fi

echo "[3/3] 复制配置文件..."
cp config.json dist/config.json

echo ""
echo "========================================"
echo "打包完成！"
echo "输出目录: dist/"
echo "主程序: dist/ScreenCapture"
echo "配置文件: dist/config.json"
echo "========================================"
echo ""
echo "⚠️  注意："
echo "生成的是 macOS 可执行程序，只能在 macOS 上运行"
echo "要在 Windows 上使用，需要在 Windows 系统上打包"
echo ""
echo "运行方式:"
echo "  chmod +x dist/ScreenCapture"
echo "  ./dist/ScreenCapture"
echo ""

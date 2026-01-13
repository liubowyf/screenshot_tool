#!/bin/bash
# 使用 Nuitka 编译（macOS/Linux）
# 注意：在 macOS 上编译只能生成 macOS 可执行文件

echo "========================================"
echo "Nuitka 编译模式（macOS 版本）"
echo "========================================"
echo ""

# 检查 Python
if ! command -v python3 &> /dev/null; then
    echo "[错误] Python3 未安装"
    exit 1
fi

# 检查 Nuitka
if ! python3 -m pip show nuitka &> /dev/null; then
    echo "[提示] Nuitka 未安装，正在安装..."
    python3 -m pip install nuitka
    if [ $? -ne 0 ]; then
        echo "[错误] Nuitka 安装失败"
        exit 1
    fi
fi

# 检查 C 编译器
if ! command -v gcc &> /dev/null && ! command -v clang &> /dev/null; then
    echo ""
    echo "⚠️  未检测到 C 编译器"
    echo "请安装 Xcode Command Line Tools:"
    echo "  xcode-select --install"
    echo ""
    exit 1
fi

echo ""
echo "⚠️  重要提示："
echo "此脚本会在 macOS 上编译，生成的是 macOS 可执行程序"
echo "编译时间约 5-15 分钟，请耐心等待..."
echo ""
read -p "按 Enter 继续，或 Ctrl+C 退出..."

echo "[1/3] 清理旧文件..."
rm -rf build ScreenCapture.dist ScreenCapture.build ScreenCapture

echo "[2/3] 使用 Nuitka 编译（这可能需要5-15分钟）..."
python3 -m nuitka \
    --standalone \
    --onefile \
    --macos-create-app-bundle \
    --enable-plugin=anti-bloat \
    --assume-yes-for-downloads \
    --nofollow-import-to=unittest \
    --nofollow-import-to=test \
    --nofollow-import-to=tkinter \
    --output-filename=ScreenCapture \
    screenshot_tool.py

if [ $? -ne 0 ]; then
    echo "[错误] 编译失败"
    exit 1
fi

echo "[3/3] 整理输出..."
mkdir -p dist
if [ -f ScreenCapture ]; then
    mv ScreenCapture dist/ScreenCapture
    cp config.json dist/config.json
fi

# 清理临时文件
rm -rf ScreenCapture.dist ScreenCapture.build

echo ""
echo "========================================"
echo "编译完成！"
echo "输出目录: dist/"
echo "主程序: dist/ScreenCapture"
echo "配置文件: dist/config.json"
echo "========================================"
echo ""
echo "Nuitka 优势:"
echo "- 真正编译为原生代码（非打包）"
echo "- 性能更好，启动更快"
echo "- 更难被逆向工程"
echo ""
echo "运行方式:"
echo "  chmod +x dist/ScreenCapture"
echo "  ./dist/ScreenCapture"
echo ""

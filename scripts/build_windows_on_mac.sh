#!/bin/bash
# macOS 上使用 Docker 构建 Windows exe
# 通过 Docker 运行 Windows 容器来打包

echo "========================================"
echo "使用 Docker 构建 Windows exe（macOS）"
echo "========================================"
echo ""

# 检查 Docker
if ! command -v docker &> /dev/null; then
    echo "❌ Docker 未安装"
    echo ""
    echo "请先安装 Docker Desktop for Mac:"
    echo "  brew install --cask docker"
    echo "或访问: https://www.docker.com/products/docker-desktop"
    echo ""
    exit 1
fi

# 检查 Docker 是否运行
if ! docker info &> /dev/null; then
    echo "❌ Docker 未运行"
    echo "请启动 Docker Desktop 应用"
    exit 1
fi

echo "✅ Docker 已就绪"
echo ""
echo "构建方式: 使用 Wine + PyInstaller"
echo "预计时间: 首次约10-15分钟（下载镜像），后续约2-5分钟"
echo ""
read -p "按 Enter 继续，或 Ctrl+C 退出..."

# 清理旧的构建文件
echo ""
echo "[1/4] 清理旧文件..."
rm -rf build dist *.spec

# 构建 Docker 镜像
echo "[2/4] 准备 Docker 镜像（首次较慢）..."

# 创建临时 Dockerfile
cat > Dockerfile.windows << 'EOF'
FROM tobix/pywine:3.10

# 设置工作目录
WORKDIR /app

# 复制依赖文件
COPY requirements.txt .

# 安装依赖
RUN wine python -m pip install --upgrade pip && \
    wine python -m pip install -r requirements.txt && \
    wine python -m pip install pyinstaller

# 设置默认命令
CMD ["bash"]
EOF

# 构建镜像
docker build -f Dockerfile.windows -t screenshot-builder:windows . || {
    echo "❌ Docker 镜像构建失败"
    rm Dockerfile.windows
    exit 1
}

rm Dockerfile.windows

# 运行构建
echo "[3/4] 在 Docker 容器中打包 Windows exe..."

docker run --rm \
    -v "$(pwd):/app" \
    -w /app \
    screenshot-builder:windows \
    bash -c "wine python -m PyInstaller \
        --onefile \
        --noconsole \
        --strip \
        --noupx \
        --exclude-module matplotlib \
        --exclude-module numpy \
        --exclude-module pandas \
        --exclude-module tkinter \
        --exclude-module unittest \
        --exclude-module test \
        --name ScreenCapture \
        screenshot_tool.py"

if [ $? -ne 0 ]; then
    echo "❌ 打包失败"
    exit 1
fi

# 复制配置文件
echo "[4/4] 复制配置文件..."
cp config.json dist/config.json

echo ""
echo "========================================"
echo "✅ Windows exe 构建完成！"
echo "========================================"
echo ""
echo "输出目录: dist/"
echo "主程序: dist/ScreenCapture.exe"
echo "配置文件: dist/config.json"
echo ""
echo "⚠️  注意:"
echo "- exe 文件只能在 Windows 系统上运行"
echo "- 首次构建较慢，后续会快很多"
echo "- 生成的 exe 可能体积稍大（约 15-20 MB）"
echo ""

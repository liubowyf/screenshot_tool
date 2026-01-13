@echo off
REM Windows 自动截图工具 - 打包脚本
REM 使用 PyInstaller 打包为单文件 exe

echo ========================================
echo Windows Screenshot Tool - Build Script
echo ========================================
echo.

REM 检查 Python 是否安装
python --version >nul 2>&1
if errorlevel 1 (
    echo [错误] Python 未安装或未添加到 PATH
    pause
    exit /b 1
)

REM 检查 PyInstaller 是否安装
pip show pyinstaller >nul 2>&1
if errorlevel 1 (
    echo [提示] PyInstaller 未安装，正在安装...
    pip install pyinstaller
    if errorlevel 1 (
        echo [错误] PyInstaller 安装失败
        pause
        exit /b 1
    )
)

echo [1/3] 清理旧的构建文件...
if exist build rmdir /s /q build
if exist dist rmdir /s /q dist
if exist *.spec del /q *.spec

echo [2/3] 开始打包（包含所有运行时依赖+版本信息）...
pyinstaller --onefile ^
            --noconsole ^
            --strip ^
            --noupx ^
            --version-file=version_info.txt ^
            --exclude-module matplotlib ^
            --exclude-module numpy ^
            --exclude-module pandas ^
            --exclude-module tkinter ^
            --exclude-module unittest ^
            --exclude-module test ^
            --exclude-module scipy ^
            --exclude-module PyQt5 ^
            --exclude-module PyQt6 ^
            --exclude-module PySide2 ^
            --exclude-module PySide6 ^
            --exclude-module IPython ^
            --exclude-module jupyter ^
            --name ScreenCapture ^
            --icon NONE ^
            --add-data "config.json;." ^
            screenshot_tool.py

if errorlevel 1 (
    echo [错误] 打包失败
    pause
    exit /b 1
)

echo [3/3] 复制配置文件...
copy config.json dist\config.json >nul

echo.
echo ========================================
echo 打包完成！
echo 输出目录: dist\
echo 主程序: dist\ScreenCapture.exe
echo 配置文件: dist\config.json
echo ========================================
echo.
echo 使用说明:
echo 1. 编辑 config.json 配置服务器地址
echo 2. 双击运行 ScreenCapture.exe
echo 3. 程序将在后台运行，无窗口显示
echo 4. 日志文件位于 logs\ 目录
echo.

pause

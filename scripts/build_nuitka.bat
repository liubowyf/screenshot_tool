@echo off
REM 使用 Nuitka 编译 - 降低杀毒软件误报率
REM Nuitka 将Python代码编译为原生C代码，比PyInstaller误报率低30-50%

echo ========================================
echo Nuitka 编译模式（推荐：降低误报）
echo ========================================
echo.

REM 检查 Python
python --version >nul 2>&1
if errorlevel 1 (
    echo [错误] Python 未安装
    pause
    exit /b 1
)

REM 检查 Nuitka
pip show nuitka >nul 2>&1
if errorlevel 1 (
    echo [提示] Nuitka 未安装，正在安装...
    pip install nuitka
    if errorlevel 1 (
        echo [错误] Nuitka 安装失败
        pause
        exit /b 1
    )
)

REM 检查 C 编译器
echo.
echo 注意：Nuitka 需要 C 编译器
echo 如果没有安装，请选择以下之一：
echo   1. MinGW64: https://winlibs.com/
echo   2. Visual Studio Build Tools
echo.
pause

echo [1/3] 清理旧文件...
if exist build rmdir /s /q build
if exist ScreenCapture.dist rmdir /s /q ScreenCapture.dist
if exist ScreenCapture.build rmdir /s /q ScreenCapture.build
if exist ScreenCapture.exe del /q ScreenCapture.exe

echo [2/3] 使用 Nuitka 编译（这可能需要5-15分钟）...
python -m nuitka ^
    --standalone ^
    --onefile ^
    --windows-disable-console ^
    --enable-plugin=anti-bloat ^
    --assume-yes-for-downloads ^
    --nofollow-import-to=unittest ^
    --nofollow-import-to=test ^
    --nofollow-import-to=tkinter ^
    --output-filename=ScreenCapture.exe ^
    screenshot_tool.py

if errorlevel 1 (
    echo [错误] 编译失败
    pause
    exit /b 1
)

echo [3/3] 整理输出...
if not exist dist mkdir dist
if exist ScreenCapture.exe (
    move /y ScreenCapture.exe dist\ScreenCapture.exe >nul
    copy config.json dist\config.json >nul
)

REM 清理临时文件
if exist ScreenCapture.dist rmdir /s /q ScreenCapture.dist
if exist ScreenCapture.build rmdir /s /q ScreenCapture.build

echo.
echo ========================================
echo 编译完成！
echo 输出目录: dist\
echo 主程序: dist\ScreenCapture.exe
echo 配置文件: dist\config.json
echo ========================================
echo.
echo Nuitka 优势:
echo - 真正编译为原生代码（非打包）
echo - 杀毒软件误报率比 PyInstaller 低 30-50%%
echo - 性能更好，启动更快
echo - 更难被逆向工程
echo.

pause

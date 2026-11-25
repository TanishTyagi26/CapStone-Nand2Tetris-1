
@echo off
cd /d "%~dp0"

echo ========================================================
echo       Assembling Box.asm using assembler.py
echo ========================================================

call python.bat assembler.py Box.asm

if errorlevel 1 (
    echo.
    echo [ERROR] Assembly failed. Check the error above.
    pause
    exit /b 1
)

echo.
echo [SUCCESS] Box.hack and symbols.txt generated successfully!
echo ========================================================
pause

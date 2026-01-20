@echo off
REM ===== Strong run.bat that works from anywhere =====

REM %~dp0 是本 bat 所在資料夾 (playwright_py\scripts\)
set "SCRIPT_DIR=%~dp0"
REM 專案根目錄 = scripts 的上兩層
for %%I in ("%SCRIPT_DIR%..") do set "PW_DIR=%%~fI"
for %%I in ("%PW_DIR%\..") do set "ROOT_DIR=%%~fI"

cd /d "%ROOT_DIR%"

REM 優先使用 venv 的 python；若沒有則 fallback 到系統 python
set "PYEXE=python"
if exist ".\.venv\Scripts\python.exe" set "PYEXE=.\.venv\Scripts\python.exe"

%PYEXE% -m playwright install >NUL 2>&1

%PYEXE% -u ".\playwright_py\src\play_eplus_bot.py" --config ".\config\config.yaml" --selectors ".\config\selectors.json"

pause
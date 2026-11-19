@echo off
setlocal
set "SCRIPT_DIR=%~dp0"
python "%SCRIPT_DIR%verify_paper8.py" %*
if %ERRORLEVEL% NEQ 0 (
    echo Paper 8 verification failed with exit code %ERRORLEVEL%.
) else (
    echo Paper 8 verification completed successfully.
)
if "%~1"=="" pause
endlocal

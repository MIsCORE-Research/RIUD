@echo off
setlocal
set "SCRIPT_DIR=%~dp0"
python "%SCRIPT_DIR%verify_paper5.py" %*
if %ERRORLEVEL% NEQ 0 (
    echo Paper 5 verification failed with exit code %ERRORLEVEL%.
) else (
    echo Paper 5 verification completed successfully.
)
if "%~1"=="" pause
endlocal

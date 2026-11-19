@echo off
setlocal
set "SCRIPT_DIR=%~dp0"
python "%SCRIPT_DIR%verify_paper3.py" %*
if %ERRORLEVEL% NEQ 0 (
    echo Paper 3 verification failed with exit code %ERRORLEVEL%.
) else (
    echo Paper 3 verification completed successfully.
)
if "%~1"=="" pause
endlocal

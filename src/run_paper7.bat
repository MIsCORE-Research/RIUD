@echo off
setlocal
set "SCRIPT_DIR=%~dp0"
python "%SCRIPT_DIR%run_paper7.py" %*
if %ERRORLEVEL% NEQ 0 (
    echo Paper 7 verification failed with exit code %ERRORLEVEL%.
) else (
    echo Paper 7 verification completed successfully.
)
if "%~1"=="" pause
endlocal

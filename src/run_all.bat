@echo off
setlocal
set "SCRIPT_DIR=%~dp0"
python "%SCRIPT_DIR%run_all_verifications.py" %*
if %ERRORLEVEL% NEQ 0 (
    echo Master verification suite failed with exit code %ERRORLEVEL%.
) else (
    echo Master verification suite completed successfully.
)
if "%~1"=="" pause
endlocal

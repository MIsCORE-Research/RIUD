@echo off
setlocal
set "SCRIPT_DIR=%~dp0"
python "%SCRIPT_DIR%reproduce_paper4.py" %*
if %ERRORLEVEL% NEQ 0 (
    echo Paper 4 reproduction failed with exit code %ERRORLEVEL%.
) else (
    echo Paper 4 reproduction completed successfully.
)
if "%~1"=="" pause
endlocal

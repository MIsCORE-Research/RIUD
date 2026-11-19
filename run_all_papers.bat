@echo off
setlocal
set "ROOT_DIR=%~dp0"
python "%ROOT_DIR%src\run_all_verifications.py" %*
if %ERRORLEVEL% NEQ 0 (
    echo [FAIL] One or more paper verifications failed.
) else (
    echo [PASS] All 8 papers verified successfully.
)
if "%~1"=="" pause
endlocal

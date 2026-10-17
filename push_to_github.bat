@echo off
title Publication AlphaBot sur GitHub
echo ========================================================
echo        Publication d'AlphaBot Trading sur GitHub
echo ========================================================
echo.

cd /d "%~dp0"

echo [1/2] Creation et push sur votre compte GitHub (Njgctxf)...
"C:\Program Files\GitHub CLI\gh.exe" repo create "Njgctxf/AlphaBot-Autonomous-Trading" --public --source=. --remote=origin --push

if %ERRORLEVEL% EQU 0 (
    echo.
    echo ========================================================
    echo Succes ! Votre projet est en ligne :
    echo https://github.com/Njgctxf/AlphaBot-Autonomous-Trading
    echo ========================================================
) else (
    echo.
    echo Note: Si la limite horaire de GitHub est encore active,
    echo patientez quelques minutes et relancez ce fichier.
)

pause

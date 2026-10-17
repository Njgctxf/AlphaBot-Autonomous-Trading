@echo off
title AlphaBot - Agent de Trading Autonome (Paper Trading)
echo ================================================================
echo         ALPHABOT - AGENT DE TRADING QUANTITATIF AUTONOME
echo         Simulation 100%% Securisee (Fonds Virtuels 10 000 $)
echo ================================================================
echo.

cd /d "%~dp0"

echo [1/2] Verification des dependances...
python -m pip install -r requirements.txt --quiet

echo.
echo [2/2] Demarrage de l'agent et de la console sur http://localhost:5055 ...
echo.
start "" http://localhost:5055
python app.py
pause

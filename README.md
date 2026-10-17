# 🤖 AlphaBot — Agent de Trading Quantitatif Autonome (Paper Trading)

> **Moteur de trading algorithmique autonome en environnement de simulation sécurisé (Zéro risque financier).**

## 💡 Principes Clés
- **100% Hors-Risque (Paper Trading)** : Opère sur un portefeuille virtuel de 10 000,00 $ avec exécution d'ordres simulés.
- **Flux de Marché Réel** : Récupère le cours direct de BTC/USDT en temps réel.
- **Stratégie Algorithmique Multi-Indicateurs** :
  - Croisement de moyennes mobiles exponentielles (EMA 9 et EMA 21).
  - Indice de force relative (RSI 14) pour éviter les zones de surachat.
- **Gestion Stricte du Risque (Risk Management)** :
  - Taille de position maximale : 25% du capital par trade.
  - **Stop-Loss automatique** : -1,0% (coupe immédiatement la perte).
  - **Take-Profit automatique** : +2,2% (sécurise le gain).
  - Sortie d'invalidation sur retournement de tendance.

## 🚀 Démarrage Rapide
Double-cliquez sur `start.bat` ou lancez :
```bash
cd trading-bot
pip install -r requirements.txt
python app.py
```
Accédez au tableau de bord en direct sur : **`http://localhost:5055`**

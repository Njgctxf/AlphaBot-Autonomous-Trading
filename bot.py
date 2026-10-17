"""
bot.py - Autonomous Quantitative Trading Agent (Paper Trading Sandbox)
Executes autonomous market monitoring, algorithmic strategy calculation,
and virtual order execution with strict capital protection rules.
"""

import time
import threading
import random
from datetime import datetime
import requests

class AutonomousTradingAgent:
    def __init__(self, initial_balance=10000.0):
        self.initial_balance = initial_balance
        self.balance_usd = initial_balance
        self.position = {
            "active": False,
            "btc_amount": 0.0,
            "entry_price": 0.0,
            "stop_loss": 0.0,
            "take_profit": 0.0,
            "entry_time": None
        }
        self.price_history = []
        self.trade_history = []
        self.logs = []
        self.is_running = True
        self.current_price = 68500.0  # Initial baseline
        self.lock = threading.RLock()

        # Start autonomous execution loop in background
        self.thread = threading.Thread(target=self._autonomous_loop, daemon=True)
        self.thread.start()

    def log(self, message, category="INFO"):
        entry = {
            "time": datetime.now().strftime("%H:%M:%S"),
            "category": category,
            "message": message
        }
        with self.lock:
            self.logs.insert(0, entry)
            if len(self.logs) > 60:
                self.logs.pop()

    def fetch_live_price(self):
        """Fetches live public BTC price or simulates realistic market fluctuations."""
        try:
            resp = requests.get("https://api.binance.com/api/v3/ticker/price?symbol=BTCUSDT", timeout=3)
            if resp.status_code == 200:
                return float(resp.json()["price"])
        except Exception:
            pass
        # Realistic fallback walk (+- 0.15% per tick)
        drift = random.uniform(-0.002, 0.0022)
        return round(self.current_price * (1.0 + drift), 2)

    def calculate_indicators(self):
        """Calculates Short EMA, Long EMA, and RSI."""
        prices = self.price_history
        if len(prices) < 15:
            return {"ema_fast": None, "ema_slow": None, "rsi": 50.0}

        # Simple EMA calculation
        def calc_ema(values, period):
            k = 2 / (period + 1)
            ema = values[0]
            for val in values[1:]:
                ema = (val * k) + (ema * (1 - k))
            return ema

        ema_fast = calc_ema(prices[-9:], 9)
        ema_slow = calc_ema(prices[-21:], 21) if len(prices) >= 21 else ema_fast

        # RSI 14
        deltas = [prices[i] - prices[i-1] for i in range(1, min(15, len(prices)))]
        gains = [d for d in deltas if d > 0]
        losses = [-d for d in deltas if d < 0]

        avg_gain = sum(gains) / 14 if gains else 0.0001
        avg_loss = sum(losses) / 14 if losses else 0.0001
        rs = avg_gain / avg_loss
        rsi = 100 - (100 / (1 + rs))

        return {
            "ema_fast": round(ema_fast, 2),
            "ema_slow": round(ema_slow, 2),
            "rsi": round(rsi, 1)
        }

    def _autonomous_loop(self):
        """Core autonomous decision & transaction cycle."""
        self.log("Démarrage de l'agent de trading autonome (Mode Simulation Sécurisée).", "START")
        
        # Pre-fill initial prices
        initial_p = self.fetch_live_price()
        self.current_price = initial_p
        self.price_history = [initial_p * (1.0 + random.uniform(-0.005, 0.005)) for _ in range(25)]

        while True:
            if self.is_running:
                price = self.fetch_live_price()
                with self.lock:
                    self.current_price = price
                    self.price_history.append(price)
                    if len(self.price_history) > 80:
                        self.price_history.pop(0)

                    indicators = self.calculate_indicators()
                    self._evaluate_strategy(price, indicators)

            time.sleep(3)

    def _evaluate_strategy(self, price, indicators):
        """Evaluates automated strategy and triggers execution."""
        # 1. Manage Active Position (Check Stop-Loss & Take-Profit)
        if self.position["active"]:
            entry = self.position["entry_price"]
            pnl_pct = ((price - entry) / entry) * 100

            # Take-Profit triggered (+2.0%)
            if price >= self.position["take_profit"]:
                self._execute_sell(price, reason="TAKE_PROFIT", pnl_pct=pnl_pct)
                return

            # Stop-Loss triggered (-1.0%)
            elif price <= self.position["stop_loss"]:
                self._execute_sell(price, reason="STOP_LOSS", pnl_pct=pnl_pct)
                return

            # Technical Exit: EMA fast crosses below EMA slow
            elif indicators["ema_fast"] and indicators["ema_slow"] and indicators["ema_fast"] < indicators["ema_slow"] and pnl_pct > 0.4:
                self._execute_sell(price, reason="MOMENTUM_REVERSAL", pnl_pct=pnl_pct)
                return

        # 2. Look for Buy Signal if no active position
        elif not self.position["active"]:
            ema_fast = indicators["ema_fast"]
            ema_slow = indicators["ema_slow"]
            rsi = indicators["rsi"]

            if ema_fast and ema_slow:
                # Buy condition: Uptrend crossover and RSI not overbought (< 68)
                if ema_fast > ema_slow and rsi < 68 and rsi > 35:
                    # Risk control: Invest 25% of virtual capital max per trade
                    investment_usd = self.balance_usd * 0.25
                    if investment_usd >= 100:
                        self._execute_buy(price, investment_usd)

    def _execute_buy(self, price, amount_usd):
        """Executes automated BUY transaction."""
        btc_bought = round(amount_usd / price, 6)
        self.balance_usd -= amount_usd

        stop_loss = round(price * 0.990, 2)    # -1.0%
        take_profit = round(price * 1.022, 2)  # +2.2%

        self.position = {
            "active": True,
            "btc_amount": btc_bought,
            "entry_price": price,
            "cost_usd": amount_usd,
            "stop_loss": stop_loss,
            "take_profit": take_profit,
            "entry_time": datetime.now().strftime("%H:%M:%S")
        }

        self.log(
            f"🟢 ORDRE ACHAT AUTOMATIQUE : {btc_bought} BTC @ {price:,.2f} $ | SL: {stop_loss:,.2f} $ | TP: {take_profit:,.2f} $",
            "BUY"
        )

    def _execute_sell(self, price, reason, pnl_pct):
        """Executes automated SELL transaction and calculates PnL."""
        btc_amount = self.position["btc_amount"]
        proceeds = round(btc_amount * price, 2)
        profit_usd = round(proceeds - self.position["cost_usd"], 2)

        self.balance_usd += proceeds

        trade_record = {
            "id": len(self.trade_history) + 1,
            "type": "BUY/SELL",
            "amount_btc": btc_amount,
            "entry_price": self.position["entry_price"],
            "exit_price": price,
            "entry_time": self.position["entry_time"],
            "exit_time": datetime.now().strftime("%H:%M:%S"),
            "profit_usd": profit_usd,
            "pnl_pct": round(pnl_pct, 2),
            "reason": reason
        }

        self.trade_history.insert(0, trade_record)
        self.position = {"active": False, "btc_amount": 0.0, "entry_price": 0.0, "stop_loss": 0.0, "take_profit": 0.0, "entry_time": None}

        icon = "🎯" if profit_usd >= 0 else "🛑"
        self.log(
            f"{icon} ORDRE VENTE AUTOMATIQUE ({reason}) : @ {price:,.2f} $ | PnL: {profit_usd:+.2f} $ ({pnl_pct:+.2f}%)",
            "SELL" if profit_usd >= 0 else "STOP"
        )

    def get_state(self):
        """Returns full telemetry for the UI dashboard."""
        with self.lock:
            # Current equity
            current_equity = self.balance_usd
            unrealized_pnl = 0.0
            if self.position["active"]:
                unrealized_pnl = (self.position["btc_amount"] * self.current_price) - self.position["cost_usd"]
                current_equity += (self.position["btc_amount"] * self.current_price)

            # Win rate
            wins = sum(1 for t in self.trade_history if t["profit_usd"] > 0)
            total_trades = len(self.trade_history)
            win_rate = round((wins / total_trades * 100), 1) if total_trades > 0 else 0.0

            indicators = self.calculate_indicators()

            return {
                "is_running": self.is_running,
                "current_price": self.current_price,
                "balance_usd": round(self.balance_usd, 2),
                "total_equity": round(current_equity, 2),
                "total_pnl": round(current_equity - self.initial_balance, 2),
                "total_pnl_pct": round(((current_equity - self.initial_balance) / self.initial_balance) * 100, 2),
                "unrealized_pnl": round(unrealized_pnl, 2),
                "position": self.position,
                "win_rate": win_rate,
                "total_trades": total_trades,
                "price_history": self.price_history[-30:],
                "indicators": indicators,
                "trade_history": self.trade_history[:15],
                "logs": self.logs[:30]
            }

    def toggle(self):
        self.is_running = not self.is_running
        status = "ACTIF" if self.is_running else "EN PAUSE"
        self.log(f"Statut de l'agent modifié : {status}", "SYSTEM")
        return self.is_running

    def reset(self):
        with self.lock:
            self.balance_usd = self.initial_balance
            self.position = {"active": False, "btc_amount": 0.0, "entry_price": 0.0, "stop_loss": 0.0, "take_profit": 0.0, "entry_time": None}
            self.trade_history = []
            self.log("Portefeuille de simulation réinitialisé à 10 000,00 $.", "SYSTEM")

# Global singleton
agent = AutonomousTradingAgent()

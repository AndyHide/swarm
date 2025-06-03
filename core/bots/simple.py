from core.bots.base import TraderBot
import random


class RSIBot(TraderBot):
    def __init__(self, rsi_period=14, rsi_entry=30):
        self.rsi_period = rsi_period
        self.rsi_entry = rsi_entry

    def signal(self, row):
        value = row.get(f"rsi_{self.rsi_period}")
        return 1 if value is not None and value < self.rsi_entry else 0


class RSIBotStochastic(TraderBot):
    def __init__(self, rsi_period=14, rsi_entry=30, noise=5):
        self.rsi_period = rsi_period
        self.rsi_entry = rsi_entry
        self.noise = noise

    def signal(self, row):
        value = row.get(f"rsi_{self.rsi_period}")
        if value is None:
            return 0
        noisy_value = value + random.uniform(-self.noise, self.noise)
        return 1 if noisy_value < self.rsi_entry else 0


class MACDBot(TraderBot):
    def __init__(self, zero_cross=False):
        self.zero_cross = zero_cross

    def signal(self, row):
        macd = row.get("macd")
        signal = row.get("macd_signal")
        if macd is None or signal is None:
            return 0
        if self.zero_cross:
            return 1 if macd > 0 and signal < 0 else 0
        else:
            return 1 if macd > signal else 0


class SmaCrossBot(TraderBot):
    def __init__(self, fast=20, slow=50):
        self.fast = fast
        self.slow = slow

    def signal(self, row):
        fast_val = row.get(f"sma_{self.fast}")
        slow_val = row.get(f"sma_{self.slow}")
        if fast_val is None or slow_val is None:
            return 0
        return 1 if fast_val > slow_val else 0


class RSIMACDComboBot(TraderBot):
    def __init__(self, rsi_period=14, rsi_entry=30):
        self.rsi_period = rsi_period
        self.rsi_entry = rsi_entry

    def signal(self, row):
        rsi_val = row.get(f"rsi_{self.rsi_period}")
        macd = row.get("macd")
        signal = row.get("macd_signal")
        if rsi_val is None or macd is None or signal is None:
            return 0
        return 1 if rsi_val < self.rsi_entry and macd > signal else 0


# 🎲 Функция для случайного создания бота и его параметров (используется в gene_pool)
def random_bot_params():
    strategy_choices = [
        ("RSIBot", {"rsi_period": random.choice([10, 14, 20]), "rsi_entry": random.randint(20, 40)}),
        ("RSIBotStochastic", {
            "rsi_period": random.choice([10, 14, 20]),
            "rsi_entry": random.randint(20, 40),
            "noise": random.randint(2, 10)
        }),
        ("MACDBot", {"zero_cross": random.choice([True, False])}),
        ("SmaCrossBot", {
            "fast": random.choice([10, 20, 30]),
            "slow": random.choice([50, 100])
        }),
        ("RSIMACDComboBot", {
            "rsi_period": random.choice([10, 14, 20]),
            "rsi_entry": random.randint(20, 40)
        }),
    ]
    strategy_type, params = random.choice(strategy_choices)
    return {"strategy_type": strategy_type, "params": params}

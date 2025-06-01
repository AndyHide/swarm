from core.bots.base import TraderBot
import random


class RSIBot(TraderBot):
    def __init__(self, threshold: float = 30):
        self.threshold = threshold

    def signal(self, row):
        if row["rsi_14"] < self.threshold:
            return 1
        elif row["rsi_14"] > (100 - self.threshold):
            return -1
        return 0

    def describe(self):
        return f"RSIBot(th={self.threshold})"

    def get_params(self):
        return {"threshold": self.threshold}


class RSIBotStochastic(TraderBot):
    def __init__(self, threshold: float = 30, randomness: float = 0.1):
        self.threshold = threshold
        self.randomness = randomness

    def signal(self, row):
        rsi = row["rsi_14"]
        rnd = random.random()
        if rsi < self.threshold and rnd > self.randomness:
            return 1
        elif rsi > (100 - self.threshold) and rnd > self.randomness:
            return -1
        return 0

    def describe(self):
        return f"RSIBotStochastic(th={self.threshold}, rand={self.randomness})"

    def get_params(self):
        return {"threshold": self.threshold, "randomness": self.randomness}


class MACDBot(TraderBot):
    def __init__(self, zero_cross: bool = True):
        self.zero_cross = zero_cross

    def signal(self, row):
        if self.zero_cross:
            if row["macd"] > 0 and row["macd_signal"] < 0:
                return 1
            elif row["macd"] < 0 and row["macd_signal"] > 0:
                return -1
        else:
            if row["macd_diff"] > 0:
                return 1
            elif row["macd_diff"] < 0:
                return -1
        return 0

    def describe(self):
        return f"MACDBot(zero_cross={self.zero_cross})"

    def get_params(self):
        return {"zero_cross": self.zero_cross}


class SmaCrossBot(TraderBot):
    def __init__(self, fast: int = 20, slow: int = 50):
        self.fast = fast
        self.slow = slow

    def signal(self, row):
        if row.get(f"sma_{self.fast}") is None or row.get(f"sma_{self.slow}") is None:
            return 0
        if row[f"sma_{self.fast}"] > row[f"sma_{self.slow}"]:
            return 1
        elif row[f"sma_{self.fast}"] < row[f"sma_{self.slow}"]:
            return -1
        return 0

    def describe(self):
        return f"SmaCrossBot({self.fast}>{self.slow})"

    def get_params(self):
        return {"fast": self.fast, "slow": self.slow}


class RSIMACDComboBot(TraderBot):
    def __init__(self, rsi_th: float = 30):
        self.rsi_th = rsi_th

    def signal(self, row):
        if row["rsi_14"] < self.rsi_th and row["macd_diff"] > 0:
            return 1
        elif row["rsi_14"] > (100 - self.rsi_th) and row["macd_diff"] < 0:
            return -1
        return 0

    def describe(self):
        return f"RSIMACDComboBot(rsi={self.rsi_th})"

    def get_params(self):
        return {"rsi_th": self.rsi_th}

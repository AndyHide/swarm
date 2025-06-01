from core.data_loader import load_ohlcv_with_features
from core.target_generator import generate_classification_target
from core.evaluator import evaluate_bots

from core.bots.simple import (
    RSIBot,
    RSIBotStochastic,
    MACDBot,
    SmaCrossBot,
    RSIMACDComboBot,
)


# Шаг 1 — загрузка данных
df = load_ohlcv_with_features("BTC/USDT", "5m", n_candles=5000)
df["future_return"] = (df["close"].shift(-12) - df["close"]) / df["close"]
df = generate_classification_target(df, horizon=12, threshold=0.0015)

# Шаг 2 — список ботов
bots = [
    RSIBot(30),
    RSIBot(35),
    RSIBotStochastic(30, 0.05),
    RSIBotStochastic(30, 0.2),
    MACDBot(zero_cross=True),
    MACDBot(zero_cross=False),
    SmaCrossBot(20, 50),
    RSIMACDComboBot(30),
]

# Шаг 3 — прогоним оценку
results = evaluate_bots(df, bots)

# Шаг 4 — выводим
for res in results:
    print(f"{res['bot']}")
    print(f"  Return:   {res['total_return']:.2%}")
    print(f"  Accuracy: {res['accuracy']:.2%}")
    print(f"  Trades:   {res['n_signals']}")
    print(f"  Params:   {bots[results.index(res)].get_params()}")
    print("-" * 40)

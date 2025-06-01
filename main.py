from core.data_loader import load_ohlcv_with_features
from core.target_generator import generate_classification_target
from core.backtester import backtest_signals


# 1. Загрузка и фичи
df = load_ohlcv_with_features(
    pair="BTC/USDT",
    timeframe="5m",
    n_candles=5000,
    mode="last_n"
)

# 2. Добавляем future_return — для оценки прибыли
df["future_return"] = (df["close"].shift(-12) - df["close"]) / df["close"]

# 3. Генерация таргетов
df = generate_classification_target(df, horizon=12, threshold=0.0015)

# 4. Сигнальная стратегия — RSI + MACD (только покупки)
def rsi_macd_long(row):
    if row["rsi_14"] < 30 and row["macd_diff"] > 0:
        return 1
    return 0

# 5. Прогон
results = backtest_signals(df, signal_func=rsi_macd_long)

# 6. Результат
print(results)
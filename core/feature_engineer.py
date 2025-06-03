import pandas as pd
import numpy as np
import ta


def generate_features(df: pd.DataFrame, horizon: int = 12) -> pd.DataFrame:
    """
    Обогащает свечи техническими фичами и целевой переменной future_return.
    """
    df = df.copy()

    # Базовые фичи
    df["log_return"] = np.log(df["close"] / df["close"].shift(1))
    df["price_change"] = df["close"] - df["open"]
    df["range"] = df["high"] - df["low"]
    df["body_ratio"] = df["price_change"] / df["range"].replace(0, np.nan)

    close = df["close"]
    high = df["high"]
    low = df["low"]
    volume = df["volume"]

    # Список RSI, SMA и EMA для разных стратегий
    rsi_periods = [10, 14, 20]
    sma_periods = [10, 20, 30, 50, 100]
    ema_periods = [20]

    for p in rsi_periods:
        df[f"rsi_{p}"] = ta.momentum.rsi(close, window=p)

    for p in sma_periods:
        df[f"sma_{p}"] = ta.trend.sma_indicator(close, window=p)

    for p in ema_periods:
        df[f"ema_{p}"] = ta.trend.ema_indicator(close, window=p)

    # MACD
    df["macd"] = ta.trend.macd(close)
    df["macd_signal"] = ta.trend.macd_signal(close)
    df["macd_diff"] = df["macd"] - df["macd_signal"]

    # Bollinger Bands
    boll = ta.volatility.BollingerBands(close)
    df["boll_mid"] = boll.bollinger_mavg()
    df["boll_high"] = boll.bollinger_hband()
    df["boll_low"] = boll.bollinger_lband()
    df["boll_width"] = df["boll_high"] - df["boll_low"]

    # Волатильность
    df["volatility_20"] = df["log_return"].rolling(window=20).std()

    # Объём
    df["volume_sma_20"] = ta.trend.sma_indicator(volume, window=20)
    df["volume_spike"] = df["volume"] / df["volume_sma_20"]

    # Целевая переменная: future return
    df["future_return"] = df["close"].shift(-horizon) / df["close"] - 1

    df.dropna(inplace=True)
    return df

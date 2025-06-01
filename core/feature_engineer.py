import pandas as pd
import numpy as np
import ta


def generate_features(df: pd.DataFrame) -> pd.DataFrame:
    """
    Добавляет технические индикаторы и фичи в DataFrame со свечами.
    """
    df = df.copy()

    # Базовые фичи
    df["log_return"] = np.log(df["close"] / df["close"].shift(1))
    df["price_change"] = df["close"] - df["open"]
    df["range"] = df["high"] - df["low"]
    df["body_ratio"] = df["price_change"] / df["range"].replace(0, np.nan)

    # Источники
    close = df["close"]
    high = df["high"]
    low = df["low"]
    volume = df["volume"]

    # Скользящие
    df["sma_20"] = ta.trend.sma_indicator(close, window=20)
    df["sma_50"] = ta.trend.sma_indicator(close, window=50)
    df["ema_20"] = ta.trend.ema_indicator(close, window=20)

    # RSI
    df["rsi_14"] = ta.momentum.rsi(close, window=14)

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

    df.dropna(inplace=True)
    return df

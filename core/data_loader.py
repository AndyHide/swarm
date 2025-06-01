import os
import time
import ccxt
import pandas as pd
from datetime import datetime, timedelta
from typing import Optional, Literal
from core.feature_engineer import generate_features


CACHE_PATH = "data/cache"
TIMEFRAME_DELTA = {
    "1m": timedelta(minutes=1),
    "5m": timedelta(minutes=5),
    "15m": timedelta(minutes=15),
    "1h": timedelta(hours=1),
    "4h": timedelta(hours=4),
    "1d": timedelta(days=1)
}


def load_ohlcv_with_features(
    pair: str,
    timeframe: str,
    mode: Literal["range", "from_date", "last_n", "forward_fill", "recent_days"] = "last_n",
    start_date: Optional[str] = None,
    end_date: Optional[str] = None,
    n_candles: Optional[int] = 100000,
    recent_days: Optional[int] = 30,
    min_date: Optional[str] = "2022-01-01",
    overwrite_cache: bool = False,
    verbose: bool = True
) -> pd.DataFrame:
    """
    Загружает OHLCV с Binance и автоматически добавляет фичи.
    Всегда сохраняет объединённый DataFrame в *_full.parquet
    """
    os.makedirs(CACHE_PATH, exist_ok=True)
    binance = ccxt.binance()
    symbol = pair.replace("/", "")
    filename = f"{symbol}_{timeframe}_full.parquet"
    filepath = os.path.join(CACHE_PATH, filename)

    if os.path.exists(filepath) and not overwrite_cache and mode != "forward_fill":
        if verbose:
            print(f"[CACHE] Загружаю: {filepath}")
        return pd.read_parquet(filepath)

    now = datetime.utcnow()
    min_dt = pd.Timestamp(min_date)
    since = None
    until = now

    if mode == "range":
        since = pd.Timestamp(start_date)
        until = pd.Timestamp(end_date)
    elif mode == "from_date":
        since = pd.Timestamp(start_date or min_date)
    elif mode == "recent_days":
        since = now - timedelta(days=recent_days or 30)
    elif mode == "last_n":
        delta = TIMEFRAME_DELTA[timeframe] * (n_candles or 100_000)
        candidate_since = now - delta
        since = max(candidate_since, min_dt)
    elif mode == "forward_fill":
        if os.path.exists(filepath):
            existing_df = pd.read_parquet(filepath)
            since = existing_df.index[-1] + TIMEFRAME_DELTA[timeframe]
        else:
            since = pd.Timestamp(min_date)
    else:
        raise ValueError(f"Неверный режим: {mode}")

    since_ms = int(since.timestamp() * 1000)
    until_ts = int(until.timestamp() * 1000)
    all_ohlcv = []

    if verbose:
        print(f"[{mode.upper()}] Загружаю {pair} {timeframe} с {since} по {until}")

    while since_ms < until_ts:
        chunk = binance.fetch_ohlcv(pair, timeframe, since=since_ms, limit=1000)
        if not chunk:
            break
        all_ohlcv.extend(chunk)
        since_ms = chunk[-1][0] + int(TIMEFRAME_DELTA[timeframe].total_seconds() * 1000)
        time.sleep(binance.rateLimit / 1000)

        if mode == "last_n" and len(all_ohlcv) >= n_candles:
            break

    df = pd.DataFrame(all_ohlcv, columns=["timestamp", "open", "high", "low", "close", "volume"])
    df["timestamp"] = pd.to_datetime(df["timestamp"], unit="ms")
    df.set_index("timestamp", inplace=True)
    df = df[~df.index.duplicated(keep="last")].sort_index()

    df = generate_features(df)

    df.to_parquet(filepath)
    if verbose:
        print(f"[FULL] Сохранил с фичами: {filepath}")

    return df

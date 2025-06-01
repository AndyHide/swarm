from core.data_loader import load_batch_ohlcv

pairs = ["BTC/USDT", "ETH/USDT"]
timeframes = ["1m", "5m"]

data = load_batch_ohlcv(
    pairs=pairs,
    timeframes=timeframes,
    mode="last_n",
    n_candles=50000
)

# Пример доступа:
btc_1m = data["BTC/USDT"]["1m"]
eth_5m = data["ETH/USDT"]["5m"]

print(btc_1m.tail())
print(eth_5m.tail())

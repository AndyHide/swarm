from core.data_loader import load_ohlcv_with_features
from core.target_generator import generate_classification_target
from core.genetics.population_runner import run_generation

# Загружаем данные
df = load_ohlcv_with_features("BTC/USDT", "5m", n_candles=10000)
df["future_return"] = (df["close"].shift(-12) - df["close"]) / df["close"]
df = generate_classification_target(df, horizon=12, threshold=0.0015)

print("future_return describe:")
print(df["future_return"].describe())

# Первый запуск
generation = None

for gen_num in range(5):
    print(f"\n=== Generation {gen_num} ===")
    generation, results = run_generation(df, previous_genomes=generation, population_size=40)

    top = results[0]
    print(f"🏆 Best: {top['bot']} | Return: {top['total_return']:.2%} | Acc: {top['accuracy']:.2%} | Trades: {top['n_signals']}")

from core.data_loader import load_ohlcv_with_features
from core.genetics.population_runner import run_generation
from core.target_generator import generate_classification_target

df = load_ohlcv_with_features("BTC/USDT", "15m", n_candles=10000)
df = generate_classification_target(df, horizon=12, threshold=0.0010)

population = None
for gen in range(5):
    print(f"\n🧬 Поколение {gen}")
    population, results = run_generation(df, population, generation=gen)
    top = results[0]
    print(f"🏆 Доходность лучшего: {top['total_return']:.2%} | Точность: {top['accuracy']:.2%} | Сделок: {top['n_signals']}")

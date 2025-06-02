from core.data_loader import load_ohlcv_with_features
from core.target_generator import generate_classification_target
from core.genetics.population_runner import run_generation

# 📊 Загрузка данных и фичей
df = load_ohlcv_with_features("BTC/USDT", "5m", n_candles=20000)

# 🎯 Генерация таргета
df = generate_classification_target(df, horizon=12, threshold=0.0015)

# ⚙️ Эволюционный цикл
N_GENERATIONS = 10
population = None

for gen in range(N_GENERATIONS):
    print(f"\n=== Поколение {gen} ===")

    population, results = run_generation(
        df,
        generation=gen,
        previous_genomes=population,
        population_size=50,
        elite_frac=0.2,
        mutation_rate=0.3
    )

    top = results[0]
    print(f"Доходность лучшего: {top['total_return']:.2%} | Точность: {top['accuracy']:.2%} | Winrate: {top['winrate']:.2%}")

import random
from core.genetics.gene_pool import random_genome
from core.genetics.genetic_ops import mutate_genome, crossover_genomes
from core.genetics.genome import Genome
from core.evaluator import evaluate_bots

from core.logger import (
    log_generation_info,
    save_bot_genome,
    append_metrics_csv
)

def run_generation(df, generation=0, previous_genomes=None, population_size=50, elite_frac=0.2, mutation_rate=0.3):
    """
    Запускает одну волну эволюции:
    - генерирует популяцию
    - проводит бэктест
    - сохраняет логи
    - возвращает топовых выживших и результаты
    """
    population = []

    # 1. Элиту копируем без изменений
    if previous_genomes:
        elites = previous_genomes[:int(population_size * elite_frac)]
        population.extend(elites)

        # 2. Мутации
        mutants = [mutate_genome(g, mutation_rate) for g in elites]
        population.extend(mutants)

        # 3. Кроссоверы
        children = [
            crossover_genomes(random.choice(elites), random.choice(elites))
            for _ in range(population_size - len(population))
        ]
        population.extend(children)
    else:
        # Первый запуск — случайная популяция
        population = [random_genome() for _ in range(population_size)]

    # 4. Бэктест
    bots = [g.create_bot() for g in population]
    results = evaluate_bots(df, bots)

    # 5. Сортировка по доходности
    results_sorted = sorted(results, key=lambda x: x["total_return"], reverse=True)

    # 6. Логгирование
    top_bot_idx = results.index(results_sorted[0])
    top_genome = population[top_bot_idx]
    top_metrics = results_sorted[0]
    avg_return = sum(r["total_return"] for r in results) / len(results)

    log_generation_info(generation, {
        "average_score": avg_return,
        "population_size": len(population),
        "top_bot": {
            "score": top_metrics["total_return"],
            "accuracy": top_metrics["accuracy"],
            "winrate": top_metrics["winrate"],
            "n_signals": top_metrics["n_signals"]
        }
    })

    save_bot_genome(top_genome, generation, rank=1)

    append_metrics_csv({
        "generation": generation,
        "score": top_metrics["total_return"],
        "accuracy": top_metrics["accuracy"],
        "winrate": top_metrics["winrate"],
        "n_signals": top_metrics["n_signals"]
    })

    # 7. Отдаём лучшие геномы (в порядке убывания доходности)
    survivors = [population[results.index(r)] for r in results_sorted[:population_size]]

    return survivors, results_sorted

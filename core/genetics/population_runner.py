import random
from core.genetics.gene_pool import random_genome
from core.genetics.genome import Genome
from core.genetics.selector import select_next_generation
from core.evaluator import evaluate_bots
from core.logger import (
    log_generation_info,
    save_bot_genome,
    append_metrics_csv
)


def run_generation(
    df,
    generation=0,
    previous_genomes=None,
    population_size=50,
    elite_frac=0.2,
    mutation_rate=0.3
):
    """
    Запускает одну волну эволюции:
    - формирует популяцию (первую или следующую)
    - проводит бэктест
    - сохраняет логи
    - возвращает лучших
    """

    if previous_genomes:
        population = select_next_generation(
            previous_genomes=previous_genomes,
            population_size=population_size,
            elite_frac=elite_frac,
            mutation_rate=mutation_rate,
            new_blood_frac=0.1  # 💉 теперь добавляем "свежую кровь"
        )
    else:
        population = [random_genome() for _ in range(population_size)]

    # Бэктест всей популяции
    bots = [g.create_bot() for g in population]
    results = evaluate_bots(df, bots)

    # Сортировка по доходности
    results_sorted = sorted(results, key=lambda x: x["total_return"], reverse=True)

    # Логгирование
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

    # Отдаём лучшие геномы (в том же порядке, что отсортированы результаты)
    survivors = [population[results.index(r)] for r in results_sorted[:population_size]]

    return survivors, results_sorted

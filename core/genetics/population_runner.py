import random
from core.genetics.gene_pool import random_genome
from core.genetics.genetic_ops import mutate_genome, crossover_genomes
from core.genetics.genome import Genome
from core.evaluator import evaluate_bots
from core.logger import save_bot_genome, log_generation_info, append_metrics_csv


def run_generation(
    df,
    previous_genomes=None,
    population_size=50,
    elite_frac=0.2,
    mutation_rate=0.3,
    generation=0
):
    """
    Запускает одну волну эволюции:
    - генерирует популяцию
    - проводит бэктест
    - логирует и возвращает лучших
    """

    population = []

    if previous_genomes:
        elites = previous_genomes[:int(population_size * elite_frac)]

        # Увеличиваем возраст
        for g in elites:
            g.age += 1

        population.extend(elites)

        # Мутации
        mutants = [mutate_genome(g, mutation_rate) for g in elites]
        population.extend(mutants)

        # Кроссоверы
        children = [
            crossover_genomes(random.choice(elites), random.choice(elites))
            for _ in range(population_size - len(population))
        ]
        population.extend(children)
    else:
        population = [random_genome() for _ in range(population_size)]

    # Бэктест
    bots = [g.create_bot() for g in population]
    results = evaluate_bots(df, bots)

    # Сортировка с сохранением индексов
    indexed_results = list(enumerate(results))
    results_sorted = sorted(indexed_results, key=lambda x: x[1]["total_return"], reverse=True)

    # Выбор лучших по индексам
    survivor_indices = [i for i, _ in results_sorted[:population_size]]
    survivors = [population[i] for i in survivor_indices]

    # Топ-бот
    top_index, top_metrics = results_sorted[0]
    top_genome = population[top_index]

    # Сохраняем лучшего
    save_bot_genome(top_genome, generation, rank=1)

    # Метрики в CSV
    metrics_record = {
        "generation": generation,
        "total_return": top_metrics["total_return"],
        "accuracy": top_metrics["accuracy"],
        "winrate": top_metrics["winrate"],
        "avg_return": top_metrics["avg_return"],
        "n_signals": top_metrics["n_signals"],
        "bot": top_metrics["bot"].describe() if hasattr(top_metrics["bot"], "describe") else str(top_metrics["bot"]),
    }
    append_metrics_csv(metrics_record)

    # Лог в JSON
    log_generation_info(generation, {
        "top_bot_id": top_genome.id,
        "top_return": top_metrics["total_return"],
        "top_accuracy": top_metrics["accuracy"],
        "top_bot_description": top_genome.describe(),
    })

    return survivors, [r for _, r in results_sorted]

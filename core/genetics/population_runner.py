import random
from core.genetics.gene_pool import random_genome
from core.genetics.genetic_ops import mutate_genome, crossover_genomes
from core.genetics.genome import Genome
from core.evaluator import evaluate_bots


def run_generation(df, previous_genomes=None, population_size=50, elite_frac=0.2, mutation_rate=0.3):
    """
    Запускает одну волну эволюции:
    - генерирует популяцию
    - проводит бэктест
    - возвращает топовых выживших
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

    # 6. Отдаём лучшие геномы
    survivors = [population[i] for i in [results.index(r) for r in results_sorted[:population_size]]]

    return survivors, results_sorted

import random
from copy import deepcopy
from core.genetics.genome import Genome
from core.genetics.gene_pool import GENE_POOL


def mutate_genome(genome: Genome, mutation_rate=0.2) -> Genome:
    """Слегка изменяет один или несколько параметров"""
    strategy_type = genome.strategy_type
    params = deepcopy(genome.params)

    param_funcs = GENE_POOL[strategy_type]
    for key in params:
        if random.random() < mutation_rate:
            params[key] = param_funcs[key]()  # Новое случайное значение

    # SMA: гарантируем fast < slow
    if strategy_type == "SmaCrossBot":
        params["fast"] = min(params["fast"], params["slow"] - 1)

    return Genome(strategy_type=strategy_type, params=params)


def crossover_genomes(g1: Genome, g2: Genome) -> Genome:
    """Создаёт нового генома, миксуя параметры родителей (если тип совпадает)"""
    if g1.strategy_type != g2.strategy_type:
        # Несовместимы — выберем случайно одного из родителей
        return random.choice([g1, g2])

    strategy_type = g1.strategy_type
    params = {}

    for k in g1.params:
        v1 = g1.params[k]
        v2 = g2.params[k]
        if isinstance(v1, (int, float)):
            # Среднее с шумом
            base = (v1 + v2) / 2
            noise = (v1 - v2) * random.uniform(-0.3, 0.3)
            params[k] = base + noise
        elif isinstance(v1, bool):
            params[k] = random.choice([v1, v2])
        else:
            params[k] = random.choice([v1, v2])

    # Спец. обработка SMA
    if strategy_type == "SmaCrossBot":
        params["fast"] = min(int(params["fast"]), int(params["slow"]) - 1)

    return Genome(strategy_type=strategy_type, params=params)

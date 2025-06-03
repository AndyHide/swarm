import random
from copy import deepcopy
from core.genetics.genome import Genome
from core.genetics.gene_pool import GENE_POOL


def mutate_genome(genome: Genome, mutation_rate: float = 0.2) -> Genome:
    new_params = deepcopy(genome.params)

    for key in new_params:
        if isinstance(new_params[key], (int, float)) and random.random() < mutation_rate:
            # Случайная мутация: добавим шум ±10%
            factor = random.uniform(0.9, 1.1)
            new_params[key] = type(new_params[key])(new_params[key] * factor)

        elif isinstance(new_params[key], bool) and random.random() < mutation_rate:
            new_params[key] = not new_params[key]

    return Genome(
        strategy_type=genome.strategy_type,
        params=new_params,
        parent_ids=[genome.id]
    )


def crossover_genomes(g1: Genome, g2: Genome) -> Genome:
    if g1.strategy_type != g2.strategy_type:
        return random.choice([g1, g2])  # несовместимые — выбираем случайно

    params = {}
    for key in g1.params:
        if key in g2.params:
            params[key] = random.choice([g1.params[key], g2.params[key]])
        else:
            params[key] = g1.params[key]

    return Genome(
        strategy_type=g1.strategy_type,
        params=params,
        parent_ids=[g1.id, g2.id]
    )

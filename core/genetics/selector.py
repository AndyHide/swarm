import random
from core.genetics.genetic_ops import mutate_genome, crossover_genomes
from core.genetics.gene_pool import random_genome

def select_next_generation(
    previous_genomes: list,
    population_size: int,
    elite_frac: float = 0.2,
    mutation_rate: float = 0.3,
    new_blood_frac: float = 0.1,
) -> list:
    """
    Формирует новое поколение:
    - элита копируется
    - мутанты от элиты
    - кроссоверы элиты
    - свежая кровь: случайные геномы
    """
    new_population = []

    elites_n = max(1, int(population_size * elite_frac))
    new_blood_n = max(1, int(population_size * new_blood_frac))

    elites = previous_genomes[:elites_n]
    new_population.extend(elites)

    # Мутации
    mutants = [mutate_genome(g, mutation_rate) for g in elites]
    new_population.extend(mutants)

    # Кроссоверы
    while len(new_population) < (population_size - new_blood_n):
        parent1, parent2 = random.choices(elites, k=2)
        child = crossover_genomes(parent1, parent2)
        new_population.append(child)

    # Свежая кровь
    fresh = [random_genome() for _ in range(population_size - len(new_population))]
    new_population.extend(fresh)

    return new_population

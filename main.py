from core.genetics.gene_pool import random_genome
from core.genetics.genetic_ops import mutate_genome, crossover_genomes

g1 = random_genome()
g2 = random_genome()

print("Parent A:", g1.describe())
print("Parent B:", g2.describe())

child = crossover_genomes(g1, g2)
mutant = mutate_genome(g1)

print("Child:", child.describe())
print("Mutant:", mutant.describe())

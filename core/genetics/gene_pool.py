import random
from typing import Dict, Any, Callable
from core.genetics.genome import Genome

# Конфигурация стратегий и допустимых параметров
GENE_POOL: Dict[str, Dict[str, Callable[[], Any]]] = {
    "RSIBot": {
        "threshold": lambda: random.uniform(15, 50),
    },
    "RSIBotStochastic": {
        "threshold": lambda: random.uniform(15, 50),
        "randomness": lambda: random.uniform(0.0, 0.3),
    },
    "MACDBot": {
        "zero_cross": lambda: random.choice([True, False]),
    },
    "SmaCrossBot": {
        "fast": lambda: random.randint(5, 50),
        "slow": lambda: random.randint(20, 200),
    },
    "RSIMACDComboBot": {
        "rsi_th": lambda: random.uniform(15, 50),
    },
}


def random_genome() -> Genome:
    strategy_type = random.choice(list(GENE_POOL.keys()))
    param_funcs = GENE_POOL[strategy_type]
    params = {k: f() for k, f in param_funcs.items()}

    # Спец-ограничение для SMA: fast < slow
    if strategy_type == "SmaCrossBot":
        params["fast"] = min(params["fast"], params["slow"] - 1)

    return Genome(strategy_type=strategy_type, params=params)

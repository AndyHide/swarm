import random
from typing import Dict, Any, Callable
from core.genetics.genome import Genome
from core.bots.simple import random_bot_params

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


def random_genome():
    bot = random_bot_params()
    return Genome(strategy_type=bot["strategy_type"], params=bot["params"])

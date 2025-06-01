from dataclasses import dataclass
from typing import Dict, Any, Type
from core.bots.simple import *


@dataclass
class Genome:
    strategy_type: str
    params: Dict[str, Any]

    def create_bot(self) -> TraderBot:
        """Создаёт бота из генома"""
        strategy_map: Dict[str, Type[TraderBot]] = {
            "RSIBot": RSIBot,
            "RSIBotStochastic": RSIBotStochastic,
            "MACDBot": MACDBot,
            "SmaCrossBot": SmaCrossBot,
            "RSIMACDComboBot": RSIMACDComboBot,
        }
        bot_class = strategy_map[self.strategy_type]
        return bot_class(**self.params)

    def describe(self) -> str:
        return f"{self.strategy_type}({self.params})"

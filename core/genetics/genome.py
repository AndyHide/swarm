from dataclasses import dataclass
from typing import Dict, Any, Type, List
from core.bots.simple import *
import uuid
from datetime import datetime


@dataclass
class Genome:
    strategy_type: str
    params: Dict[str, Any]
    id: str
    created_at: str
    age: int
    role: str
    lifespan: int
    parent_ids: List[str]

    def __init__(
        self,
        strategy_type: str,
        params: Dict[str, Any],
        id: str = None,
        created_at: str = None,
        age: int = 0,
        role: str = "neutral",
        lifespan: int = 20,
        parent_ids: List[str] = None,
    ):
        self.strategy_type = strategy_type
        self.params = params
        self.id = id or f"GENOME-{uuid.uuid4().hex[:6].upper()}"
        self.created_at = created_at or datetime.utcnow().isoformat()
        self.age = age
        self.role = role
        self.lifespan = lifespan
        self.parent_ids = parent_ids or []

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

    def to_dict(self) -> Dict[str, Any]:
        return {
            "strategy_type": self.strategy_type,
            "params": self.params,
            "id": self.id,
            "created_at": self.created_at,
            "age": self.age,
            "role": self.role,
            "lifespan": self.lifespan,
            "parent_ids": self.parent_ids,
        }

    @staticmethod
    def from_dict(data: Dict[str, Any]) -> "Genome":
        return Genome(
            strategy_type=data["strategy_type"],
            params=data["params"],
            id=data.get("id"),
            created_at=data.get("created_at"),
            age=data.get("age", 0),
            role=data.get("role", "neutral"),
            lifespan=data.get("lifespan", 20),
            parent_ids=data.get("parent_ids", []),
        )

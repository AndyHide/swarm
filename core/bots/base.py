from abc import ABC, abstractmethod
import pandas as pd


class TraderBot(ABC):
    @abstractmethod
    def signal(self, row: pd.Series) -> int:
        """Выдаёт торговый сигнал: -1 (short), 0 (hold), 1 (long)"""
        pass

    def backtest(self, df: pd.DataFrame, target_col="target") -> dict:
        from core.backtester import backtest_signals
        return backtest_signals(df, self.signal, target_col)

    def describe(self) -> str:
        """Человеко-понятное описание стратегии"""
        return self.__class__.__name__

    def get_params(self) -> dict:
        """Словарь параметров стратегии — основа генетики"""
        return {}

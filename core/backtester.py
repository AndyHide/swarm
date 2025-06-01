import pandas as pd
from typing import Callable


def backtest_signals(
    df: pd.DataFrame,
    signal_func: Callable[[pd.Series], int],
    target_col: str = "target",
    verbose: bool = True
) -> dict:
    """
    Простейший бэктест сигнальной функции на исторических данных с таргетом.
    """
    trades = []
    returns = []

    for _, row in df.iterrows():
        signal = signal_func(row)
        target = row[target_col]
        future_return = row.get("future_return", None)

        # Запись трейда
        if signal != 0:
            is_correct = int(signal == target)
            trades.append((signal, target, is_correct))

            if future_return is not None:
                returns.append(signal * future_return)

    n = len(trades)
    correct = sum(t[2] for t in trades)
    acc = correct / n if n > 0 else 0
    avg_return = sum(returns) / len(returns) if returns else 0
    total_return = sum(returns) if returns else 0
    winrate = sum(1 for r in returns if r > 0) / len(returns) if returns else 0

    if verbose:
        print(f"Всего сделок: {n}")
        print(f"Точность: {acc:.2%}")
        print(f"Доходность: {total_return:.2%}")
        print(f"Средняя на сделку: {avg_return:.4%}")
        print(f"Winrate: {winrate:.2%}")

    return {
        "n_signals": n,
        "accuracy": acc,
        "avg_return": avg_return,
        "total_return": total_return,
        "winrate": winrate,
    }
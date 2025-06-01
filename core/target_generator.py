import pandas as pd


def generate_classification_target(
    df: pd.DataFrame,
    horizon: int = 10,
    threshold: float = 0.002,
    column: str = "close",
    target_col: str = "target"
) -> pd.DataFrame:
    """
    Добавляет колонку target:
    1 = рост выше threshold через horizon свечей,
    -1 = падение ниже -threshold,
    0 = внутри диапазона.
    """
    df = df.copy()
    future_return = (df[column].shift(-horizon) - df[column]) / df[column]

    df[target_col] = 0
    df.loc[future_return > threshold, target_col] = 1
    df.loc[future_return < -threshold, target_col] = -1

    df.dropna(inplace=True)
    return df

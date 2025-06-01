def evaluate_bots(df, bots, sort_by="total_return"):
    results = []
    for bot in bots:
        metrics = bot.backtest(df)
        metrics["bot"] = bot.describe()
        results.append(metrics)
    return sorted(results, key=lambda x: x[sort_by], reverse=True)

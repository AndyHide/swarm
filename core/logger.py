import os
import json
import csv
from datetime import datetime

# Папки
LOG_DIR = "logs"
BEST_BOTS_DIR = "best_bots"

# Файлы
EVOLUTION_LOG = os.path.join(LOG_DIR, "evolution_log.json")
METRICS_CSV = os.path.join(LOG_DIR, "metrics.csv")

# Убедимся, что директории существуют
os.makedirs(LOG_DIR, exist_ok=True)
os.makedirs(BEST_BOTS_DIR, exist_ok=True)


def log_generation_info(generation: int, info: dict):
    """
    Добавляет информацию о поколении в evolution_log.json
    """
    entry = {
        "generation": generation,
        "timestamp": datetime.utcnow().isoformat(),
        **info
    }

    if os.path.exists(EVOLUTION_LOG):
        with open(EVOLUTION_LOG, "r") as f:
            data = json.load(f)
    else:
        data = []

    data.append(entry)

    with open(EVOLUTION_LOG, "w") as f:
        json.dump(data, f, indent=2)


def save_bot_genome(genome, generation: int, rank: int):
    """
    Сохраняет геном в JSON-файл
    """
    filename = f"generation_{generation:03d}_bot_{rank}.json"
    path = os.path.join(BEST_BOTS_DIR, filename)
    with open(path, "w") as f:
        json.dump(genome.to_dict(), f, indent=2)


def append_metrics_csv(metrics: dict):
    """
    Добавляет строку в CSV-файл с метриками поколений
    """
    file_exists = os.path.exists(METRICS_CSV)

    with open(METRICS_CSV, "a", newline="") as csvfile:
        writer = csv.DictWriter(csvfile, fieldnames=metrics.keys())
        if not file_exists:
            writer.writeheader()
        writer.writerow(metrics)

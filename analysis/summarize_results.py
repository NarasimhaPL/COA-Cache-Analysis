
import csv
from pathlib import Path
from collections import defaultdict

PROJECT_ROOT = Path(__file__).resolve().parent.parent
RESULTS_FILE = PROJECT_ROOT / "results" / "trace_experiment_results.csv"

data = defaultdict(list)

with open(RESULTS_FILE, "r", newline="") as file:
    reader = csv.DictReader(file)

    for row in reader:
        key = (int(row["cache_size"]), row["policy"])
        data[key].append(float(row["hit_ratio"]))

print("\nAVERAGE HIT RATIO BY CACHE SIZE AND POLICY")
print("-" * 65)

for cache_size in [128, 256, 512]:
    print(f"\nCache Capacity: {cache_size} bytes")

    rankings = []

    for policy in ["FIFO", "LRU", "LFU", "MRU", "Random", "Clock"]:
        values = data[(cache_size, policy)]
        average = sum(values) / len(values)
        rankings.append((policy, average))

    rankings.sort(key=lambda item: item[1], reverse=True)

    for policy, average in rankings:
        print(f"{policy:10} Average Hit Ratio: {average:.2f}%")

    print(
        f"Best average policy: {rankings[0][0]} "
        f"({rankings[0][1]:.2f}%)"
    )

print("\nSUMMARY GENERATED SUCCESSFULLY")

'''
py -m streamlit run dashboard/app.py
'''
import csv
from pathlib import Path
from collections import defaultdict

import matplotlib.pyplot as plt


PROJECT_ROOT = Path(__file__).resolve().parent.parent
RESULTS_FILE = PROJECT_ROOT / "results" / "trace_experiment_results.csv"
OUTPUT_DIR = PROJECT_ROOT / "results"

CACHE_SIZES = [128, 256, 512]

POLICIES = [
    "FIFO",
    "LRU",
    "LFU",
    "MRU",
    "Random",
    "Clock",
]

WORKLOADS = [
    "Array",
    "Matrix Row-Major",
    "Matrix Column-Major",
    "Random Array",
    "Repeated Loop",
    "Multiple Arrays",
]


def read_results():
    results = []

    with open(RESULTS_FILE, "r", newline="") as file:
        reader = csv.DictReader(file)

        for row in reader:
            row["cache_size"] = int(row["cache_size"])
            row["hit_ratio"] = float(row["hit_ratio"])
            row["miss_ratio"] = float(row["miss_ratio"])
            row["evictions"] = int(row["evictions"])
            row["writebacks"] = int(row["writebacks"])
            results.append(row)

    return results


def plot_metric(results, cache_size, metric, ylabel, title, filename):
    filtered = [
        row for row in results
        if row["cache_size"] == cache_size
    ]

    values = defaultdict(dict)

    for row in filtered:
        values[row["workload"]][row["policy"]] = row[metric]

    x_positions = list(range(len(WORKLOADS)))
    bar_width = 0.12

    plt.figure(figsize=(14, 7))

    for policy_index, policy in enumerate(POLICIES):
        offsets = [
            x + (policy_index - (len(POLICIES) - 1) / 2) * bar_width
            for x in x_positions
        ]

        policy_values = [
            values[workload].get(policy, 0)
            for workload in WORKLOADS
        ]

        plt.bar(
            offsets,
            policy_values,
            width=bar_width,
            label=policy
        )

    plt.xticks(x_positions, WORKLOADS, rotation=20, ha="right")
    plt.xlabel("Workload")
    plt.ylabel(ylabel)
    plt.title(f"{title} - {cache_size} B Cache")
    plt.legend(title="Replacement Policy")
    plt.grid(axis="y", linestyle="--", alpha=0.4)
    plt.tight_layout()

    output_path = OUTPUT_DIR / filename
    plt.savefig(output_path, dpi=300)
    plt.close()

    print(f"Saved: {output_path}")


def plot_capacity_comparison(results):
    averages = defaultdict(dict)

    for cache_size in CACHE_SIZES:
        for policy in POLICIES:
            policy_rows = [
                row for row in results
                if row["cache_size"] == cache_size
                and row["policy"] == policy
            ]

            if policy_rows:
                average = sum(
                    row["hit_ratio"] for row in policy_rows
                ) / len(policy_rows)

                averages[policy][cache_size] = average

    plt.figure(figsize=(10, 6))

    for policy in POLICIES:
        values = [
            averages[policy].get(cache_size, 0)
            for cache_size in CACHE_SIZES
        ]

        plt.plot(
            CACHE_SIZES,
            values,
            marker="o",
            label=policy
        )

    plt.xlabel("Cache Capacity (bytes)")
    plt.ylabel("Average Hit Ratio (%)")
    plt.title("Average Hit Ratio Across Cache Capacities")
    plt.xticks(CACHE_SIZES)
    plt.legend(title="Replacement Policy")
    plt.grid(True, linestyle="--", alpha=0.4)
    plt.tight_layout()

    output_path = OUTPUT_DIR / "cache_capacity_hit_ratio_comparison.png"
    plt.savefig(output_path, dpi=300)
    plt.close()

    print(f"Saved: {output_path}")


def main():
    print("Generating cache experiment graphs...\n")

    results = read_results()

    print(f"Loaded {len(results)} experiment records.")

    for cache_size in CACHE_SIZES:
        plot_metric(
            results,
            cache_size,
            "hit_ratio",
            "Hit Ratio (%)",
            "Hit Ratio Comparison",
            f"trace_hit_ratio_{cache_size}B.png"
        )

        plot_metric(
            results,
            cache_size,
            "miss_ratio",
            "Miss Ratio (%)",
            "Miss Ratio Comparison",
            f"trace_miss_ratio_{cache_size}B.png"
        )

        plot_metric(
            results,
            cache_size,
            "evictions",
            "Number of Evictions",
            "Eviction Comparison",
            f"trace_evictions_{cache_size}B.png"
        )

        plot_metric(
            results,
            cache_size,
            "writebacks",
            "Number of Writebacks",
            "Writeback Comparison",
            f"trace_writebacks_{cache_size}B.png"
        )

    plot_capacity_comparison(results)

    print("\nAll graphs generated successfully!")


if __name__ == "__main__":
    main()
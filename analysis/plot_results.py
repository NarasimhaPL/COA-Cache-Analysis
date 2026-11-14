
import csv
from pathlib import Path

import matplotlib.pyplot as plt


def load_results(csv_path):

    with open(csv_path, "r", newline="") as file:
        reader = csv.DictReader(file)
        return list(reader)


def plot_hit_ratio(results, output_dir):

    policies = [row["Policy"] for row in results]
    hit_ratios = [float(row["Hit Ratio (%)"]) for row in results]

    plt.figure(figsize=(9, 5))
    bars = plt.bar(policies, hit_ratios)

    plt.title("Cache Replacement Policies - Hit Ratio")
    plt.xlabel("Replacement Policy")
    plt.ylabel("Hit Ratio (%)")
    plt.ylim(0, 100)
    plt.grid(axis="y", linestyle="--", alpha=0.4)

    for bar, value in zip(bars, hit_ratios):
        plt.text(
            bar.get_x() + bar.get_width() / 2,
            bar.get_height() + 1,
            f"{value:.1f}%",
            ha="center"
        )

    plt.tight_layout()
    plt.savefig(output_dir / "hit_ratio_comparison.png", dpi=300)
    plt.close()


def plot_miss_ratio(results, output_dir):

    policies = [row["Policy"] for row in results]
    miss_ratios = [float(row["Miss Ratio (%)"]) for row in results]

    plt.figure(figsize=(9, 5))
    bars = plt.bar(policies, miss_ratios)

    plt.title("Cache Replacement Policies - Miss Ratio")
    plt.xlabel("Replacement Policy")
    plt.ylabel("Miss Ratio (%)")
    plt.ylim(0, 100)
    plt.grid(axis="y", linestyle="--", alpha=0.4)

    for bar, value in zip(bars, miss_ratios):
        plt.text(
            bar.get_x() + bar.get_width() / 2,
            bar.get_height() + 1,
            f"{value:.1f}%",
            ha="center"
        )

    plt.tight_layout()
    plt.savefig(output_dir / "miss_ratio_comparison.png", dpi=300)
    plt.close()


def plot_evictions_writebacks(results, output_dir):

    policies = [row["Policy"] for row in results]
    evictions = [int(row["Evictions"]) for row in results]
    writebacks = [int(row["Writebacks"]) for row in results]

    positions = list(range(len(policies)))
    width = 0.35

    plt.figure(figsize=(10, 5))

    eviction_bars = plt.bar(
        [position - width / 2 for position in positions],
        evictions,
        width,
        label="Evictions"
    )

    writeback_bars = plt.bar(
        [position + width / 2 for position in positions],
        writebacks,
        width,
        label="Writebacks"
    )

    plt.title("Cache Replacement Policies - Evictions and Writebacks")
    plt.xlabel("Replacement Policy")
    plt.ylabel("Count")
    plt.xticks(positions, policies)
    plt.legend()
    plt.grid(axis="y", linestyle="--", alpha=0.4)

    for bars in (eviction_bars, writeback_bars):
        for bar in bars:
            plt.text(
                bar.get_x() + bar.get_width() / 2,
                bar.get_height() + 0.05,
                str(int(bar.get_height())),
                ha="center"
            )

    plt.tight_layout()
    plt.savefig(output_dir / "evictions_writebacks_comparison.png", dpi=300)
    plt.close()


def main():

    project_root = Path(__file__).resolve().parents[1]
    results_dir = project_root / "results"
    csv_path = results_dir / "policy_comparison.csv"

    if not csv_path.exists():
        raise FileNotFoundError(
            f"Results CSV not found: {csv_path}\n"
            "Run the experiment runner first."
        )

    results = load_results(csv_path)

    if not results:
        raise ValueError("The results CSV is empty.")

    plot_hit_ratio(results, results_dir)
    plot_miss_ratio(results, results_dir)
    plot_evictions_writebacks(results, results_dir)

    print("All comparison graphs generated successfully!")

    print(f"Graphs saved in: {results_dir}")


if __name__ == "__main__":
    main()

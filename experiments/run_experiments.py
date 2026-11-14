
import csv
import random
from pathlib import Path

from cache_simulator.cache import Cache
from cache_simulator.policies.fifo import FIFOPolicy
from cache_simulator.policies.lru import LRUPolicy
from cache_simulator.policies.lfu import LFUPolicy
from cache_simulator.policies.mru import MRUPolicy
from cache_simulator.policies.random_policy import RandomPolicy
from cache_simulator.policies.clock import ClockPolicy


memory_trace = [
    (0, "READ"),
    (16, "READ"),
    (32, "READ"),
    (48, "WRITE"),
    (0, "READ"),
    (64, "READ"),
    (16, "WRITE"),
    (80, "READ"),
    (32, "READ"),
    (96, "WRITE"),
    (0, "READ"),
    (112, "READ"),
    (48, "READ"),
    (128, "WRITE"),
    (16, "READ"),
    (64, "READ"),
    (144, "READ"),
    (0, "WRITE"),
    (32, "READ"),
    (160, "READ"),
]

policies = {
    "FIFO": FIFOPolicy,
    "LRU": LRUPolicy,
    "LFU": LFUPolicy,
    "MRU": MRUPolicy,
    "Random": RandomPolicy,
    "Clock": ClockPolicy,
}


def run_experiment(policy_name, policy_class):

    random.seed(42)

    cache = Cache(
        cache_size=128,
        block_size=16,
        associativity=2,
        replacement_policy=policy_class()
    )

    for address, operation in memory_trace:
        cache.access(address, operation)

    stats = cache.get_statistics()

    return {
        "Policy": policy_name,
        "Total Accesses": stats["total_accesses"],
        "Hits": stats["hits"],
        "Misses": stats["misses"],
        "Hit Ratio (%)": stats["hit_ratio"],
        "Miss Ratio (%)": stats["miss_ratio"],
        "Evictions": stats["evictions"],
        "Writebacks": stats["writebacks"],
    }


def main():

    results = []

    print("\nRunning cache replacement experiments...\n")

    for policy_name, policy_class in policies.items():

        result = run_experiment(policy_name, policy_class)
        results.append(result)

        print(
            f"{policy_name}: "
            f"Hit Ratio = {result['Hit Ratio (%)']}%, "
            f"Misses = {result['Misses']}"
        )

    project_root = Path(__file__).resolve().parents[1]
    results_directory = project_root / "results"
    results_directory.mkdir(exist_ok=True)

    output_file = results_directory / "policy_comparison.csv"

    # Save results using Python's built-in CSV module.
    with open(output_file, "w", newline="") as file:

        writer = csv.DictWriter(
            file,
            fieldnames=results[0].keys()
        )

        writer.writeheader()
        writer.writerows(results)

    print("\nFinal Comparison:\n")

    headers = list(results[0].keys())

    print(" | ".join(headers))
    print("-" * 110)

    for result in results:
        print(" | ".join(str(result[key]) for key in headers))

    print(f"\nResults saved to: {output_file}")


if __name__ == "__main__":
    main()

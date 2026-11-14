
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


PROJECT_ROOT = Path(__file__).resolve().parent.parent
TRACE_DIR = PROJECT_ROOT / "traces"
RESULTS_DIR = PROJECT_ROOT / "results"

RESULTS_DIR.mkdir(exist_ok=True)

CACHE_SIZES = [128, 256, 512]
BLOCK_SIZE = 16
ASSOCIATIVITY = 2

POLICIES = {
    "FIFO": FIFOPolicy,
    "LRU": LRUPolicy,
    "LFU": LFUPolicy,
    "MRU": MRUPolicy,
    "Random": RandomPolicy,
    "Clock": ClockPolicy,
}

WORKLOADS = {
    "Array": "array_traversal.csv",
    "Matrix Row-Major": "matrix_traversal.csv",
    "Matrix Column-Major": "matrix_column_traversal.csv",
    "Random Array": "random_array_access.csv",
    "Repeated Loop": "repeated_loop_access.csv",
    "Multiple Arrays": "multiple_array_interleaved.csv",
}


def read_trace(filename):
    trace = []
    path = TRACE_DIR / filename

    with open(path, "r", newline="") as file:
        reader = csv.DictReader(file)

        for row in reader:
            address = int(row["address"])
            operation = row["operation"].strip().upper()
            trace.append((address, operation))

    return trace


def run_experiment(trace, policy_class, cache_size):
    random.seed(42)

    cache = Cache(
        cache_size=cache_size,
        block_size=BLOCK_SIZE,
        associativity=ASSOCIATIVITY,
        replacement_policy=policy_class()
    )

    for address, operation in trace:
        cache.access(address, operation)

    return cache.get_statistics()


def main():
    print("Starting cache experiments...")
    print(f"Cache sizes: {CACHE_SIZES}")
    print(f"Block size: {BLOCK_SIZE} bytes")
    print(f"Associativity: {ASSOCIATIVITY}-way\n")

    results = []

    for cache_size in CACHE_SIZES:
        print("=" * 55)
        print(f"CACHE SIZE: {cache_size} BYTES")
        print("=" * 55)

        for workload, filename in WORKLOADS.items():
            print(f"\nWorkload: {workload}")

            trace = read_trace(filename)
            print(f"Memory accesses: {len(trace)}")

            for policy_name, policy_class in POLICIES.items():
                stats = run_experiment(
                    trace,
                    policy_class,
                    cache_size
                )

                result = {
                    "cache_size": cache_size,
                    "workload": workload,
                    "policy": policy_name,
                    **stats
                }

                results.append(result)

                print(
                    f"{policy_name}: "
                    f"Hits={stats['hits']}, "
                    f"Misses={stats['misses']}, "
                    f"Hit Ratio={stats['hit_ratio']:.2f}%"
                )

    output_file = RESULTS_DIR / "trace_experiment_results.csv"

    fieldnames = [
        "cache_size",
        "workload",
        "policy",
        "total_accesses",
        "hits",
        "misses",
        "evictions",
        "writebacks",
        "hit_ratio",
        "miss_ratio",
    ]

    with open(output_file, "w", newline="") as file:
        writer = csv.DictWriter(file, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(results)

    print("\nAll experiments completed!")
    print(f"Total experiments: {len(results)}")
    print(f"Results saved to: {output_file}")


if __name__ == "__main__":
    main()

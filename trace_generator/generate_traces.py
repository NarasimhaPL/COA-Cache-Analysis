
import csv
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parent.parent
TRACE_DIR = PROJECT_ROOT / "traces"

TRACE_DIR.mkdir(exist_ok=True)


def save_trace(filename, accesses):
    output_path = TRACE_DIR / filename

    with open(output_path, "w", newline="") as file:
        writer = csv.writer(file)
        writer.writerow(["address", "operation"])
        writer.writerows(accesses)

    print(f"Generated: {output_path}")
    print(f"Memory accesses: {len(accesses)}")


def generate_array_trace():
    accesses = []
    base_address = 0x1000

    # Array initialization: WRITE operations
    for i in range(1024):
        address = base_address + i * 4
        accesses.append((address, "WRITE"))

    # Array traversal: READ operations
    for i in range(1024):
        address = base_address + i * 4
        accesses.append((address, "READ"))

    save_trace("array_traversal.csv", accesses)


def generate_matrix_trace():
    accesses = []
    base_address = 0x10000

    # Matrix initialization: WRITE operations
    for i in range(64):
        for j in range(64):
            address = base_address + (i * 64 + j) * 4
            accesses.append((address, "WRITE"))

    # Row-major traversal: READ operations
    for i in range(64):
        for j in range(64):
            address = base_address + (i * 64 + j) * 4
            accesses.append((address, "READ"))

    save_trace("matrix_traversal.csv", accesses)

def generate_matrix_column_trace():
    accesses = []
    base_address = 0x10000

    # Matrix initialization
    for i in range(64):
        for j in range(64):
            address = base_address + (i * 64 + j) * 4
            accesses.append((address, "WRITE"))

    # Column-major traversal
    for j in range(64):
        for i in range(64):
            address = base_address + (i * 64 + j) * 4
            accesses.append((address, "READ"))

    save_trace("matrix_column_traversal.csv", accesses)


def generate_random_array_trace():
    import random

    accesses = []
    base_address = 0x20000
    indices = list(range(1024))

    # Reproduce the same shuffled order every time.
    random.seed(42)
    random.shuffle(indices)

    # Array initialization
    for i in range(1024):
        address = base_address + i * 4
        accesses.append((address, "WRITE"))

    # Random-order traversal
    for i in indices:
        address = base_address + i * 4
        accesses.append((address, "READ"))

    save_trace("random_array_access.csv", accesses)


def generate_repeated_loop_trace():
    accesses = []
    base_address = 0x30000

    # Array initialization
    for i in range(64):
        address = base_address + i * 4
        accesses.append((address, "WRITE"))

    # Repeated sequential reads
    for repeat in range(100):
        for i in range(64):
            address = base_address + i * 4
            accesses.append((address, "READ"))

    save_trace("repeated_loop_access.csv", accesses)

def generate_multiple_array_trace():
    accesses = []

    base_A = 0x40000
    base_B = 0x41000
    base_C = 0x42000

    # Initialize all three arrays
    for i in range(64):
        accesses.append((base_A + i * 4, "WRITE"))
        accesses.append((base_B + i * 4, "WRITE"))
        accesses.append((base_C + i * 4, "WRITE"))

    # Interleaved reads
    for i in range(64):
        accesses.append((base_A + i * 4, "READ"))
        accesses.append((base_B + i * 4, "READ"))
        accesses.append((base_C + i * 4, "READ"))

    save_trace("multiple_array_interleaved.csv", accesses)


def main():
    print("Generating memory traces...\n")

    generate_array_trace()
    print()

    generate_matrix_trace()
    print()

    generate_matrix_column_trace()
    print()

    generate_random_array_trace()
    print()

    generate_repeated_loop_trace()
    print()

    generate_multiple_array_trace()

    print("\nTrace generation completed!")

if __name__ == "__main__":
    main()





# Comparative Survey and Performance Analysis of Cache Replacement Policies

## Project Overview

This project implements and evaluates different cache replacement policies to understand their impact on cache performance under different memory access patterns.

The project compares six cache replacement algorithms using six synthetic memory access workloads and three cache capacities.

The main objective is to identify how cache capacity, workload characteristics, and replacement strategies influence cache hit ratio, miss ratio, evictions, and writebacks.

## Objectives

- Implement different cache replacement algorithms.
- Simulate cache memory behavior.
- Generate memory access traces for different workloads.
- Compare replacement policies under identical experimental configurations.
- Analyze cache hits, misses, evictions, and writebacks.
- Visualize experimental results using graphs.
- Develop an interactive Streamlit dashboard for performance analysis.

## Replacement Policies Implemented

The project implements six replacement policies:

| Policy | Description |
|---|---|
| FIFO | First In, First Out. Replaces the block that entered the cache earliest. |
| LRU | Least Recently Used. Replaces the block that has not been accessed for the longest time. |
| LFU | Least Frequently Used. Replaces the block with the lowest access frequency. |
| MRU | Most Recently Used. Replaces the most recently accessed block. |
| Random | Selects a victim block randomly. |
| Clock | Uses a reference-bit-based circular replacement mechanism. |

## Project Architecture

```text
COA-Cache-Analysis/
│
├── workloads/
│
├── trace_generator/
│   ├── __init__.py
│   └── generate_traces.py
│
├── traces/
│
├── cache_simulator/
│   ├── __init__.py
│   ├── cache.py
│   ├── cache_block.py
│   ├── cache_set.py
│   ├── address_mapper.py
│   │
│   └── policies/
│       ├── __init__.py
│       ├── fifo.py
│       ├── lru.py
│       ├── lfu.py
│       ├── mru.py
│       ├── random_policy.py
│       └── clock.py
│
├── experiments/
│   ├── run_experiments.py
│   └── run_trace_experiments.py
│
├── analysis/
│   ├── plot_results.py
│   ├── plot_trace_results.py
│   └── summarize_results.py
│
├── results/
│   ├── trace_experiment_results.csv
│   └── performance graphs
│
├── dashboard/
│   └── app.py
│
├── tests/
│   ├── test_cache.py
│   └── test_policies.py
│
├── requirements.txt
└── README.md
```

## Workloads Used

Six synthetic memory access workloads are used:

| Workload | Description |
|---|---|
| Array Traversal | Sequential access to array elements. |
| Matrix Row-Major | Matrix elements accessed row by row. |
| Matrix Column-Major | Matrix elements accessed column by column. |
| Random Array Access | Array elements accessed in a randomized order. |
| Repeated Loop | Repeated access to a selected sequence of memory locations. |
| Multiple Arrays | Interleaved access to multiple arrays. |

These workloads represent different memory access patterns and help evaluate the behavior of replacement algorithms.

## Experimental Configuration

The experiments use the following configuration:

| Parameter | Value |
|---|---|
| Cache Capacities | 128 B, 256 B, 512 B |
| Block Size | 16 B |
| Associativity | 2-way |
| Replacement Policies | FIFO, LRU, LFU, MRU, Random, Clock |
| Workloads | 6 |
| Total Experiment Records | 108 |

The total number of experiment records is:

3 cache capacities × 6 workloads × 6 replacement policies = 108 records.

## Performance Metrics

The following performance metrics are collected:

### 1. Cache Hit Ratio

Measures the percentage of memory accesses successfully served by the cache.

Hit Ratio = (Cache Hits / Total Accesses) × 100

### 2. Cache Miss Ratio

Measures the percentage of memory accesses that are not found in the cache.

Miss Ratio = (Cache Misses / Total Accesses) × 100

### 3. Evictions

Counts the number of cache blocks removed to accommodate new blocks.

### 4. Writebacks

Counts the number of dirty cache blocks written back to memory during replacement.

## Important Experimental Results

Average hit ratio across the six workloads:

| Cache Capacity | FIFO | LRU | LFU | MRU | Random | Clock |
|---|---:|---:|---:|---:|---:|---:|
| 128 B | 50.20% | 50.21% | 50.26% | 53.63% | 55.06% | 50.20% |
| 256 B | 54.58% | 54.58% | 54.67% | 58.65% | 58.78% | 54.58% |
| 512 B | 54.97% | 54.98% | 55.22% | 63.12% | 60.31% | 54.97% |

### Key Inferences

1. Random replacement achieved the highest average hit ratio at 128 B and 256 B.
2. MRU achieved the highest average hit ratio at 512 B.
3. Increasing cache capacity generally improved average hit ratio.
4. MRU performed particularly well for the repeated-loop workload.
5. The Multiple Arrays workload exposed significant cache conflict behavior.
6. FIFO, LRU, and Clock showed similar average performance in the tested configurations.
7. No single replacement policy performed best for every workload and cache capacity.

These conclusions apply to the specific synthetic workloads and experimental configurations used in this project.

## Graphical Analysis

The `results/` directory contains graphs generated from the experimental dataset.

The graphs cover:

- Hit ratio comparison at 128 B, 256 B, and 512 B.
- Cache capacity versus average hit ratio.
- Miss ratio comparison.
- Cache eviction comparison.
- Cache writeback comparison.

## Interactive Dashboard

An interactive Streamlit dashboard is included to explore the experimental results.

Dashboard features:

- Filter by cache capacity.
- Select individual workloads.
- Compare replacement policies.
- View cache performance metrics.
- Visualize hit ratio and capacity comparisons.
- Explore generated performance graphs.

### Run the Dashboard

```powershell
py -m pip install -r requirements.txt
py -m streamlit run dashboard/app.py
```

The dashboard will be available locally at:

http://localhost:8501

## Installation and Execution

### Prerequisites

- Python 3
- Git
- GCC (only if compiling C components)

### 1. Clone the Repository

```powershell
git clone https://github.com/NarasimhaPL/COA-Cache-Analysis.git
```

### 2. Enter the Project Directory

```powershell
cd COA-Cache-Analysis
```

### 3. Install Dependencies

```powershell
py -m pip install -r requirements.txt
```

### 4. Generate Memory Access Traces

```powershell
py -m trace_generator.generate_traces
```

### 5. Run Cache Experiments

```powershell
py -m experiments.run_trace_experiments
```

### 6. Summarize Results

```powershell
py -m analysis.summarize_results
```

### 7. Generate Performance Graphs

```powershell
py -m analysis.plot_trace_results
```

### 8. Run Unit Tests

```powershell
py -m pytest tests/ -v
```

Previously verified test result: 13 passed.

### 9. Launch the Dashboard

```powershell
py -m streamlit run dashboard/app.py
```

## Testing

Unit tests are provided in the `tests/` directory.

Test files:

- `test_cache.py`
- `test_policies.py`

The previously executed test suite completed successfully with 13 passing tests.

## Technologies Used

- Python
- C (where applicable)
- Streamlit
- Matplotlib
- NumPy
- Pytest
- Git and GitHub

## Limitations

- Experiments use synthetic memory access workloads.
- Only three cache capacities are evaluated.
- Block size and associativity are fixed during the main experiments.
- Results depend on workload characteristics and simulator implementation.
- The experiment results should not be treated as universal rankings for real-world processors.

## Future Enhancements

- Evaluate additional cache replacement algorithms.
- Test different block sizes and associativity levels.
- Introduce real-world memory access traces.
- Evaluate larger cache capacities.
- Analyze execution time and replacement overhead.
- Extend the simulator to model multi-level cache architectures.
- Improve the dashboard with additional performance comparisons.

## Conclusion

This project demonstrates how cache replacement policies influence cache performance under different memory access patterns and cache configurations.

The experimental results show that replacement policy effectiveness depends on workload characteristics and cache capacity. Random replacement performed best on average for the smaller tested cache capacities, while MRU performed best at the largest tested capacity.

The project provides a practical foundation for understanding cache memory management, replacement algorithms, and performance evaluation in Computer Organization and Architecture.

## Author

**Project:** Comparative Survey and Performance Analysis of Cache Replacement Policies

**GitHub Repository:**

https://github.com/NarasimhaPL/COA-Cache-Analysis

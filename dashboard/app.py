
import csv
from pathlib import Path

import matplotlib.pyplot as plt
import streamlit as st


# --------------------------------------------------
# PROJECT PATHS
# --------------------------------------------------

PROJECT_ROOT = Path(__file__).resolve().parent.parent
RESULTS_FILE = PROJECT_ROOT / "results" / "trace_experiment_results.csv"
RESULTS_DIR = PROJECT_ROOT / "results"


# --------------------------------------------------
# PAGE CONFIGURATION
# --------------------------------------------------

st.set_page_config(
    page_title="Cache Replacement Policy Analysis",
    page_icon="💾",
    layout="wide"
)


# --------------------------------------------------
# LOAD EXPERIMENT RESULTS
# --------------------------------------------------

@st.cache_data
def load_results():
    rows = []

    with open(RESULTS_FILE, "r", newline="") as file:
        reader = csv.DictReader(file)

        for row in reader:
            rows.append({
                "cache_size": int(row["cache_size"]),
                "workload": row["workload"],
                "policy": row["policy"],
                "total_accesses": int(row["total_accesses"]),
                "hits": int(row["hits"]),
                "misses": int(row["misses"]),
                "evictions": int(row["evictions"]),
                "writebacks": int(row["writebacks"]),
                "hit_ratio": float(row["hit_ratio"]),
                "miss_ratio": float(row["miss_ratio"]),
            })

    return rows


# --------------------------------------------------
# APPLICATION HEADER
# --------------------------------------------------

st.title("Cache Replacement Policy Analysis")

st.markdown(
    """
    ### Comparative Survey and Performance Analysis of Cache Replacement Policies

    This dashboard compares six cache replacement policies
    across six memory workloads and three cache capacities.
    """
)

st.divider()


# --------------------------------------------------
# CHECK RESULTS FILE
# --------------------------------------------------

if not RESULTS_FILE.exists():
    st.error(
        "Experiment results file not found. "
        "Run the experiment script first."
    )
    st.stop()

results = load_results()

if not results:
    st.error("The experiment results file is empty.")
    st.stop()


# --------------------------------------------------
# SIDEBAR FILTERS
# --------------------------------------------------

cache_sizes = sorted({
    row["cache_size"] for row in results
})

workloads = sorted({
    row["workload"] for row in results
})

policies = [
    "FIFO",
    "LRU",
    "LFU",
    "MRU",
    "Random",
    "Clock"
]

st.sidebar.title("Experiment Filters")

selected_cache = st.sidebar.selectbox(
    "Cache Capacity",
    cache_sizes
)

selected_workload = st.sidebar.selectbox(
    "Workload",
    workloads
)

selected_policy = st.sidebar.selectbox(
    "Replacement Policy",
    policies
)


# --------------------------------------------------
# SELECTED EXPERIMENT
# --------------------------------------------------

filtered = [
    row for row in results
    if row["cache_size"] == selected_cache
    and row["workload"] == selected_workload
    and row["policy"] == selected_policy
]

if not filtered:
    st.warning("No matching experiment result found.")
    st.stop()

result = filtered[0]

st.header("Selected Experiment")

st.write(
    f"**Workload:** {selected_workload}  \n"
    f"**Cache Capacity:** {selected_cache} bytes  \n"
    f"**Replacement Policy:** {selected_policy}"
)

col1, col2, col3, col4 = st.columns(4)

col1.metric(
    "Total Accesses",
    result["total_accesses"]
)

col2.metric(
    "Cache Hits",
    result["hits"]
)

col3.metric(
    "Cache Misses",
    result["misses"]
)

col4.metric(
    "Hit Ratio",
    f'{result["hit_ratio"]:.2f}%'
)

col5, col6, col7 = st.columns(3)

col5.metric(
    "Miss Ratio",
    f'{result["miss_ratio"]:.2f}%'
)

col6.metric(
    "Evictions",
    result["evictions"]
)

col7.metric(
    "Writebacks",
    result["writebacks"]
)

st.divider()


# --------------------------------------------------
# REPLACEMENT POLICY COMPARISON
# --------------------------------------------------

st.header("Replacement Policy Comparison")

comparison = [
    row for row in results
    if row["cache_size"] == selected_cache
    and row["workload"] == selected_workload
]

comparison.sort(
    key=lambda row: policies.index(row["policy"])
)

fig, ax = plt.subplots(figsize=(10, 5))

policy_names = [
    row["policy"] for row in comparison
]

hit_ratios = [
    row["hit_ratio"] for row in comparison
]

ax.bar(policy_names, hit_ratios)

ax.set_xlabel("Replacement Policy")
ax.set_ylabel("Hit Ratio (%)")

ax.set_title(
    f"Policy Comparison - {selected_workload} "
    f"({selected_cache} B Cache)"
)

ax.grid(
    axis="y",
    linestyle="--",
    alpha=0.4
)

fig.tight_layout()

st.pyplot(fig)
plt.close(fig)


# --------------------------------------------------
# POLICY RESULTS TABLE
# --------------------------------------------------

st.subheader("All Policy Results")

table = """
| Policy | Hits | Misses | Hit Ratio (%) | Miss Ratio (%) | Evictions | Writebacks |
|---|---:|---:|---:|---:|---:|---:|
"""

for row in comparison:
    table += (
        f"| {row['policy']} "
        f"| {row['hits']} "
        f"| {row['misses']} "
        f"| {row['hit_ratio']:.2f} "
        f"| {row['miss_ratio']:.2f} "
        f"| {row['evictions']} "
        f"| {row['writebacks']} |\n"
    )

st.markdown(table)

st.divider()


# --------------------------------------------------
# CACHE CAPACITY COMPARISON
# --------------------------------------------------

st.header("Cache Capacity Comparison")

capacity_comparison = [
    row for row in results
    if row["workload"] == selected_workload
    and row["policy"] == selected_policy
]

capacity_comparison.sort(
    key=lambda row: row["cache_size"]
)

fig, ax = plt.subplots(figsize=(10, 5))

capacities = [
    row["cache_size"]
    for row in capacity_comparison
]

capacity_hit_ratios = [
    row["hit_ratio"]
    for row in capacity_comparison
]

ax.plot(
    capacities,
    capacity_hit_ratios,
    marker="o",
    linewidth=2
)

ax.set_xlabel("Cache Capacity (bytes)")
ax.set_ylabel("Hit Ratio (%)")

ax.set_title(
    f"Cache Capacity vs Hit Ratio - "
    f"{selected_workload} ({selected_policy})"
)

ax.set_xticks(capacities)

ax.grid(
    True,
    linestyle="--",
    alpha=0.4
)

fig.tight_layout()

st.pyplot(fig)
plt.close(fig)

st.divider()


# --------------------------------------------------
# GENERATED EXPERIMENT GRAPHS
# --------------------------------------------------

st.header("Generated Experiment Graphs")

graph_files = [
    "trace_hit_ratio_128B.png",
    "trace_miss_ratio_128B.png",
    "trace_evictions_128B.png",
    "trace_writebacks_128B.png",

    "trace_hit_ratio_256B.png",
    "trace_miss_ratio_256B.png",
    "trace_evictions_256B.png",
    "trace_writebacks_256B.png",

    "trace_hit_ratio_512B.png",
    "trace_miss_ratio_512B.png",
    "trace_evictions_512B.png",
    "trace_writebacks_512B.png",

    "cache_capacity_hit_ratio_comparison.png",
]

for graph in graph_files:
    graph_path = RESULTS_DIR / graph

    if graph_path.exists():
        st.subheader(
            graph.replace("_", " ").replace(".png", "")
        )

        st.image(
            str(graph_path),
            use_container_width=True
        )


# --------------------------------------------------
# PROJECT INFORMATION
# --------------------------------------------------

st.divider()

st.header("Project Information")

st.write(
    """
    **Project:** Comparative Survey and Performance Analysis
    of Cache Replacement Policies

    **Replacement Policies:** FIFO, LRU, LFU, MRU, Random and Clock

    **Workloads:** Array, Matrix Row-Major, Matrix Column-Major,
    Random Array, Repeated Loop and Multiple Arrays

    **Cache Capacities:** 128 B, 256 B and 512 B

    **Block Size:** 16 bytes

    **Associativity:** 2-way

    **Total Experiments:** 108
    """
)

st.caption(
    "Academic COA Project | Cache Memory Performance Analysis"
)

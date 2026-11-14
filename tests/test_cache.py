
from cache_simulator.cache import Cache
import pytest

from cache_simulator.policies.fifo import FIFOPolicy
from cache_simulator.policies.lru import LRUPolicy
from cache_simulator.policies.lfu import LFUPolicy
from cache_simulator.policies.mru import MRUPolicy
from cache_simulator.policies.random_policy import RandomPolicy
from cache_simulator.policies.clock import ClockPolicy

def test_cache():
    cache = Cache(
        cache_size=128,
        block_size=16,
        associativity=2
    )

    addresses = [
        0, 16, 32, 0, 16,
        64, 80, 0, 32, 96
    ]

    for address in addresses:
        cache.access(address)

    stats = cache.get_statistics()

    print("\nFinal Statistics:")
    for key, value in stats.items():
        print(f"{key}: {value}")

    assert stats["hits"] == 4
    assert stats["misses"] == 6



@pytest.mark.parametrize(
    "policy",
    [
        FIFOPolicy(),
        LRUPolicy(),
        LFUPolicy(),
        MRUPolicy(),
        RandomPolicy(),
        ClockPolicy()
    ],
    ids=["FIFO", "LRU", "LFU", "MRU", "Random", "Clock"]
)
def test_cache_with_all_replacement_policies(policy):

    cache = Cache(
        cache_size=32,
        block_size=16,
        associativity=2,
        replacement_policy=policy
    )

    # Access a sequence of memory addresses.
    addresses = [0, 16, 32, 48, 0, 32, 64, 16]

    for address in addresses:
        result = cache.access(address)
        assert result in ("HIT", "MISS")

    stats = cache.get_statistics()

    # Verify performance counters.
    assert stats["total_accesses"] == len(addresses)
    assert stats["hits"] + stats["misses"] == len(addresses)

    # Verify that cache evictions occurred.
    assert stats["evictions"] > 0

    # Verify that all cache blocks remain valid.
    for cache_set in cache.sets:
        for block in cache_set.blocks:
            assert block.valid


from cache_simulator.cache_block import CacheBlock
from cache_simulator.policies.fifo import FIFOPolicy


def test_fifo_selects_oldest_block():
    block_a = CacheBlock()
    block_b = CacheBlock()
    block_c = CacheBlock()

    block_a.inserted_at = 1
    block_b.inserted_at = 2
    block_c.inserted_at = 3

    policy = FIFOPolicy()

    victim = policy.choose_victim([
        block_a,
        block_b,
        block_c
    ])

    assert victim is block_a


from cache_simulator.policies.lru import LRUPolicy


def test_lru_selects_least_recently_used_block():

    block_a = CacheBlock()
    block_b = CacheBlock()
    block_c = CacheBlock()

    block_a.last_accessed = 5
    block_b.last_accessed = 12
    block_c.last_accessed = 8

    policy = LRUPolicy()

    victim = policy.choose_victim([
        block_a,
        block_b,
        block_c
    ])

    assert victim is block_a


from cache_simulator.policies.lfu import LFUPolicy


def test_lfu_selects_least_frequently_used_block():

    block_a = CacheBlock()
    block_b = CacheBlock()
    block_c = CacheBlock()

    block_a.frequency = 2
    block_b.frequency = 7
    block_c.frequency = 4

    block_a.inserted_at = 1
    block_b.inserted_at = 2
    block_c.inserted_at = 3

    policy = LFUPolicy()

    victim = policy.choose_victim([
        block_a,
        block_b,
        block_c
    ])

    assert victim is block_a


from cache_simulator.policies.mru import MRUPolicy


def test_mru_selects_most_recently_used_block():

    block_a = CacheBlock()
    block_b = CacheBlock()
    block_c = CacheBlock()

    block_a.last_accessed = 5
    block_b.last_accessed = 12
    block_c.last_accessed = 8

    policy = MRUPolicy()

    victim = policy.choose_victim([
        block_a,
        block_b,
        block_c
    ])

    assert victim is block_b



from cache_simulator.policies.random_policy import RandomPolicy


def test_random_selects_a_valid_block():

    block_a = CacheBlock()
    block_b = CacheBlock()
    block_c = CacheBlock()

    blocks = [block_a, block_b, block_c]

    policy = RandomPolicy()

    victim = policy.choose_victim(blocks)

    assert victim in blocks



from cache_simulator.policies.clock import ClockPolicy



def test_clock_selects_block_with_zero_reference_bit():

    block_a = CacheBlock()
    block_b = CacheBlock()
    block_c = CacheBlock()

    # Mark all blocks as valid.
    block_a.valid = True
    block_b.valid = True
    block_c.valid = True

    block_a.reference_bit = 1
    block_b.reference_bit = 0
    block_c.reference_bit = 1

    blocks = [block_a, block_b, block_c]

    policy = ClockPolicy()

    victim = policy.choose_victim(blocks)

    assert victim == block_b
    assert block_a.reference_bit == 0
    assert block_c.reference_bit == 1

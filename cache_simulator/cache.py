
from .address_mapper import AddressMapper
from .cache_set import CacheSet
from .policies.fifo import FIFOPolicy


class Cache:

    def __init__(
        self,
        cache_size,
        block_size,
        associativity,
        replacement_policy=None
    ):

        self.mapper = AddressMapper(
            cache_size,
            block_size,
            associativity
        )

        self.sets = [
            CacheSet(associativity)
            for _ in range(self.mapper.number_of_sets)
        ]

        self.timestamp = 0

        # Default replacement policy: FIFO
        self.replacement_policy = (
            replacement_policy
            if replacement_policy is not None
            else FIFOPolicy()
        )

        # Performance counters
        self.hits = 0
        self.misses = 0
        self.evictions = 0
        self.writebacks = 0

    def access(self, address, operation="READ"):

        operation = operation.upper()

        if operation not in ("READ", "WRITE"):
            raise ValueError("Operation must be READ or WRITE")

        self.timestamp += 1

        mapped = self.mapper.map_address(address)

        set_index = mapped["set_index"]
        tag = mapped["tag"]

        cache_set = self.sets[set_index]

        # Check whether block is already present
        way = cache_set.find_block(tag)

        if way is not None:

            self.hits += 1

            block = cache_set.blocks[way]

            block.access(
                self.timestamp,
                operation
            )

            return "HIT"

        # Cache miss
        self.misses += 1

        # Look for an empty block
        way = cache_set.find_empty_block()

        if way is None:

            # Ask selected policy to choose a victim
            if self.replacement_policy.__class__.__name__ == "ClockPolicy":

                victim = self.replacement_policy.choose_victim(
                cache_set.blocks,
                set_index
            )

            else:

                valid_blocks = cache_set.get_valid_blocks()

                victim = self.replacement_policy.choose_victim(
                    valid_blocks
                )

            way = cache_set.blocks.index(victim)

            self.evictions += 1

            if victim.dirty:
                self.writebacks += 1

        # Insert new block
        block = cache_set.blocks[way]

        block.load_block(
            tag,
            self.timestamp
        )

        if operation == "WRITE":
            block.dirty = True

        return "MISS"

    def get_statistics(self):

        total = self.hits + self.misses

        hit_ratio = (
            self.hits / total * 100
            if total else 0
        )

        miss_ratio = (
            self.misses / total * 100
            if total else 0
        )

        return {
            "total_accesses": total,
            "hits": self.hits,
            "misses": self.misses,
            "evictions": self.evictions,
            "writebacks": self.writebacks,
            "hit_ratio": round(hit_ratio, 2),
            "miss_ratio": round(miss_ratio, 2)
        }

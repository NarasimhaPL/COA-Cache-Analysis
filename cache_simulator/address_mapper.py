
class AddressMapper:

    def __init__(
        self,
        cache_size,
        block_size,
        associativity
    ):

        if cache_size <= 0 or block_size <= 0:
            raise ValueError("Cache and block sizes must be positive")

        if associativity <= 0:
            raise ValueError("Associativity must be positive")

        if cache_size % (block_size * associativity) != 0:
            raise ValueError("Invalid cache configuration")

        self.cache_size = cache_size
        self.block_size = block_size
        self.associativity = associativity

        self.number_of_sets = (
            cache_size //
            (block_size * associativity)
        )

    def map_address(self, address):

        if address < 0:
            raise ValueError("Address cannot be negative")

        block_number = address // self.block_size

        set_index = (
            block_number % self.number_of_sets
        )

        tag = (
            block_number // self.number_of_sets
        )

        block_offset = (
            address % self.block_size
        )

        return {
            "block_number": block_number,
            "set_index": set_index,
            "tag": tag,
            "offset": block_offset
        }


from .cache_block import CacheBlock


class CacheSet:

    def __init__(self, associativity):

        self.associativity = associativity

        # Create cache blocks
        self.blocks = [
            CacheBlock()
            for _ in range(associativity)
        ]

    def find_block(self, tag):
        """Find a valid block matching the tag."""

        for index, block in enumerate(self.blocks):

            if block.valid and block.tag == tag:
                return index

        return None

    def find_empty_block(self):
        """Find an invalid cache block."""

        for index, block in enumerate(self.blocks):

            if not block.valid:
                return index

        return None

    def get_valid_blocks(self):
        """Return all valid cache blocks."""

        return [
            block
            for block in self.blocks
            if block.valid
        ]

    def __repr__(self):

        return str(self.blocks)

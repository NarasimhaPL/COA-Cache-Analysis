
class CacheBlock:

    def __init__(self):
        self.tag = None
        self.valid = False
        self.dirty = False

        # Metadata for replacement policies
        self.last_accessed = 0
        self.inserted_at = 0
        self.frequency = 0
        self.reference_bit = 0

    def load_block(self, tag, timestamp):
        """Load a new memory block into cache."""

        self.tag = tag
        self.valid = True
        self.dirty = False

        self.last_accessed = timestamp
        self.inserted_at = timestamp
        self.frequency = 1
        self.reference_bit = 1

    def access(self, timestamp, operation):
        """Update metadata when block is accessed."""

        self.last_accessed = timestamp
        self.frequency += 1
        self.reference_bit = 1

        if operation == "WRITE":
            self.dirty = True

    def invalidate(self):
        """Invalidate the cache block."""

        self.tag = None
        self.valid = False
        self.dirty = False
        self.frequency = 0
        self.reference_bit = 0

    def __repr__(self):
        return (
            f"CacheBlock(tag={self.tag}, "
            f"valid={self.valid}, "
            f"dirty={self.dirty})"
        )

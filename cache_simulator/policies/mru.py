
class MRUPolicy:
    """Most Recently Used cache replacement policy."""

    def choose_victim(self, blocks):

        if not blocks:
            raise ValueError("No valid blocks available for replacement.")

        return max(
            blocks,
            key=lambda block: block.last_accessed
        )

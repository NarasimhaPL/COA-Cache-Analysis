
class LRUPolicy:
    """Least Recently Used cache replacement policy."""

    def choose_victim(self, blocks):
        """
        Select the block that was accessed least recently.
        """

        if not blocks:
            raise ValueError("No valid blocks available for replacement.")

        return min(
            blocks,
            key=lambda block: block.last_accessed
        )

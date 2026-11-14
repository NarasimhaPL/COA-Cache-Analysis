
class LFUPolicy:
    """Least Frequently Used cache replacement policy."""

    def choose_victim(self, blocks):
        """
        Select the block with the lowest access frequency.
        """

        if not blocks:
            raise ValueError("No valid blocks available for replacement.")

        return min(
            blocks,
            key=lambda block: (block.frequency, block.inserted_at)
        )

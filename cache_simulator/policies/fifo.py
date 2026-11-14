
class FIFOPolicy:
    """First-In, First-Out cache replacement policy."""

    def choose_victim(self, blocks):
        """
        Select the block that was inserted earliest.

        Args:
            blocks: List of valid cache blocks.

        Returns:
            The cache block to replace.
        """

        if not blocks:
            raise ValueError("No valid blocks available for replacement.")

        return min(
            blocks,
            key=lambda block: block.inserted_at
        )

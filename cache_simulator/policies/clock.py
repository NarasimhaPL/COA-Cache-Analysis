
class ClockPolicy:
    """Clock (Second-Chance) cache replacement policy."""

    def __init__(self):
        # Each cache set gets its own clock hand.
        self.hands = {}

    def choose_victim(self, blocks, set_index=0):
        """
        Select a victim using the Clock algorithm.

        The blocks argument should contain the full list of
        blocks belonging to one cache set, including invalid blocks.
        """

        if not blocks:
            raise ValueError("No cache blocks available.")

        if not all(block.valid for block in blocks):
            raise ValueError(
                "Clock replacement should only run when the set is full."
            )

        n = len(blocks)

        # Get this set's current clock-hand position.
        hand = self.hands.get(set_index, 0)

        while True:
            block = blocks[hand]

            if block.reference_bit == 0:
                self.hands[set_index] = (hand + 1) % n
                return block

            # Give this block a second chance.
            block.reference_bit = 0
            hand = (hand + 1) % n

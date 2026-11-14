
import random


class RandomPolicy:
    """Random cache replacement policy."""

    def choose_victim(self, blocks):

        if not blocks:
            raise ValueError("No valid blocks available for replacement.")

        return random.choice(blocks)

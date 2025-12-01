class Card:
    def __init__(self, suit, rank):
        self.suit = suit
        self.rank = rank

    @property
    def value(self):
        if self.rank in ["jack", "queen", "king"]:
            return 10
        elif self.rank == "1":     # Ace
            return 11
        return int(self.rank)

    def filename(self):
        return f"cards/{self.suit}_{self.rank}.png"

    def __repr__(self):
        return f"{self.rank} of {self.suit}"

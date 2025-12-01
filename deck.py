import random
from card import Card

class Deck:
    def __init__(self):
        suits = ["club", "diamond", "heart", "spade"]
        ranks = ["1", "2", "3", "4", "5", "6", "7", "8", "9", "10", "jack", "queen", "king"]

        # Build full deck using Card objects
        self.cards = [Card(s, r) for s in suits for r in ranks]

    def shuffle(self):
        random.shuffle(self.cards)

    def draw(self):
        return self.cards.pop()

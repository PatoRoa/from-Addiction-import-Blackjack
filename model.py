# model.py
import random
from dataclasses import dataclass

SUITS = ["♠", "♥", "♦", "♣"]
RANKS = ["A", "2", "3", "4", "5", "6", "7", "8", "9", "10", "J", "Q", "K"]
VALUES = {**{str(i): i for i in range(2, 11)}, "J": 10, "Q": 10, "K": 10, "A": 11}


@dataclass(frozen=True)
class Card:
    rank: str
    suit: str

    @property
    def value(self) -> int:
        return VALUES[self.rank]


class Deck:
    def __init__(self, n_decks: int = 1):
        self.cards = [Card(rank, suit)
                      for _ in range(n_decks)
                      for suit in SUITS
                      for rank in RANKS]
        random.shuffle(self.cards)

    def draw(self) -> Card:
        if not self.cards:
            raise RuntimeError("Deck is empty.")
        return self.cards.pop()


class Hand:
    def __init__(self):
        self.cards: list[Card] = []

    def add(self, card: Card) -> None:
        self.cards.append(card)

    def total(self) -> int:
        total = sum(c.value for c in self.cards)
        aces = sum(1 for c in self.cards if c.rank == "A")

        # Convert Aces from 11 to 1 if hand > 21
        while total > 21 and aces:
            total -= 10
            aces -= 1

        return total

    def is_blackjack(self) -> bool:
        return len(self.cards) == 2 and self.total() == 21

    def is_bust(self) -> bool:
        return len(self.cards) > 21


class Player:
    def __init__(self, name: str = "Player", chips: int = 1000):
        self.name = name
        self.chips = chips
        self.hand = Hand()
        self.bet = 0

    def place_bet(self, amount: int) -> None:
        if amount < 1 or amount > self.chips:
            raise ValueError("Invalid bet amount.")
        self.bet = amount
        self.chips -= amount


class Dealer(Player):
    def __init__(self):
        super().__init__(name="Dealer", chips=0)


if __name__ == "__main__":
    d = Deck()
    h = Hand()
    h.add(d.draw())
    h.add(d.draw())

    print("Hand: ", " ".join(f"{c.rank}{c.suit}" for c in h.cards), "=>", h.total())
    print("Blackjack?", h.is_blackjack(), "Bust?", h.is_bust())

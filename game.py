# game.py
import time
from model import Deck, Player, Dealer


class BlackjackGame:
    def __init__(self, n_decks: int = 6, delay: float = 0.0):
        self.deck = Deck(n_decks)
        self.player = Player(name="You", chips=1000)
        self.dealer = Dealer()
        self.delay = delay

    def _reset_hands(self):
        self.player.hand = type(self.player.hand)()
        self.dealer.hand = type(self.dealer.hand)()

    def new_round(self, bet:int):
        """Start a new round and place a bet."""
        self._reset_hands()
        self.player.place_bet(bet)

        # Deal two cards to Player, and two to Dealer
        for _ in range(2):
            self.player.hand.add(self.deck.draw())
            self.dealer.hand.add(self.deck.draw())

    def player_hit(self):
        self.player.hand.add(self.deck.draw())
        return self.player.hand.is_bust()

    def dealer_play(self):
        """Dealer hits up to 17+ (stands on 17)."""
        while self.dealer.hand.total() < 17:
            self.dealer.hand.add(self.deck.draw())
            if self.delay:
                time.sleep(self.delay)

    def resolve(self) -> str:
        """Decide outcome and settle chips. Returns a result string."""
        p = self.player.hand
        d = self.dealer.hand

        # Compare totals
        pt = p.total()
        dt = d.total()

        # Debug
        # print(f"DEBUG - Player total: {pt}, Dealer total: {dt}")

        if pt > 21:
            return "player_bust"

        if dt > 21:
            self.player.chips += self.player.bet * 2
            return "dealer_bust:"

        # Blackjacks
        if p.is_blackjack() and not d.is_blackjack():
            # 3:2 payout rounded down
            self.player.chips += int(self.player.bet * 2.5)
            return "player_blackjack"

        if d.is_blackjack() and not p.is_blackjack():
            return "dealer_blackjack"

        if pt > dt:
            self.player.chips += self.player.bet * 2
            return "player_win"

        if pt < dt:
            return "dealer_win"

        # Push
        self.player.chips += self.player.bet
        return "push"

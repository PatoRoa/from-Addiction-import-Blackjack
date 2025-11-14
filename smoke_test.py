# smoke_test.py
# Used to test game.py
from game import BlackjackGame

g = BlackjackGame(n_decks=1)
g.new_round(bet=50)
print("Player:", [(c.rank, c.suit) for c in g.player.hand.cards], g.player.hand.total())
print("Dealer:", [(c.rank, c.suit) for c in g.dealer.hand.cards], "(hole card hidden)")

# Simulate simple strategy: hit until 17+
while g.player.hand.total() < 17:
    if g.player_hit():
        print("Player busted.")
        break
print("Player stands at:", g.player.hand.total())

g.dealer_play()
result = g.resolve()
print("Dealer total:", g.dealer.hand.total())
print("Result:", result, "| Chips:", g.player.chips)

# test_game.py
import unittest
from model import Card, Hand
from game import BlackjackGame


class TestTotals(unittest.TestCase):
    def test_ace_adjustment(self):
        h = Hand()
        h.add(Card("A","♠")); h.add(Card("9","♦")); h.add(Card("5","♣"))
        self.assertEqual(h.total(), 15)


class TestGameFlow(unittest.TestCase):
    def test_new_rouund_places_bet(self):
        g = BlackjackGame()
        chips_before = g.player.chips
        g.new_round(100)
        self.assertEqual(g.player.chips, chips_before - 100)
        self.assertEqual(len(g.player.hand.cards), 2)
        self.assertEqual(len(g.dealer.hand.cards), 2)


if __name__ == "__main__":
    unittest.main()
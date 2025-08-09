import unittest
from src.raffle.selection import RaffleSelector

class TestRaffleSelector(unittest.TestCase):

    def setUp(self):
        self.commenters = ["user1", "user2", "user3"]
        self.selector = RaffleSelector(self.commenters)

    def test_select_winner(self):
        winner = self.selector.select_winner()
        self.assertIn(winner, self.commenters)

    def test_multiple_winner_selections(self):
        winners = {self.selector.select_winner() for _ in range(100)}
        self.assertTrue(len(winners) > 1)

    def test_empty_commenters(self):
        empty_selector = RaffleSelector([])
        with self.assertRaises(ValueError):
            empty_selector.select_winner()

if __name__ == '__main__':
    unittest.main()
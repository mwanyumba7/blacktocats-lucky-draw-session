class RaffleSelector:
    def __init__(self, commenters):
        self.commenters = commenters

    def select_winner(self):
        import random
        if not self.commenters:
            return None
        return random.choice(self.commenters)

    def get_winner_message(self, winner):
        if winner:
            return f"Congratulations to {winner}! You've won the raffle!"
        else:
            return "No participants in the raffle."
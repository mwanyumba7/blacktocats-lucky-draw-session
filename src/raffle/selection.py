import random
import time
from typing import List, Optional, Dict, Any
from datetime import datetime


class RaffleSelector:
    def __init__(self, commenters: List[str], exclude_users: Optional[List[str]] = None):
        """
        Initialize the raffle selector.
        
        Args:
            commenters: List of GitHub usernames
            exclude_users: Optional list of users to exclude from the raffle
        """
        self.original_commenters = commenters.copy()
        self.exclude_users = exclude_users or []
        
        # Filter out excluded users
        self.commenters = [user for user in commenters if user not in self.exclude_users]
        self.winner = None
        self.selection_timestamp = None
        
    def get_participants_count(self) -> int:
        """Get the total number of eligible participants."""
        return len(self.commenters)
    
    def get_excluded_count(self) -> int:
        """Get the number of excluded users."""
        return len(self.original_commenters) - len(self.commenters)
    
    def select_winner(self, seed: Optional[int] = None) -> Optional[str]:
        """
        Select a random winner from the commenters.
        
        Args:
            seed: Optional random seed for reproducible results
            
        Returns:
            Username of the winner or None if no participants
        """
        if not self.commenters:
            return None
            
        if seed is not None:
            random.seed(seed)
        
        self.winner = random.choice(self.commenters)
        self.selection_timestamp = datetime.now()
        
        return self.winner
    
    def select_multiple_winners(self, count: int, seed: Optional[int] = None) -> List[str]:
        """
        Select multiple winners from the commenters.
        
        Args:
            count: Number of winners to select
            seed: Optional random seed for reproducible results
            
        Returns:
            List of winner usernames
        """
        if not self.commenters:
            return []
            
        if seed is not None:
            random.seed(seed)
            
        # Don't select more winners than available participants
        actual_count = min(count, len(self.commenters))
        
        winners = random.sample(self.commenters, actual_count)
        return winners
    
    def get_winner_message(self, winner: Optional[str] = None) -> str:
        """
        Get a congratulatory message for the winner.
        
        Args:
            winner: Username of the winner (uses self.winner if not provided)
            
        Returns:
            Congratulatory message
        """
        winner_name = winner or self.winner
        
        if winner_name:
            messages = [
                f"🎉 Congratulations to @{winner_name}! You've won the GitHub Commenter Raffle! 🎉",
                f"🏆 Winner winner! @{winner_name} has been selected as our lucky winner! 🏆", 
                f"🎊 Amazing! @{winner_name} is our raffle champion! 🎊",
                f"🥳 Fantastic! @{winner_name} has won the prize! 🥳"
            ]
            return random.choice(messages)
        else:
            return "❌ No participants found in the raffle. Make sure there are comments on the issue!"
    
    def get_raffle_stats(self) -> Dict[str, Any]:
        """
        Get comprehensive statistics about the raffle.
        
        Returns:
            Dictionary containing raffle statistics
        """
        stats = {
            'total_commenters': len(self.original_commenters),
            'eligible_participants': len(self.commenters),
            'excluded_users': self.exclude_users,
            'excluded_count': self.get_excluded_count(),
            'winner': self.winner,
            'selection_timestamp': self.selection_timestamp.isoformat() if self.selection_timestamp else None,
            'participation_rate': len(self.commenters) / len(self.original_commenters) if self.original_commenters else 0
        }
        return stats
    
    def simulate_raffle_animation(self, duration_seconds: float = 3.0) -> List[str]:
        """
        Simulate a raffle animation by returning a sequence of potential winners.
        
        Args:
            duration_seconds: How long the animation should run
            
        Returns:
            List of usernames shown during animation
        """
        if not self.commenters:
            return []
            
        animation_steps = []
        steps = int(duration_seconds * 10)  # 10 steps per second
        
        for i in range(steps):
            # Show random users during animation
            random_user = random.choice(self.commenters)
            animation_steps.append(random_user)
            
        return animation_steps
    
    def is_valid_raffle(self) -> bool:
        """Check if the raffle has valid participants."""
        return len(self.commenters) > 0
    
    def reset(self):
        """Reset the raffle to initial state."""
        self.winner = None
        self.selection_timestamp = None
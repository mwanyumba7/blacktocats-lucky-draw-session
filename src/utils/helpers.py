import re
import random
from typing import List, Dict, Any, Optional, Tuple
from datetime import datetime
from urllib.parse import urlparse


def format_commenter_data(commenters: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
    """
    Format commenter data for display.
    
    Args:
        commenters: List of commenter objects from GitHub API
        
    Returns:
        List of formatted commenter dictionaries
    """
    formatted_data = []
    for commenter in commenters:
        formatted_data.append({
            'username': commenter.get('login', 'unknown'),
            'avatar_url': commenter.get('avatar_url', ''),
            'profile_url': commenter.get('html_url', ''),
            'user_type': commenter.get('type', 'User')
        })
    return formatted_data


def validate_repository_format(repo: str) -> bool:
    """
    Validate that repository string is in correct 'owner/repo' format.
    
    Args:
        repo: Repository string
        
    Returns:
        True if format is valid
    """
    pattern = r'^[a-zA-Z0-9]([a-zA-Z0-9._-]*[a-zA-Z0-9])?/[a-zA-Z0-9]([a-zA-Z0-9._-]*[a-zA-Z0-9])?$'
    return bool(re.match(pattern, repo)) if repo else False


def parse_repository_url(url: str) -> Optional[str]:
    """
    Parse a GitHub repository URL and extract owner/repo format.
    
    Args:
        url: GitHub repository URL
        
    Returns:
        Repository in 'owner/repo' format or None if invalid
    """
    try:
        parsed = urlparse(url)
        if 'github.com' not in parsed.netloc:
            return None
            
        path_parts = parsed.path.strip('/').split('/')
        if len(path_parts) >= 2:
            owner, repo = path_parts[0], path_parts[1]
            # Remove .git suffix if present
            if repo.endswith('.git'):
                repo = repo[:-4]
            return f"{owner}/{repo}"
    except:
        pass
    return None


def validate_issue_number(issue_number: str) -> Tuple[bool, Optional[int]]:
    """
    Validate and convert issue number string to integer.
    
    Args:
        issue_number: Issue number as string
        
    Returns:
        Tuple of (is_valid, converted_number)
    """
    try:
        num = int(issue_number)
        return num > 0, num if num > 0 else None
    except (ValueError, TypeError):
        return False, None


def filter_bot_users(commenters: List[str], include_bots: bool = False) -> List[str]:
    """
    Filter out bot users from commenters list.
    
    Args:
        commenters: List of usernames
        include_bots: Whether to include bots in results
        
    Returns:
        Filtered list of usernames
    """
    if include_bots:
        return commenters
    
    # Common bot patterns
    bot_patterns = [
        r'.*\[bot\]$',
        r'^dependabot',
        r'^renovate',
        r'^github-actions',
        r'^codecov',
        r'.*-bot$',
        r'.*bot$'
    ]
    
    filtered = []
    for user in commenters:
        is_bot = any(re.match(pattern, user, re.IGNORECASE) for pattern in bot_patterns)
        if not is_bot:
            filtered.append(user)
    
    return filtered


def get_random_winner(commenters: List[str], seed: Optional[int] = None) -> Optional[str]:
    """
    Select a random winner from commenters.
    
    Args:
        commenters: List of commenter usernames
        seed: Optional random seed for reproducible results
        
    Returns:
        Selected winner username or None if no commenters
    """
    if not commenters:
        return None
    
    if seed is not None:
        random.seed(seed)
    
    return random.choice(commenters)


def validate_commenter_data(commenters: List[Dict[str, Any]]) -> bool:
    """
    Validate that commenter data has required fields.
    
    Args:
        commenters: List of commenter objects
        
    Returns:
        True if all commenters have required fields
    """
    if not commenters:
        return False
    
    required_fields = ['login']
    return all(
        isinstance(commenter, dict) and 
        all(field in commenter for field in required_fields)
        for commenter in commenters
    )


def generate_winner_announcement(winner: str, repo: str, issue_number: int) -> str:
    """
    Generate a formatted winner announcement.
    
    Args:
        winner: Winner username
        repo: Repository name
        issue_number: Issue number
        
    Returns:
        Formatted announcement string
    """
    announcements = [
        f"🎉 Congratulations @{winner}! You're the winner of the GitHub Commenter Raffle for {repo} issue #{issue_number}!",
        f"🏆 We have a winner! @{winner} has been selected from {repo} issue #{issue_number}!",
        f"🎊 Amazing! @{winner} wins the raffle for commenting on {repo} issue #{issue_number}!",
        f"🥳 Fantastic! @{winner} is our lucky winner from {repo} issue #{issue_number}!"
    ]
    
    return random.choice(announcements)


def format_timestamp(timestamp: Optional[datetime]) -> str:
    """
    Format timestamp for display.
    
    Args:
        timestamp: Datetime object
        
    Returns:
        Formatted timestamp string
    """
    if not timestamp:
        return "Unknown"
    
    return timestamp.strftime("%Y-%m-%d %H:%M:%S UTC")


def sanitize_input(text: str) -> str:
    """
    Sanitize user input by removing potentially harmful characters.
    
    Args:
        text: Input text to sanitize
        
    Returns:
        Sanitized text
    """
    if not isinstance(text, str):
        return ""
    
    # Remove HTML tags and potentially harmful characters
    sanitized = re.sub(r'<[^>]*>', '', text)
    sanitized = re.sub(r'[<>&"\'`]', '', sanitized)
    
    return sanitized.strip()


def calculate_participation_stats(total_comments: int, unique_commenters: int) -> Dict[str, Any]:
    """
    Calculate participation statistics.
    
    Args:
        total_comments: Total number of comments
        unique_commenters: Number of unique commenters
        
    Returns:
        Dictionary with participation statistics
    """
    avg_comments_per_user = total_comments / unique_commenters if unique_commenters > 0 else 0
    
    return {
        'total_comments': total_comments,
        'unique_commenters': unique_commenters,
        'average_comments_per_user': round(avg_comments_per_user, 2),
        'engagement_level': 'High' if avg_comments_per_user > 2 else 'Medium' if avg_comments_per_user > 1 else 'Low'
    }
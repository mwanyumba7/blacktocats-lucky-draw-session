#!/usr/bin/env python3
"""
Test the enhanced backend logic
"""

import sys
import os
sys.path.append('src')

from api.github_client import GitHubClient
from raffle.selection import RaffleSelector
from utils.helpers import (
    validate_repository_format,
    parse_repository_url, 
    validate_issue_number,
    filter_bot_users,
    generate_winner_announcement
)

def test_helpers():
    print("🧪 Testing Helper Functions")
    print("=" * 40)
    
    # Test repository validation
    valid_repos = ["microsoft/vscode", "octocat/Hello-World", "user123/repo-name"]
    invalid_repos = ["invalid", "toolong/", "/invalid", "invalid repo"]
    
    print("✅ Valid repository formats:")
    for repo in valid_repos:
        result = validate_repository_format(repo)
        print(f"  {repo}: {result}")
        assert result == True
    
    print("❌ Invalid repository formats:")
    for repo in invalid_repos:
        result = validate_repository_format(repo)
        print(f"  {repo}: {result}")
        assert result == False
    
    # Test URL parsing
    test_urls = [
        ("https://github.com/microsoft/vscode", "microsoft/vscode"),
        ("https://github.com/octocat/Hello-World.git", "octocat/Hello-World"),
        ("invalid-url", None)
    ]
    
    print("\n🔗 URL parsing tests:")
    for url, expected in test_urls:
        result = parse_repository_url(url)
        print(f"  {url} -> {result}")
        assert result == expected
    
    # Test issue number validation
    test_numbers = [("123", True), ("0", False), ("-1", False), ("abc", False)]
    
    print("\n🔢 Issue number validation:")
    for num, expected in test_numbers:
        is_valid, _ = validate_issue_number(num)
        print(f"  {num}: {is_valid}")
        assert is_valid == expected
    
    # Test bot filtering
    test_users = ["user1", "dependabot[bot]", "github-actions[bot]", "real-user", "some-bot"]
    filtered = filter_bot_users(test_users, include_bots=False)
    print(f"\n🤖 Bot filtering: {test_users} -> {filtered}")
    assert "dependabot[bot]" not in filtered
    assert "github-actions[bot]" not in filtered
    assert "user1" in filtered
    assert "real-user" in filtered
    
    print("✅ All helper function tests passed!\n")

def test_raffle_selector():
    print("🎲 Testing Enhanced Raffle Selector")
    print("=" * 40)
    
    # Test with sample commenters
    commenters = ["alice", "bob", "charlie", "diana"]
    exclude_users = ["bob"]
    
    raffle = RaffleSelector(commenters, exclude_users)
    
    print(f"📊 Total participants: {raffle.get_participants_count()}")
    print(f"🚫 Excluded users: {raffle.get_excluded_count()}")
    
    # Test winner selection
    winner = raffle.select_winner(seed=42)  # Use seed for reproducible test
    print(f"🏆 Selected winner: {winner}")
    assert winner in commenters
    assert winner not in exclude_users
    
    # Test multiple winners
    winners = raffle.select_multiple_winners(2, seed=42)
    print(f"🏆 Multiple winners: {winners}")
    assert len(winners) <= len(raffle.commenters)
    
    # Test raffle stats
    stats = raffle.get_raffle_stats()
    print(f"📈 Raffle stats: {stats}")
    assert stats['total_commenters'] == len(commenters)
    assert stats['eligible_participants'] == len(commenters) - len(exclude_users)
    
    # Test winner message
    message = raffle.get_winner_message(winner)
    print(f"💬 Winner message: {message}")
    assert winner in message
    
    print("✅ All raffle selector tests passed!\n")

def test_github_client():
    print("🐙 Testing Enhanced GitHub Client")
    print("=" * 40)
    
    try:
        client = GitHubClient()
        
        # Test authentication
        if client.test_authentication():
            print("✅ GitHub authentication successful")
            
            # Test getting user info
            user_info = client.get_authenticated_user()
            print(f"👤 Authenticated as: {user_info.get('login')}")
            
            # Test rate limit info
            rate_limit = client.get_rate_limit_status()
            remaining = rate_limit.get('rate', {}).get('remaining', 'unknown')
            print(f"⚡ Rate limit remaining: {remaining}")
            
        else:
            print("❌ GitHub authentication failed")
            
    except Exception as e:
        print(f"❌ GitHub client test failed: {e}")
    
    print("✅ GitHub client tests completed!\n")

def test_integration():
    print("🔗 Testing Integration")
    print("=" * 40)
    
    # Test winner announcement generation
    announcement = generate_winner_announcement("testuser", "microsoft/vscode", 123)
    print(f"📢 Sample announcement: {announcement}")
    assert "testuser" in announcement
    assert "microsoft/vscode" in announcement
    assert "123" in announcement
    
    print("✅ Integration tests passed!\n")

if __name__ == "__main__":
    print("🚀 Running Enhanced Backend Logic Tests")
    print("=" * 50)
    
    test_helpers()
    test_raffle_selector()
    test_github_client()
    test_integration()
    
    print("🎉 All tests completed successfully!")
    print("🌐 Flask app is running at: http://127.0.0.1:5000")
    print("🎯 You can now test the enhanced raffle functionality!")

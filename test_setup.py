#!/usr/bin/env python3
"""
Test GitHub API Authentication
"""

import os
import sys
from pathlib import Path
from dotenv import load_dotenv

# Add src to path
sys.path.append('src')

def test_github_auth():
    print("🧪 Testing GitHub API Authentication")
    print("=" * 40)
    
    # Load environment variables
    load_dotenv()
    
    # Check if token is set
    token = os.getenv('GITHUB_TOKEN')
    if not token:
        print("❌ GITHUB_TOKEN not found in environment variables")
        print("📝 Please run: python setup_github_auth.py")
        return False
    
    print(f"✅ GitHub token found (length: {len(token)})")
    
    # Test authentication
    try:
        from api.github_client import GitHubClient
        
        print("🔄 Testing GitHub API connection...")
        client = GitHubClient()
        
        if client.test_authentication():
            print("✅ GitHub API authentication successful!")
            return True
        else:
            print("❌ GitHub API authentication failed")
            print("📝 Please check your token is valid and has the correct permissions")
            return False
            
    except Exception as e:
        print(f"❌ Error testing GitHub API: {e}")
        return False

def test_sample_repository():
    """Test fetching commenters from a sample repository"""
    print("\n🧪 Testing Sample Repository Access")
    print("=" * 40)
    
    try:
        from api.github_client import GitHubClient
        
        client = GitHubClient()
        
        # Test with a well-known repository and issue
        repo = "microsoft/vscode"
        issue_number = 1
        
        print(f"🔄 Testing access to {repo}/issues/{issue_number}...")
        
        try:
            commenters = client.fetch_issue_commenters(repo, issue_number)
            print(f"✅ Successfully fetched commenters!")
            print(f"📊 Found {len(commenters)} unique commenters")
            if commenters:
                print(f"📝 Sample commenters: {commenters[:5]}...")  # Show first 5
            return True
            
        except Exception as e:
            print(f"❌ Error fetching commenters: {e}")
            return False
            
    except Exception as e:
        print(f"❌ Error: {e}")
        return False

if __name__ == "__main__":
    auth_success = test_github_auth()
    
    if auth_success:
        test_sample_repository()
        print("\n🎉 Setup complete! You can now run the raffle app.")
        print("🚀 Run: python src/app.py")
    else:
        print("\n❌ Setup incomplete. Please fix the issues above.")

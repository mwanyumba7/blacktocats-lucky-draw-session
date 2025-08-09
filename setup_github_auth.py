#!/usr/bin/env python3
"""
GitHub Commenter Raffle Setup Script
This script helps you set up GitHub API authentication.
"""

import os
import sys
from pathlib import Path

def main():
    print("🎯 GitHub Commenter Raffle Setup")
    print("=" * 40)
    
    # Check if .env file exists
    env_file = Path('.env')
    if not env_file.exists():
        print("❌ .env file not found!")
        print("📝 Creating .env file from template...")
        
        # Copy from .env.example if it exists
        example_file = Path('.env.example')
        if example_file.exists():
            with open(example_file, 'r') as f:
                content = f.read()
            with open(env_file, 'w') as f:
                f.write(content)
            print("✅ .env file created!")
        else:
            print("❌ .env.example not found. Please create .env manually.")
            return
    
    print("\n📋 GitHub Personal Access Token Setup:")
    print("1. Go to https://github.com/settings/tokens")
    print("2. Click 'Generate new token (classic)'")
    print("3. Give it a descriptive name (e.g., 'Commenter Raffle App')")
    print("4. Select the following scopes:")
    print("   - repo (for private repositories)")
    print("   - public_repo (for public repositories)")
    print("   - read:user (to read user information)")
    print("5. Click 'Generate token'")
    print("6. Copy the token (you won't see it again!)")
    
    print(f"\n🔧 Next steps:")
    print(f"1. Open the .env file: {env_file.absolute()}")
    print(f"2. Replace 'your_github_personal_access_token_here' with your actual token")
    print(f"3. Save the file")
    print(f"4. Run: python test_setup.py")

if __name__ == "__main__":
    main()

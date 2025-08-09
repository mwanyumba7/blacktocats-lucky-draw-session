import requests
import os
from typing import List, Optional, Dict, Any
from datetime import datetime, timedelta
import time


class GitHubClient:
    def __init__(self, token: Optional[str] = None):
        self.token = token or os.getenv('GITHUB_TOKEN')
        self.base_url = "https://api.github.com"
        self.rate_limit_remaining = None
        self.rate_limit_reset = None
        
        if not self.token:
            raise ValueError("GitHub token is required. Set GITHUB_TOKEN environment variable or pass token parameter.")

    def authenticate(self) -> dict:
        """Create authentication headers for GitHub API requests."""
        headers = {
            "Authorization": f"Bearer {self.token}",
            "Accept": "application/vnd.github.v3+json",
            "X-GitHub-Api-Version": "2022-11-28"
        }
        return headers

    def _update_rate_limit_info(self, response: requests.Response):
        """Update rate limit information from response headers."""
        self.rate_limit_remaining = int(response.headers.get('X-RateLimit-Remaining', 0))
        self.rate_limit_reset = int(response.headers.get('X-RateLimit-Reset', 0))

    def _handle_rate_limit(self, response: requests.Response):
        """Handle rate limiting by waiting if necessary."""
        if response.status_code == 403 and 'rate limit' in response.text.lower():
            reset_time = datetime.fromtimestamp(self.rate_limit_reset)
            wait_time = (reset_time - datetime.now()).total_seconds()
            if wait_time > 0:
                print(f"Rate limit exceeded. Waiting {wait_time:.0f} seconds...")
                time.sleep(min(wait_time, 60))  # Cap wait time at 1 minute

    def test_authentication(self) -> bool:
        """Test if the GitHub token is valid."""
        url = f"{self.base_url}/user"
        headers = self.authenticate()
        
        try:
            response = requests.get(url, headers=headers)
            self._update_rate_limit_info(response)
            return response.status_code == 200
        except Exception:
            return False

    def get_authenticated_user(self) -> Dict[str, Any]:
        """Get information about the authenticated user."""
        url = f"{self.base_url}/user"
        headers = self.authenticate()
        
        try:
            response = requests.get(url, headers=headers)
            response.raise_for_status()
            self._update_rate_limit_info(response)
            return response.json()
        except Exception as e:
            raise Exception(f"Error fetching user info: {str(e)}")

    def fetch_issue_commenters(self, repo: str, issue_number: int, exclude_author: bool = False) -> List[str]:
        """
        Fetch commenters from a GitHub issue.
        
        Args:
            repo: Repository in format 'owner/repo'
            issue_number: Issue number
            exclude_author: Whether to exclude the issue author from results
            
        Returns:
            List of unique commenter usernames
        """
        # First get the issue to find the author if needed
        issue_author = None
        if exclude_author:
            issue_info = self.get_issue_info(repo, issue_number)
            issue_author = issue_info.get('user', {}).get('login')

        url = f"{self.base_url}/repos/{repo}/issues/{issue_number}/comments"
        headers = self.authenticate()
        all_commenters = []
        page = 1
        
        try:
            while True:
                params = {'page': page, 'per_page': 100}
                response = requests.get(url, headers=headers, params=params)
                response.raise_for_status()
                self._update_rate_limit_info(response)
                
                comments = response.json()
                if not comments:  # No more comments
                    break
                    
                # Extract usernames from this page
                page_commenters = [comment['user']['login'] for comment in comments if comment['user']['login']]
                all_commenters.extend(page_commenters)
                
                page += 1
                
                # Check if we've reached the last page
                if len(comments) < 100:
                    break
            
            # Remove duplicates and optionally exclude issue author
            unique_commenters = list(set(all_commenters))
            
            if exclude_author and issue_author:
                unique_commenters = [user for user in unique_commenters if user != issue_author]
            
            return unique_commenters
            
        except requests.exceptions.HTTPError as e:
            if response.status_code == 404:
                raise Exception(f"Repository or issue not found: {repo}/issues/{issue_number}")
            elif response.status_code == 403:
                self._handle_rate_limit(response)
                raise Exception("GitHub API rate limit exceeded or insufficient permissions")
            else:
                raise Exception(f"Error fetching commenters: {response.status_code} - {response.text}")
        except Exception as e:
            raise Exception(f"Unexpected error: {str(e)}")

    def get_issue_info(self, repo: str, issue_number: int) -> Dict[str, Any]:
        """
        Get detailed information about a GitHub issue.
        
        Args:
            repo: Repository in format 'owner/repo'
            issue_number: Issue number
            
        Returns:
            Dictionary containing issue information
        """
        url = f"{self.base_url}/repos/{repo}/issues/{issue_number}"
        headers = self.authenticate()
        
        try:
            response = requests.get(url, headers=headers)
            response.raise_for_status()
            self._update_rate_limit_info(response)
            return response.json()
        except Exception as e:
            raise Exception(f"Error fetching issue info: {str(e)}")

    def get_repository_info(self, repo: str) -> Dict[str, Any]:
        """Get basic repository information."""
        url = f"{self.base_url}/repos/{repo}"
        headers = self.authenticate()
        
        try:
            response = requests.get(url, headers=headers)
            response.raise_for_status()
            self._update_rate_limit_info(response)
            return response.json()
        except Exception as e:
            raise Exception(f"Error fetching repository info: {str(e)}")

    def get_comment_details(self, repo: str, issue_number: int) -> List[Dict[str, Any]]:
        """
        Get detailed information about all comments on an issue.
        
        Args:
            repo: Repository in format 'owner/repo'
            issue_number: Issue number
            
        Returns:
            List of comment dictionaries with user info, timestamps, etc.
        """
        url = f"{self.base_url}/repos/{repo}/issues/{issue_number}/comments"
        headers = self.authenticate()
        all_comments = []
        page = 1
        
        try:
            while True:
                params = {'page': page, 'per_page': 100}
                response = requests.get(url, headers=headers, params=params)
                response.raise_for_status()
                self._update_rate_limit_info(response)
                
                comments = response.json()
                if not comments:
                    break
                    
                all_comments.extend(comments)
                page += 1
                
                if len(comments) < 100:
                    break
            
            return all_comments
            
        except Exception as e:
            raise Exception(f"Error fetching comment details: {str(e)}")

    def get_rate_limit_status(self) -> Dict[str, Any]:
        """Get current rate limit status."""
        url = f"{self.base_url}/rate_limit"
        headers = self.authenticate()
        
        try:
            response = requests.get(url, headers=headers)
            response.raise_for_status()
            return response.json()
        except Exception as e:
            return {
                'remaining': self.rate_limit_remaining,
                'reset': self.rate_limit_reset,
                'error': str(e)
            }

    def validate_repository(self, repo: str) -> bool:
        """
        Validate if a repository exists and is accessible.
        
        Args:
            repo: Repository in format 'owner/repo'
            
        Returns:
            True if repository is valid and accessible
        """
        try:
            self.get_repository_info(repo)
            return True
        except:
            return False
import requests

class GitHubClient:
    def __init__(self, token=None):
        self.token = token
        self.base_url = "https://api.github.com"

    def authenticate(self):
        headers = {
            "Accept": "application/vnd.github.v3+json"
        }
        if self.token:
            headers["Authorization"] = f"token {self.token}"
        return headers

    def fetch_issue_commenters(self, owner, repo, issue_number):
        url = f"{self.base_url}/repos/{owner}/{repo}/issues/{issue_number}/comments"
        headers = self.authenticate()
        response = requests.get(url, headers=headers)

        if response.status_code == 200:
            comments = response.json()
            # Get unique commenters (avoid duplicates if someone commented multiple times)
            commenters = list(set([comment['user']['login'] for comment in comments]))
            return commenters
        else:
            raise Exception(f"Error fetching commenters: {response.status_code} - {response.text}")
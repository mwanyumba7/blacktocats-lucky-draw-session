class GitHubClient:
    def __init__(self, token):
        self.token = token
        self.base_url = "https://api.github.com"

    def authenticate(self):
        headers = {
            "Authorization": f"token {self.token}",
            "Accept": "application/vnd.github.v3+json"
        }
        return headers

    def fetch_issue_commenters(self, owner, repo, issue_number):
        url = f"{self.base_url}/repos/{owner}/{repo}/issues/{issue_number}/comments"
        headers = self.authenticate()
        response = requests.get(url, headers=headers)

        if response.status_code == 200:
            commenters = [comment['user']['login'] for comment in response.json()]
            return commenters
        else:
            raise Exception(f"Error fetching commenters: {response.status_code} - {response.text}")
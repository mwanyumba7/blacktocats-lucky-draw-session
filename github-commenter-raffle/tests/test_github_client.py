import unittest
from src.api.github_client import GitHubClient

class TestGitHubClient(unittest.TestCase):

    def setUp(self):
        self.client = GitHubClient(token='test_token')

    def test_authentication(self):
        self.assertTrue(self.client.authenticate())

    def test_fetch_issue_commenters(self):
        issue_number = 1
        commenters = self.client.fetch_issue_commenters(repo='owner/repo', issue_number=issue_number)
        self.assertIsInstance(commenters, list)

    def test_fetch_issue_commenters_empty(self):
        issue_number = 99999  # Assuming this issue does not exist
        commenters = self.client.fetch_issue_commenters(repo='owner/repo', issue_number=issue_number)
        self.assertEqual(commenters, [])

if __name__ == '__main__':
    unittest.main()
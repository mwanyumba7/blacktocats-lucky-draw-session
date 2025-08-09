import os
from flask import Flask, render_template, request, redirect, url_for
from api.github_client import GitHubClient
from raffle.selection import RaffleSelector

# Get the parent directory (github-commenter-raffle)
basedir = os.path.abspath(os.path.dirname(os.path.dirname(__file__)))

app = Flask(__name__, 
            template_folder=os.path.join(basedir, 'templates'),
            static_folder=os.path.join(basedir, 'static'))

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/raffle', methods=['POST'])
def raffle():
    repo = request.form['repository']
    issue_number = request.form['issue_number']
    
    # Parse repo format (owner/repo)
    if '/' in repo:
        owner, repo_name = repo.split('/', 1)
    else:
        return "Invalid repository format. Use 'owner/repo'", 400
    
    github_client = GitHubClient(token=None)  # We'll make it work without token for public repos
    commenters = github_client.fetch_issue_commenters(owner, repo_name, issue_number)
    
    raffle_selector = RaffleSelector(commenters)
    winner = raffle_selector.select_winner()
    
    return render_template('results.html', winner=winner)

if __name__ == '__main__':
    app.run(debug=True)
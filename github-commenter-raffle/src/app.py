from flask import Flask, render_template, request, redirect, url_for
from api.github_client import GitHubClient
from raffle.selection import RaffleSelector

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/raffle', methods=['POST'])
def raffle():
    repo = request.form['repository']
    issue_number = request.form['issue_number']
    
    github_client = GitHubClient()
    commenters = github_client.fetch_issue_commenters(repo, issue_number)
    
    raffle_selector = RaffleSelector(commenters)
    winner = raffle_selector.select_winner()
    
    return render_template('results.html', winner=winner)

if __name__ == '__main__':
    app.run(debug=True)
from flask import Flask, render_template, request, redirect, url_for, jsonify, session
from api.github_client import GitHubClient
from raffle.selection import RaffleSelector
import os

app = Flask(__name__)
app.secret_key = os.environ.get('SECRET_KEY', 'dev-secret-key-change-in-production')

# Global state for the current raffle
current_raffle = {
    'commenters': [],
    'winner': None,
    'repo_info': None
}

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/api/fetch-commenters', methods=['POST'])
def fetch_commenters():
    """Fetch commenters from GitHub API"""
    try:
        data = request.get_json()
        repo = data.get('repository')
        issue_number = data.get('issue_number')
        
        if not repo or not issue_number:
            return jsonify({'error': 'Repository and issue number are required'}), 400
        
        # Parse repo (assuming format: owner/repo)
        if '/' not in repo:
            return jsonify({'error': 'Repository format should be owner/repo'}), 400
        
        owner, repo_name = repo.split('/', 1)
        
        github_client = GitHubClient(token=os.environ.get('GITHUB_TOKEN'))
        commenters = github_client.fetch_issue_commenters(owner, repo_name, issue_number)
        
        # Update global state
        current_raffle['commenters'] = commenters
        current_raffle['repo_info'] = {
            'owner': owner,
            'repo': repo_name,
            'issue_number': issue_number
        }
        current_raffle['winner'] = None
        
        return jsonify({
            'success': True,
            'commenters': commenters,
            'count': len(commenters)
        })
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/select-winner', methods=['POST'])
def select_winner():
    """Select a random winner from the commenters"""
    try:
        if not current_raffle['commenters']:
            return jsonify({'error': 'No commenters available. Please fetch commenters first.'}), 400
        
        raffle_selector = RaffleSelector(current_raffle['commenters'])
        winner = raffle_selector.select_winner()
        
        # Update global state
        current_raffle['winner'] = winner
        
        return jsonify({
            'success': True,
            'winner': winner,
            'message': raffle_selector.get_winner_message(winner)
        })
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/raffle-state')
def get_raffle_state():
    """Get current raffle state"""
    return jsonify(current_raffle)

@app.route('/raffle', methods=['POST'])
def raffle():
    """Legacy route for form-based submission"""
    repo = request.form['repository']
    issue_number = request.form['issue_number']
    
    try:
        owner, repo_name = repo.split('/', 1)
        github_client = GitHubClient(token=os.environ.get('GITHUB_TOKEN'))
        commenters = github_client.fetch_issue_commenters(owner, repo_name, issue_number)
        
        raffle_selector = RaffleSelector(commenters)
        winner = raffle_selector.select_winner()
        
        return render_template('results.html', 
                             winner=winner, 
                             winner_name=winner,
                             commenters=commenters,
                             repo_info={'owner': owner, 'repo': repo_name, 'issue_number': issue_number})
    except Exception as e:
        return render_template('index.html', error=str(e))

if __name__ == '__main__':
    app.run(debug=True)
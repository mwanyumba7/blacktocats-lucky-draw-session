import os
from flask import Flask, render_template, request, jsonify, flash
from flask_cors import CORS
from dotenv import load_dotenv
from api.github_client import GitHubClient
from raffle.selection import RaffleSelector
from utils.helpers import (
    validate_repository_format, 
    parse_repository_url,
    validate_issue_number,
    filter_bot_users,
    generate_winner_announcement,
    sanitize_input
)

# Load environment variables from parent directory
load_dotenv(dotenv_path='../.env')

app = Flask(__name__, template_folder='../templates', static_folder='../static')
app.secret_key = os.getenv('FLASK_SECRET_KEY', 'dev-secret-key')
CORS(app)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/debug-env', methods=['GET'])
def debug_env():
    """Debug route to check environment variables (for development only)."""
    if not app.debug:
        return jsonify({'error': 'Debug mode only'}), 403
    
    token = os.getenv('GITHUB_TOKEN')
    return jsonify({
        'token_exists': bool(token),
        'token_prefix': token[:10] + '...' if token else 'None',
        'flask_secret_exists': bool(os.getenv('FLASK_SECRET_KEY')),
        'env_file_path': os.path.abspath('../.env'),
        'current_dir': os.getcwd()
    })

@app.route('/test-github-auth', methods=['POST'])
def test_github_auth():
    """Test GitHub API authentication."""
    try:
        # Debug: Check if token is loaded
        token = os.getenv('GITHUB_TOKEN')
        if not token:
            return jsonify({
                'status': 'error', 
                'message': 'GitHub token not found in environment variables. Please check your .env file.'
            }), 500
        
        # Debug: Check token format
        if not token.startswith('ghp_') and not token.startswith('github_pat_'):
            return jsonify({
                'status': 'error',
                'message': f'Invalid token format. Token should start with "ghp_" or "github_pat_", but starts with "{token[:10]}..."'
            }), 500
        
        github_client = GitHubClient()
        is_authenticated = github_client.test_authentication()
        
        if is_authenticated:
            try:
                user_info = github_client.get_authenticated_user()
                rate_limit = github_client.get_rate_limit_status()
                
                return jsonify({
                    'status': 'success', 
                    'message': f'GitHub API authentication successful! Connected as @{user_info.get("login", "unknown")}',
                    'user': user_info.get('login'),
                    'rate_limit': rate_limit.get('rate', {}).get('remaining', 'unknown')
                })
            except Exception as user_error:
                # Authentication works but getting user info failed
                return jsonify({
                    'status': 'success',
                    'message': f'GitHub API authentication successful! (Note: Could not fetch user details: {str(user_error)})',
                    'user': 'unknown',
                    'rate_limit': 'unknown'
                })
        else:
            return jsonify({
                'status': 'error', 
                'message': 'GitHub API authentication failed. The token may be invalid, expired, or have insufficient permissions.'
            }), 401
            
    except Exception as e:
        return jsonify({
            'status': 'error', 
            'message': f'GitHub API test failed: {str(e)}'
        }), 500

@app.route('/validate-repo', methods=['POST'])
def validate_repo():
    """Validate repository exists and is accessible."""
    try:
        data = request.get_json()
        repo = sanitize_input(data.get('repository', '').strip())
        
        # Try to parse as URL first, then validate format
        if repo.startswith('http'):
            repo = parse_repository_url(repo)
        
        if not repo or not validate_repository_format(repo):
            return jsonify({'status': 'error', 'message': 'Invalid repository format. Use owner/repository'}), 400
        
        github_client = GitHubClient()
        if github_client.validate_repository(repo):
            repo_info = github_client.get_repository_info(repo)
            return jsonify({
                'status': 'success',
                'message': f'Repository found: {repo_info.get("full_name")}',
                'repo_info': {
                    'name': repo_info.get('name'),
                    'full_name': repo_info.get('full_name'),
                    'description': repo_info.get('description'),
                    'stars': repo_info.get('stargazers_count'),
                    'is_private': repo_info.get('private', False)
                }
            })
        else:
            return jsonify({'status': 'error', 'message': 'Repository not found or not accessible'}), 404
            
    except Exception as e:
        return jsonify({'status': 'error', 'message': str(e)}), 500

@app.route('/preview-commenters', methods=['POST'])
def preview_commenters():
    """Preview commenters for an issue without selecting a winner."""
    try:
        data = request.get_json()
        repo = sanitize_input(data.get('repository', '').strip())
        issue_number_str = sanitize_input(str(data.get('issue_number', '')).strip())
        exclude_bots = data.get('exclude_bots', True)
        exclude_author = data.get('exclude_author', False)
        
        # Validate inputs
        if repo.startswith('http'):
            repo = parse_repository_url(repo)
        
        if not repo or not validate_repository_format(repo):
            return jsonify({'status': 'error', 'message': 'Invalid repository format'}), 400
        
        is_valid, issue_number = validate_issue_number(issue_number_str)
        if not is_valid:
            return jsonify({'status': 'error', 'message': 'Invalid issue number'}), 400
        
        github_client = GitHubClient()
        
        # Get issue info
        issue_info = github_client.get_issue_info(repo, issue_number)
        
        # Get commenters
        commenters = github_client.fetch_issue_commenters(repo, issue_number, exclude_author)
        
        # Filter bots if requested
        if exclude_bots:
            commenters = filter_bot_users(commenters)
        
        if not commenters:
            return jsonify({
                'status': 'warning', 
                'message': 'No eligible commenters found for this issue.',
                'issue_info': {
                    'title': issue_info.get('title'),
                    'author': issue_info.get('user', {}).get('login'),
                    'state': issue_info.get('state')
                }
            })
        
        return jsonify({
            'status': 'success',
            'message': f'Found {len(commenters)} eligible participant(s)',
            'commenters': commenters,
            'issue_info': {
                'title': issue_info.get('title'),
                'author': issue_info.get('user', {}).get('login'),
                'state': issue_info.get('state'),
                'url': issue_info.get('html_url')
            }
        })
        
    except Exception as e:
        return jsonify({'status': 'error', 'message': str(e)}), 500

@app.route('/raffle', methods=['POST'])
def raffle():
    """Conduct the raffle and select a winner."""
    repo = sanitize_input(request.form.get('repository', '').strip())
    issue_number_str = sanitize_input(request.form.get('issue_number', '').strip())
    exclude_bots = request.form.get('exclude_bots') == 'on'
    exclude_author = request.form.get('exclude_author') == 'on'
    
    # Validate inputs
    if repo.startswith('http'):
        repo = parse_repository_url(repo)
    
    if not repo or not validate_repository_format(repo):
        flash('Invalid repository format. Please use owner/repository format.', 'error')
        return render_template('index.html')
    
    is_valid, issue_number = validate_issue_number(issue_number_str)
    if not is_valid:
        flash('Issue number must be a valid positive integer.', 'error')
        return render_template('index.html')
    
    try:
        github_client = GitHubClient()
        
        # Get issue information
        issue_info = github_client.get_issue_info(repo, issue_number)
        
        # Fetch commenters
        commenters = github_client.fetch_issue_commenters(repo, issue_number, exclude_author)
        original_count = len(commenters)
        
        # Filter bots if requested
        if exclude_bots:
            commenters = filter_bot_users(commenters)
            
        if not commenters:
            flash('No eligible commenters found for this issue. Try including bots or the issue author.', 'warning')
            return render_template('index.html')
        
        # Create raffle selector with enhanced features
        exclude_users = []  # Could be extended to exclude specific users
        raffle_selector = RaffleSelector(commenters, exclude_users)
        
        # Select winner
        winner = raffle_selector.select_winner()
        
        if not winner:
            flash('Unable to select a winner. Please try again.', 'error')
            return render_template('index.html')
        
        # Generate winner announcement
        announcement = generate_winner_announcement(winner, repo, issue_number)
        
        # Get raffle statistics
        raffle_stats = raffle_selector.get_raffle_stats()
        
        return render_template('results.html',
            winner=winner,
            commenters=commenters,
            repo=repo,
            issue_number=issue_number,
            issue_info=issue_info,
            announcement=announcement,
            raffle_stats=raffle_stats,
            original_count=original_count,
            excluded_bots=exclude_bots,
            excluded_author=exclude_author
        )
        
    except Exception as e:
        flash(f'Error: {str(e)}', 'error')
        return render_template('index.html')

@app.route('/api/raffle-stats/<repo>/<int:issue_number>')
def get_raffle_stats(repo, issue_number):
    """Get raffle statistics for an issue."""
    try:
        github_client = GitHubClient()
        issue_info = github_client.get_issue_info(repo, issue_number)
        commenters = github_client.fetch_issue_commenters(repo, issue_number)
        
        return jsonify({
            'total_commenters': len(commenters),
            'issue_title': issue_info.get('title'),
            'issue_state': issue_info.get('state'),
            'issue_author': issue_info.get('user', {}).get('login')
        })
    except Exception as e:
        return jsonify({'error': str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True)
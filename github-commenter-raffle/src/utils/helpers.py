def format_commenter_data(commenters):
    formatted_data = []
    for commenter in commenters:
        formatted_data.append({
            'username': commenter['login'],
            'avatar_url': commenter['avatar_url'],
            'url': commenter['html_url']
        })
    return formatted_data

def get_random_winner(commenters):
    import random
    if not commenters:
        return None
    return random.choice(commenters)

def validate_commenter_data(commenters):
    return all('login' in commenter for commenter in commenters) and len(commenters) > 0
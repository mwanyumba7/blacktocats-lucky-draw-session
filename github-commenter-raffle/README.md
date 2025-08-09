# 🎉 GitHub Commenter Raffle

A dynamic and engaging web application that conducts raffles among GitHub issue commenters. Perfect for community events, giveaways, and interactive presentations!

## ✨ Features

- **GitHub API Integration**: Automatically fetch commenters from any public GitHub issue
- **Random Winner Selection**: Fair and transparent winner selection algorithm
- **Interactive UI**: Modern, responsive design with smooth animations
- **Confetti Animation**: Celebratory confetti effect when a winner is announced
- **Prominent Winner Display**: Winner's name is displayed prominently at the top
- **Participant Gallery**: View all participants with their GitHub avatars
- **Real-time State Management**: Maintains raffle state throughout the session
- **Error Handling**: Comprehensive error handling and user feedback

## 🚀 Quick Start

### Prerequisites

- Python 3.7 or higher
- Git
- A GitHub account (optional: GitHub token for higher API rate limits)

### Installation

1. **Clone the repository**
   ```bash
   git clone <repository-url>
   cd github-commenter-raffle
   ```

2. **Create a virtual environment**
   ```bash
   python -m venv raffle-env
   
   # On Windows
   raffle-env\Scripts\activate
   
   # On macOS/Linux
   source raffle-env/bin/activate
   ```

3. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

4. **Set up environment variables (optional)**
   ```bash
   # Copy the example environment file
   cp .env.example .env
   
   # Edit .env and add your GitHub token for higher rate limits
   # GITHUB_TOKEN=your_github_token_here
   ```

5. **Run the application**
   ```bash
   cd src
   python app.py
   ```

6. **Open your browser**
   Navigate to `http://localhost:5000`

## 🎯 How to Use

### For Event Organizers

1. **Create a GitHub Issue**: Create an issue in your repository asking people to comment to enter the raffle
2. **Launch the App**: Open the raffle application in your browser
3. **Enter Repository Details**: 
   - Repository: `owner/repository-name` (e.g., `octocat/Hello-World`)
   - Issue Number: The number of your raffle issue
4. **Fetch Commenters**: Click "Fetch Commenters" to load all participants
5. **Select Winner**: Click the "🎲 Select Winner" button for a dramatic winner selection
6. **Celebrate**: Watch the confetti animation and announce your winner!

### For Participants

1. **Find the Raffle Issue**: Look for the GitHub issue mentioned by the organizer
2. **Comment**: Add any comment to the issue to enter the raffle
3. **Wait for Results**: The organizer will run the raffle and announce the winner

## 🛠️ Technical Details

### Architecture

- **Backend**: Flask (Python)
  - RESTful API endpoints
  - GitHub API integration
  - Session state management
  
- **Frontend**: Vanilla JavaScript + HTML5 + CSS3
  - Responsive design
  - Canvas-based confetti animation
  - Modern CSS Grid and Flexbox layouts
  
- **GitHub API**: 
  - Fetches issue comments
  - Retrieves commenter information
  - Handles rate limiting gracefully

### API Endpoints

- `GET /` - Main raffle interface
- `POST /api/fetch-commenters` - Fetch commenters from GitHub issue
- `POST /api/select-winner` - Randomly select a winner
- `GET /api/raffle-state` - Get current raffle state
- `POST /raffle` - Legacy form-based raffle (for direct submissions)

### File Structure

```
github-commenter-raffle/
├── src/
│   ├── app.py                 # Main Flask application
│   ├── api/
│   │   ├── __init__.py
│   │   └── github_client.py   # GitHub API client
│   ├── raffle/
│   │   ├── __init__.py
│   │   └── selection.py       # Winner selection logic
│   ├── ui/
│   │   ├── __init__.py
│   │   ├── animations.py      # UI animations (reserved)
│   │   └── components.py      # UI components (reserved)
│   └── utils/
│       ├── __init__.py
│       └── helpers.py         # Utility functions
├── static/
│   ├── css/
│   │   └── style.css          # Comprehensive styling
│   └── js/
│       └── main.js            # Main application logic
├── templates/
│   ├── base.html              # Base template (reserved)
│   ├── index.html             # Main raffle interface
│   └── results.html           # Winner announcement page
├── tests/                     # Test suite
├── requirements.txt           # Python dependencies
└── README.md                  # This file
```

## 🎨 Customization

### Styling
Edit `static/css/style.css` to customize:
- Color schemes
- Animations
- Layout
- Typography

### Confetti Animation
Modify the `GitHubRaffleApp` class in `static/js/main.js`:
- Change colors: Update `getRandomColor()` method
- Adjust particle count: Modify confetti piece generation
- Change duration: Update timeout in `startConfetti()`

### Winner Selection
Edit `src/raffle/selection.py` to:
- Implement weighted selection
- Add exclusion lists
- Create custom selection algorithms

## 🔧 Configuration

### Environment Variables

| Variable | Description | Required |
|----------|-------------|----------|
| `GITHUB_TOKEN` | GitHub personal access token | No* |
| `SECRET_KEY` | Flask session secret key | Yes |
| `FLASK_ENV` | Flask environment (development/production) | No |
| `FLASK_DEBUG` | Enable Flask debug mode | No |

*Note: While not required, a GitHub token is highly recommended to avoid rate limiting.

### GitHub Token Setup

1. Go to [GitHub Settings > Developer settings > Personal access tokens](https://github.com/settings/tokens)
2. Click "Generate new token"
3. Select scopes: `public_repo` (for public repositories)
4. Copy the token and add it to your `.env` file

## 🚀 Deployment

### Local Development
```bash
cd src
python app.py
```

### Production Deployment

#### Using Gunicorn
```bash
cd src
gunicorn --bind 0.0.0.0:8000 app:app
```

#### Using Docker
```dockerfile
FROM python:3.9-slim
WORKDIR /app
COPY requirements.txt .
RUN pip install -r requirements.txt
COPY . .
EXPOSE 5000
CMD ["python", "src/app.py"]
```

## 🧪 Testing

Run the test suite:
```bash
python -m pytest tests/
```

Run specific tests:
```bash
python -m pytest tests/test_github_client.py
python -m pytest tests/test_selection.py
```

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch: `git checkout -b feature/amazing-feature`
3. Commit your changes: `git commit -m 'Add amazing feature'`
4. Push to the branch: `git push origin feature/amazing-feature`
5. Open a Pull Request

## 📝 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 🎭 Demo Usage

Perfect for:
- **Tech Conferences**: Live winner selection during presentations
- **Community Events**: GitHub-based giveaways
- **Open Source Projects**: Contributor appreciation raffles
- **Meetups**: Interactive audience engagement
- **Hackathons**: Prize distribution

## 🛟 Troubleshooting

### Common Issues

**"Error fetching commenters: 403"**
- You've hit GitHub's rate limit
- Add a GitHub token to your environment variables

**"No commenters found"**
- Verify the repository and issue number are correct
- Ensure the issue has comments
- Check if the repository is public

**"Repository format should be owner/repo"**
- Use the format: `username/repository-name`
- Example: `octocat/Hello-World`

### Support

If you encounter issues:
1. Check the browser console for JavaScript errors
2. Review the Flask application logs
3. Verify your GitHub token has the correct permissions
4. Ensure all dependencies are installed correctly

## 🌟 Acknowledgments

- GitHub API for providing excellent developer tools
- Flask community for the robust web framework
- Open source contributors who make projects like this possible

---

Made with ❤️ for the GitHub community. Happy raffling! 🎉

## Project Structure

```
github-commenter-raffle
├── src
│   ├── app.py                # Main entry point of the application
│   ├── api                   # Contains API client for GitHub
│   │   ├── __init__.py
│   │   └── github_client.py   # GitHub API client
│   ├── raffle                # Raffle logic and winner selection
│   │   ├── __init__.py
│   │   └── selection.py       # Winner selection logic
│   ├── ui                    # User interface components and animations
│   │   ├── __init__.py
│   │   ├── animations.py      # Animation functions
│   │   └── components.py      # UI components
│   └── utils                 # Utility functions
│       ├── __init__.py
│       └── helpers.py        # Helper functions
├── static                    # Static files (CSS and JS)
│   ├── css
│   │   └── style.css         # Styles for the application
│   └── js
│       └── main.js           # Client-side JavaScript
├── templates                 # HTML templates
│   ├── base.html             # Base template
│   ├── index.html            # Main template for the application
│   └── results.html          # Results template
├── tests                     # Unit tests
│   ├── __init__.py
│   ├── test_github_client.py  # Tests for GitHubClient
│   └── test_selection.py      # Tests for RaffleSelector
├── .gitignore                # Git ignore file
├── requirements.txt          # Project dependencies
├── setup.py                  # Setup script for the project
└── README.md                 # Project documentation
```

## Installation

1. Clone the repository:
   ```
   git clone https://github.com/yourusername/github-commenter-raffle.git
   cd github-commenter-raffle
   ```

2. Install the required dependencies:
   ```
   pip install -r requirements.txt
   ```

## Usage

1. Run the application:
   ```
   python src/app.py
   ```

2. Open your web browser and navigate to `http://localhost:5000` to access the application.

3. Enter the GitHub issue URL to fetch commenters and start the raffle!

## Contributing

Contributions are welcome! Please open an issue or submit a pull request for any enhancements or bug fixes.

## License

This project is licensed under the MIT License. See the LICENSE file for more details.

## Acknowledgments

- Thanks to GitHub for providing a powerful API.
- Special thanks to the community for their support and feedback!
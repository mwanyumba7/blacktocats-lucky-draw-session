# GitHub Commenter Raffle

Welcome to the GitHub Commenter Raffle project! This application allows you to randomly select a winner from the commenters of a specified GitHub issue. The winner will receive a special prize, such as a Mona plushie!

## Features

- Fetches issue commenters from the GitHub API.
- Implements a dynamic winner selection process with engaging animations.
- User-friendly interface for initiating the raffle and displaying results.

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
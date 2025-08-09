class GitHubRaffleApp {
    constructor() {
        this.commenters = [];
        this.winner = null;
        this.confettiAnimation = null;
        this.init();
    }

    init() {
        this.bindEvents();
        this.setupConfetti();
    }

    bindEvents() {
        // Form submission for fetching commenters
        const raffleForm = document.getElementById('raffle-form');
        raffleForm.addEventListener('submit', (e) => {
            e.preventDefault();
            this.fetchCommenters();
        });

        // Select winner button
        const selectWinnerBtn = document.getElementById('select-winner-btn');
        selectWinnerBtn.addEventListener('click', () => {
            this.selectWinner();
        });

        // New raffle button
        const newRaffleBtn = document.getElementById('new-raffle-btn');
        newRaffleBtn.addEventListener('click', () => {
            this.startNewRaffle();
        });

        // Error dismiss button
        const dismissErrorBtn = document.getElementById('dismiss-error');
        dismissErrorBtn.addEventListener('click', () => {
            this.hideError();
        });
    }

    async fetchCommenters() {
        const repository = document.getElementById('repository').value.trim();
        const issueNumber = document.getElementById('issue_number').value.trim();

        if (!repository || !issueNumber) {
            this.showError('Please fill in both repository and issue number');
            return;
        }

        this.showLoading(true);
        this.hideError();

        try {
            const response = await fetch('/api/fetch-commenters', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify({
                    repository: repository,
                    issue_number: parseInt(issueNumber)
                })
            });

            const data = await response.json();

            if (!response.ok) {
                throw new Error(data.error || 'Failed to fetch commenters');
            }

            this.commenters = data.commenters;
            this.displayCommenters(data.commenters);
            this.showCommentersSection();

        } catch (error) {
            this.showError(`Error: ${error.message}`);
        } finally {
            this.showLoading(false);
        }
    }

    displayCommenters(commenters) {
        const commentersList = document.getElementById('commenters-list');
        const commentersCount = document.getElementById('commenters-count');
        
        commentersCount.textContent = commenters.length;
        
        commentersList.innerHTML = '';
        
        commenters.forEach(commenter => {
            const commenterItem = document.createElement('div');
            commenterItem.className = 'commenter-item';
            commenterItem.innerHTML = `
                <img src="https://github.com/${commenter}.png?size=40" 
                     alt="${commenter}" class="commenter-avatar"
                     onerror="this.src='https://github.com/github.png?size=40'">
                <div class="commenter-name">@${commenter}</div>
            `;
            commentersList.appendChild(commenterItem);
        });
    }

    async selectWinner() {
        if (this.commenters.length === 0) {
            this.showError('No commenters available. Please fetch commenters first.');
            return;
        }

        this.showLoading(true);

        try {
            // Add some suspense with a delay
            await this.animateSelection();

            const response = await fetch('/api/select-winner', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                }
            });

            const data = await response.json();

            if (!response.ok) {
                throw new Error(data.error || 'Failed to select winner');
            }

            this.winner = data.winner;
            this.displayWinner(data.winner);
            this.startConfetti();

        } catch (error) {
            this.showError(`Error: ${error.message}`);
        } finally {
            this.showLoading(false);
        }
    }

    async animateSelection() {
        const selectWinnerBtn = document.getElementById('select-winner-btn');
        const originalText = selectWinnerBtn.textContent;
        
        const animationTexts = ['🎲 Selecting...', '🔄 Randomizing...', '🎯 Picking winner...'];
        
        for (let i = 0; i < 3; i++) {
            for (const text of animationTexts) {
                selectWinnerBtn.textContent = text;
                await this.sleep(300);
            }
        }
        
        selectWinnerBtn.textContent = originalText;
    }

    displayWinner(winner) {
        const winnerDisplay = document.getElementById('winner-display');
        const winnerNameDisplay = document.getElementById('winner-name-display');
        
        winnerNameDisplay.textContent = `@${winner}`;
        winnerDisplay.classList.remove('hidden');
        winnerDisplay.classList.add('fade-in');
        
        // Scroll to top to show winner
        winnerDisplay.scrollIntoView({ behavior: 'smooth', block: 'start' });
        
        // Hide other sections
        document.getElementById('commenters-section').style.opacity = '0.5';
    }

    startNewRaffle() {
        // Reset state
        this.commenters = [];
        this.winner = null;
        
        // Reset form
        document.getElementById('raffle-form').reset();
        
        // Hide sections
        document.getElementById('winner-display').classList.add('hidden');
        document.getElementById('commenters-section').classList.add('hidden');
        document.getElementById('commenters-section').style.opacity = '1';
        
        // Stop confetti
        this.stopConfetti();
        
        // Focus on repository input
        document.getElementById('repository').focus();
    }

    showCommentersSection() {
        const section = document.getElementById('commenters-section');
        section.classList.remove('hidden');
        section.classList.add('fade-in');
    }

    showLoading(show) {
        const loading = document.getElementById('loading');
        if (show) {
            loading.classList.remove('hidden');
        } else {
            loading.classList.add('hidden');
        }
    }

    showError(message) {
        const errorDisplay = document.getElementById('error-display');
        const errorMessage = document.getElementById('error-message');
        
        errorMessage.textContent = message;
        errorDisplay.classList.remove('hidden');
        errorDisplay.scrollIntoView({ behavior: 'smooth' });
    }

    hideError() {
        const errorDisplay = document.getElementById('error-display');
        errorDisplay.classList.add('hidden');
    }

    sleep(ms) {
        return new Promise(resolve => setTimeout(resolve, ms));
    }

    // Confetti Animation
    setupConfetti() {
        this.canvas = document.getElementById('confetti-canvas');
        this.ctx = this.canvas.getContext('2d');
        this.confettiPieces = [];
        
        this.resizeCanvas();
        window.addEventListener('resize', () => this.resizeCanvas());
    }

    resizeCanvas() {
        this.canvas.width = window.innerWidth;
        this.canvas.height = window.innerHeight;
    }

    createConfettiPiece() {
        return {
            x: Math.random() * this.canvas.width,
            y: -10,
            width: Math.random() * 8 + 5,
            height: Math.random() * 8 + 5,
            color: this.getRandomColor(),
            rotation: Math.random() * 360,
            rotationSpeed: Math.random() * 5 + 2,
            velocityX: Math.random() * 4 - 2,
            velocityY: Math.random() * 3 + 2,
            gravity: 0.1
        };
    }

    getRandomColor() {
        const colors = [
            '#ff6b6b', '#4ecdc4', '#45b7d1', '#96ceb4', '#feca57',
            '#ff9ff3', '#54a0ff', '#5f27cd', '#00d2d3', '#ff9f43'
        ];
        return colors[Math.floor(Math.random() * colors.length)];
    }

    updateConfetti() {
        this.ctx.clearRect(0, 0, this.canvas.width, this.canvas.height);
        
        for (let i = this.confettiPieces.length - 1; i >= 0; i--) {
            const piece = this.confettiPieces[i];
            
            piece.x += piece.velocityX;
            piece.y += piece.velocityY;
            piece.velocityY += piece.gravity;
            piece.rotation += piece.rotationSpeed;
            
            this.ctx.save();
            this.ctx.translate(piece.x + piece.width / 2, piece.y + piece.height / 2);
            this.ctx.rotate(piece.rotation * Math.PI / 180);
            this.ctx.fillStyle = piece.color;
            this.ctx.fillRect(-piece.width / 2, -piece.height / 2, piece.width, piece.height);
            this.ctx.restore();
            
            if (piece.y > this.canvas.height + 10) {
                this.confettiPieces.splice(i, 1);
            }
        }
        
        // Add new confetti pieces
        if (this.confettiPieces.length < 100) {
            for (let i = 0; i < 3; i++) {
                this.confettiPieces.push(this.createConfettiPiece());
            }
        }
    }

    startConfetti() {
        if (this.confettiAnimation) {
            cancelAnimationFrame(this.confettiAnimation);
        }
        
        const animate = () => {
            this.updateConfetti();
            this.confettiAnimation = requestAnimationFrame(animate);
        };
        
        animate();
        
        // Stop confetti after 10 seconds
        setTimeout(() => {
            this.stopConfetti();
        }, 10000);
    }

    stopConfetti() {
        if (this.confettiAnimation) {
            cancelAnimationFrame(this.confettiAnimation);
            this.confettiAnimation = null;
        }
        this.confettiPieces = [];
        this.ctx.clearRect(0, 0, this.canvas.width, this.canvas.height);
    }
}

// Initialize the app when DOM is loaded
document.addEventListener('DOMContentLoaded', () => {
    new GitHubRaffleApp();
});
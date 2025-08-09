document.addEventListener('DOMContentLoaded', () => {
    const raffleButton = document.getElementById('raffle-button');
    const resultContainer = document.getElementById('result-container');

    raffleButton.addEventListener('click', async () => {
        const commenters = await fetchCommenters();
        const winner = selectWinner(commenters);
        displayWinner(winner);
    });

    async function fetchCommenters() {
        const response = await fetch('/api/commenters');
        if (!response.ok) {
            throw new Error('Network response was not ok');
        }
        return await response.json();
    }

    function selectWinner(commenters) {
        const randomIndex = Math.floor(Math.random() * commenters.length);
        return commenters[randomIndex];
    }

    function displayWinner(winner) {
        resultContainer.innerHTML = `<h2>Congratulations, ${winner}!</h2>`;
        animateWinnerAnnouncement();
    }

    function animateWinnerAnnouncement() {
        resultContainer.classList.add('animate');
        setTimeout(() => {
            resultContainer.classList.remove('animate');
        }, 3000);
    }
});
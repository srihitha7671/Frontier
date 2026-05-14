async function playGame(choice) {
    const playerName = document.getElementById('playerName').value;
    
    if (!playerName.trim()) {
        alert('Please enter your name!');
        return;
    }
    
    try {
        const response = await fetch('/api/play', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({
                playerName: playerName,
                choice: choice
            })
        });
        
        const data = await response.json();
        displayResult(data);
        loadLeaderboard();
    } catch (error) {
        console.error('Error:', error);
        alert('An error occurred!');
    }
}

function displayResult(data) {
    const resultDiv = document.getElementById('result');
    let resultText = '';
    let resultColor = '';
    
    if (data.result === 'win') {
        resultText = '🎉 You Won!';
        resultColor = 'green';
    } else if (data.result === 'loss') {
        resultText = '😢 You Lost!';
        resultColor = 'red';
    } else {
        resultText = '🤝 Draw!';
        resultColor = 'blue';
    }
    
    resultDiv.innerHTML = `
        <h3 style="color: ${resultColor}">${resultText}</h3>
        <p>Your choice: ${data.playerChoice}</p>
        <p>Computer choice: ${data.computerChoice}</p>
    `;
}

async function loadLeaderboard() {
    try {
        const response = await fetch('/api/leaderboard');
        const data = await response.json();
        const leaderboardDiv = document.getElementById('leaderboard');
        // VULNERABILITY: XSS - innerHTML allows script injection
        leaderboardDiv.innerHTML = data.leaderboard;
    } catch (error) {
        console.error('Error loading leaderboard:', error);
    }
}

async function resetDatabase() {
    if (confirm('Are you sure you want to reset the database? This cannot be undone!')) {
        try {
            const response = await fetch('/api/reset', {
                method: 'POST'
            });
            const data = await response.json();
            alert(data.message || data.error);
            loadLeaderboard();
        } catch (error) {
            console.error('Error:', error);
            alert('An error occurred!');
        }
    }
}

// Load leaderboard on page load
window.addEventListener('load', loadLeaderboard);

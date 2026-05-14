# 🎮 Rock Paper Scissors Game

A simple web-based Rock Paper Scissors game built with Flask and SQLite.

## Features

- 🎯 Play Rock Paper Scissors against the computer
- 📊 Track your win/loss/draw statistics
- 🏆 View top 10 players on the leaderboard
- 💾 Persistent game data with SQLite
- 🎨 Beautiful responsive UI

## Tech Stack

- **Backend**: Flask (Python)
- **Frontend**: HTML5, CSS3, JavaScript
- **Database**: SQLite3

## Installation

1. Clone the repository:
   ```bash
   git clone https://github.com/srihitha7671/frontier.git
   cd frontier
   ```

2. Create a virtual environment:
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

4. Run the application:
   ```bash
   python app.py
   ```

5. Open your browser and go to:
   ```
   http://localhost:5000
   ```

## How to Play

1. Enter your name
2. Choose Rock, Paper, or Scissors
3. The computer makes a random choice
4. The result is displayed and your stats are updated
5. Check the leaderboard to see how you rank

## ⚠️ Security Vulnerabilities (Educational Purpose)

This project intentionally contains security vulnerabilities for learning purposes:

1. **SQL Injection** - User input is directly inserted into SQL queries
2. **Cross-Site Scripting (XSS)** - Leaderboard data is not HTML-escaped
3. **Hardcoded Credentials** - Admin credentials are hardcoded in the source
4. **No Authentication** - Reset endpoint requires no authentication
5. **Debug Mode Enabled** - Flask is running in debug mode
6. **No CSRF Protection** - State-changing operations have no CSRF tokens

### Do NOT use this code in production!

## Learning Resources

- [OWASP Top 10](https://owasp.org/www-project-top-ten/)
- [SQL Injection Prevention](https://owasp.org/www-community/attacks/SQL_Injection)
- [XSS Prevention](https://owasp.org/www-community/attacks/xss/)

## License

MIT License

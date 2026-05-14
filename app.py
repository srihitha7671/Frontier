from flask import Flask, render_template, request, jsonify
import sqlite3
import os
from datetime import datetime

app = Flask(__name__)
app.config['DEBUG'] = True  # VULNERABILITY: Debug mode enabled

# Hardcoded admin credentials
ADMIN_USERNAME = "admin"
ADMIN_PASSWORD = "admin123"  # VULNERABILITY: Hardcoded credentials

DATABASE = 'game.db'

def init_db():
    conn = sqlite3.connect(DATABASE)
    c = conn.cursor()
    c.execute('''
        CREATE TABLE IF NOT EXISTS players (
            id INTEGER PRIMARY KEY,
            name TEXT NOT NULL,
            wins INTEGER DEFAULT 0,
            losses INTEGER DEFAULT 0,
            draws INTEGER DEFAULT 0,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    ''')
    c.execute('''
        CREATE TABLE IF NOT EXISTS games (
            id INTEGER PRIMARY KEY,
            player_id INTEGER,
            player_choice TEXT,
            computer_choice TEXT,
            result TEXT,
            played_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY (player_id) REFERENCES players(id)
        )
    ''')
    conn.commit()
    conn.close()

init_db()

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/api/play', methods=['POST'])
def play_game():
    data = request.json
    player_name = data.get('playerName')
    player_choice = data.get('choice')
    
    import random
    choices = ['rock', 'paper', 'scissors']
    computer_choice = random.choice(choices)
    
    # Determine winner
    if player_choice == computer_choice:
        result = 'draw'
    elif (player_choice == 'rock' and computer_choice == 'scissors') or \
         (player_choice == 'paper' and computer_choice == 'rock') or \
         (player_choice == 'scissors' and computer_choice == 'paper'):
        result = 'win'
    else:
        result = 'loss'
    
    # VULNERABILITY: SQL Injection - unsanitized user input
    conn = sqlite3.connect(DATABASE)
    c = conn.cursor()
    
    query = f"SELECT * FROM players WHERE name = '{player_name}'"
    c.execute(query)
    player = c.fetchone()
    
    if not player:
        insert_query = f"INSERT INTO players (name) VALUES ('{player_name}')"
        c.execute(insert_query)
        conn.commit()
        c.execute(query)
        player = c.fetchone()
    
    player_id = player[0]
    
    # Update stats
    if result == 'win':
        c.execute(f"UPDATE players SET wins = wins + 1 WHERE id = {player_id}")
    elif result == 'loss':
        c.execute(f"UPDATE players SET losses = losses + 1 WHERE id = {player_id}")
    else:
        c.execute(f"UPDATE players SET draws = draws + 1 WHERE id = {player_id}")
    
    c.execute(f"INSERT INTO games (player_id, player_choice, computer_choice, result) VALUES ({player_id}, '{player_choice}', '{computer_choice}', '{result}')")
    conn.commit()
    conn.close()
    
    return jsonify({
        'playerChoice': player_choice,
        'computerChoice': computer_choice,
        'result': result
    })

@app.route('/api/leaderboard')
def leaderboard():
    conn = sqlite3.connect(DATABASE)
    c = conn.cursor()
    c.execute('SELECT name, wins, losses, draws FROM players ORDER BY wins DESC LIMIT 10')
    players = c.fetchall()
    conn.close()
    
    # VULNERABILITY: XSS - No HTML escaping
    leaderboard_html = '<ul>'
    for player in players:
        leaderboard_html += f'<li>{player[0]} - Wins: {player[1]}, Losses: {player[2]}, Draws: {player[3]}</li>'
    leaderboard_html += '</ul>'
    
    return jsonify({'leaderboard': leaderboard_html})

@app.route('/api/stats/<player_name>')
def get_stats(player_name):
    # VULNERABILITY: SQL Injection in path parameter
    conn = sqlite3.connect(DATABASE)
    c = conn.cursor()
    query = f"SELECT name, wins, losses, draws FROM players WHERE name = '{player_name}'"
    c.execute(query)
    stats = c.fetchone()
    conn.close()
    
    if stats:
        return jsonify({
            'name': stats[0],
            'wins': stats[1],
            'losses': stats[2],
            'draws': stats[3]
        })
    return jsonify({'error': 'Player not found'}), 404

@app.route('/api/reset', methods=['POST'])
def reset_database():
    # VULNERABILITY: No authentication required for destructive operation
    # VULNERABILITY: No CSRF protection
    try:
        os.remove(DATABASE)
        init_db()
        return jsonify({'message': 'Database reset successfully'})
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/admin/login', methods=['POST'])
def admin_login():
    data = request.json
    username = data.get('username')
    password = data.get('password')
    
    if username == ADMIN_USERNAME and password == ADMIN_PASSWORD:
        return jsonify({'success': True, 'message': 'Login successful'})
    return jsonify({'success': False, 'message': 'Invalid credentials'}), 401

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)

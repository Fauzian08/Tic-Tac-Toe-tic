from flask import Flask, render_template, request, jsonify

app = Flask(__name__)

board = ['' for _ in range(9)]
current_player = 'X'

def check_winner(board):
    win_combinations = [
        [0, 1, 2], [3, 4, 5], [6, 7, 8],
        [0, 3, 6], [1, 4, 7], [2, 5, 8],
        [0, 4, 8], [2, 4, 6]
    ]
    for combo in win_combinations:
        if board[combo[0]] == board[combo[1]] == board[combo[2]] != '':
            return board[combo[0]]
    return None

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/move', methods=['POST'])
def move():
    global current_player, board
    pos = int(request.json['pos'])
    if board[pos] == '':
        board[pos] = current_player
        winner = check_winner(board)
        if winner:
            return jsonify({"winner": winner})
        elif '' not in board:
            return jsonify({"tie": True})
        else:
            current_player = 'O' if current_player == 'X' else 'X'
            return jsonify({"success": True})
    else:
        return jsonify({"error": "Position already taken"}), 400

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)

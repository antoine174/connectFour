from flask import Flask, jsonify, request
from flask_cors import CORS

from board import Board
from heuristic import evaluate_board
from minimax import find_best_move

app = Flask(__name__)
CORS(app)

game = {"board": Board(), "k": 4, "first_player": Board.HUMAN, "over": False}


def build_response(ai_move=None, search_tree=None, stats=None):
    board = game["board"]
    score, breakdown = evaluate_board(board)
    game_over = board.is_full()
    human_score = board.count_connected_fours(Board.HUMAN)
    ai_score = board.count_connected_fours(Board.AI)
    winner = None
    if game_over:
        winner = "human" if human_score > ai_score else "ai" if ai_score > human_score else "draw"
    return jsonify({
        "board": board.to_matrix(),
        "ai_move": ai_move,
        "human_score": human_score,
        "ai_score": ai_score,
        "discs_played": board.disc_count,
        "current_heuristic": score,
        "heuristic_breakdown": breakdown,
        "stats": stats,
        "game_over": game_over,
        "winner": winner,
        "search_tree": search_tree,
    })


def play_ai_turn():
    board = game["board"]
    col, root, stats = find_best_move(board, game["k"])
    board.drop_piece(col, Board.AI)
    return col, root.to_dict(), stats


@app.post("/api/new-game")
def new_game():
    data = request.get_json(silent=True) or {}
    k = int(data.get("k", 4))
    if not 1 <= k <= 10:
        return jsonify({"error": "k must be between 1 and 10"}), 400
    first = Board.AI if data.get("first_player") == "ai" else Board.HUMAN

    game.update(board=Board(), k=k, first_player=first)
    if first == Board.AI:
        col, tree, stats = play_ai_turn()
        return build_response(ai_move=col, search_tree=tree, stats=stats)
    return build_response()


@app.post("/api/move")
def move():
    board = game["board"]
    data = request.get_json(silent=True) or {}
    col = data.get("col")
    if board.is_full():
        return jsonify({"error": "game is over"}), 400
    if not isinstance(col, int) or not 0 <= col < Board.COLS or board.get_next_open_row(col) == -1:
        return jsonify({"error": "invalid column"}), 400

    board.drop_piece(col, Board.HUMAN)
    if board.is_full():
        return build_response()

    ai_col, tree, stats = play_ai_turn()
    return build_response(ai_move=ai_col, search_tree=tree, stats=stats)


if __name__ == "__main__":
    app.run(port=5000, debug=False)

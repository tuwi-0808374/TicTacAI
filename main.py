from flask import *

from lib.ai_manager import AIManager

app = Flask(__name__)
@app.route('/')
def home_page():
    return render_template('home.html')

@app.route('/game')
def game_page():
    return render_template('game.html')

@app.route('/api/get_next_move', methods=['POST'])
def get_next_move():
    print(request)
    if request.method == 'POST':
        print(request.json)
        ai = AIManager()

        prompt = f"""
            Play a 5x5 Tic-Tac-Toe variant as '1' (AI). Rules:
                    - Grid uses ONLY numeric values: '0' (empty), '1' (AI), '2' (opponent).
                    - Place ONE numeric '1' in any empty '0' cell.
                    - Prioritize winning (four '1's in a row, column, or diagonal).
                    - If no win, block opponent (four '2's in a row, column, or diagonal).
                    - If neither, choose an empty '0' cell, preferring central positions (e.g., row 2, column 2).
                    - Output ONLY a 5x5 grid in JSON format as an array of arrays (e.g., [[0,0,0,0,0],[0,0,0,0,0],[0,0,0,0,0],[0,0,0,0,0],[0,0,0,0,0]]), using ONLY numeric values (0, 1, 2), no strings, no extra text, no other numbers (e.g., no '3'), no object keys (e.g., no {{"grid": [...]}}).
                    - Use compact JSON: no indentation, no newlines, no extra spaces.
                    - You MUST place a new '1' in an empty '0' cell and MUST NOT repeat the input grid.
            """
        response = ai.get_next_move(request.json, prompt, "gemini-2.5-flash-lite", 10, 50)
        # response = ai.get_next_move(request.json, prompt, "random", 10, 50)
        # response = ai.get_next_move(request.json, prompt, "llama3.1:8b", 10, 50)

        return response, 200
    else:
        print(2)


if __name__ == "__main__":
    app.run(debug=True)
from flask import *

import data
from lib.ai_manager import AIManager
from data import *
from lib.game_manager import GameManager

game_manager = GameManager()
app = Flask(__name__)
@app.route('/')
def home_page():
    return render_template('home.html')

@app.route('/game')
def game_page():
    return render_template('game.html', possible_models = model_data)

@app.route('/api/get_next_move', methods=['POST'])
def get_next_move():
    if request.method == 'POST':
        print(request.json)
        ai = AIManager()

        prompt = data.prompt_data["default"]

        grid = request.get_json()['grid']

        who_won = game_manager.check_win(grid)
        if who_won == 1:
            print("ai win")
            game_manager.restart_game()
        elif who_won == 2:
            print("player win")
            game_manager.restart_game()
        else:
            game_manager.next_turn()

        model_name = request.get_json()['model']

        if model_name not in data.model_data:
            return jsonify({'error': 'Model not found'}), 400

        ai_model = data.model_data[model_name]["ai_model"]
        api_name = data.model_data[model_name]["api_name"]

        new_grid, response_time, model_name, attempt = ai.get_next_move(grid, prompt, api_name, ai_model)

        response = jsonify(
            {'grid': new_grid,
             'response_time': response_time,
             'attempt': attempt,
             'api_name': api_name,
             'winner': who_won}
        )

        print(response.get_json())

        return response, 200


if __name__ == "__main__":
    app.run(debug=True)
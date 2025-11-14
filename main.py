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
        ai = AIManager()

        prompt = data.prompt_data["default"]

        grid = request.get_json()['grid']

        model_name = request.get_json()['model']
        if model_name not in data.model_data:
            return jsonify({'error': 'Model not found'}), 400
        ai_model = data.model_data[model_name]["ai_model"]
        api_name = data.model_data[model_name]["api_name"]

        who_won = game_manager.check_win(grid)
        response = {
            'turn': game_manager.get_current_turn(),
            'who_won': who_won,
            'api_name': api_name,
        }

        if who_won == 0:

            new_grid, response_time, model_name, attempt = ai.get_next_move(grid, prompt, api_name, ai_model)

            who_won = game_manager.check_win(new_grid)
            response.update({
                'grid': new_grid,
                'response_time': response_time,
                'attempt': attempt,
                'who_won': who_won
            })

            game_manager.next_turn()

        if who_won != 0:
            game_manager.restart_game()

        print(response)

        return jsonify(response), 200


if __name__ == "__main__":
    app.run(debug=True)
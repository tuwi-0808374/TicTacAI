from flask import *

import data
from lib.ai_manager import AIManager
from data import *
from lib.game_manager import GameManager
from lib.statistics import Statistics

game_manager = GameManager()
app = Flask(__name__)
@app.route('/')
def home_page():
    return redirect('game')

@app.route('/stats')
def stats():
    return render_template('stats.html')

@app.route('/api/stats/most_used_models')
def most_used_models():
    stats = Statistics()
    response = jsonify(stats.get_most_used_models())
    return response, 200

@app.route('/api/stats/winning_models')
def winning_models():
    stats = Statistics()
    response = jsonify(stats.get_winning_model())
    return response, 200

@app.route('/api/stats/user_vs_ai')
def user_vs_ai():
    stats = Statistics()
    response = jsonify(stats.get_user_vs_ai())
    return response, 200

@app.route('/game')
def game_page():
    return render_template('game.html', possible_models = model_data)

@app.route('/api/get_next_move', methods=['POST'])
def get_next_move():
    if request.method == 'POST':
        ai = AIManager()

        prompt_title = "default"
        prompt = data.prompt_data[prompt_title]

        grid = request.get_json()['grid']

        model_name = request.get_json()['model']
        if model_name not in data.model_data:
            return jsonify({'error': 'Model not found'}), 400
        ai_model = data.model_data[model_name]["ai_model"]
        api_name = data.model_data[model_name]["api_name"]

        who_won = game_manager.check_win(grid)
        response = {
            'turn': game_manager.get_current_turn(),
            'winner': who_won,
            'model': api_name,
            'prompt': prompt_title,
            'grid': grid,
        }

        if who_won == 0:
            new_grid, model_name, attempts = ai.get_next_move(grid, prompt, api_name, ai_model)

            who_won = game_manager.check_win(new_grid)
            response.update({
                'grid': new_grid,
                'attempt': attempts,
                'winner': who_won
            })

            game_manager.next_turn()

        game_manager.add_move(response)

        if who_won != 0:
            print(f"History of the the game: {game_manager.moves}")
            game_manager.save_move()
            game_manager.restart_game()

        # print(response)

        return jsonify(response), 200


if __name__ == "__main__":
    app.run(debug=True)
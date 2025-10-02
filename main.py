from flask import *

import data
from lib.ai_manager import AIManager
from data import *

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
        model_name = request.get_json()['model']

        if model_name not in data.model_data:
            return jsonify({'error': 'Model not found'}), 400

        ai_model = data.model_data[model_name]["ai_model"]

        new_grid, response_time, model_name = ai.get_next_move(grid, prompt, model_name, ai_model)
        response = jsonify({'grid': new_grid, 'response_time': response_time, 'model_name': model_name})

        return response, 200


if __name__ == "__main__":
    app.run(debug=True)
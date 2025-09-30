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
        model = request.get_json()['model']

        if model not in data.model_data:
            return jsonify({'error': 'Model not found'}), 400

        response = ai.get_next_move(grid, prompt, model)

        return response, 200


if __name__ == "__main__":
    app.run(debug=True)
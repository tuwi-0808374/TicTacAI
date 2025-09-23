from flask import *

from lib.ai_manager import AIManager

app = Flask(__name__)

@app.route('/')
def home_page():
    return render_template('home.html')

@app.route('/api/get_next_move', methods=['POST'])
def get_next_move():
    print(request)
    if request.method == 'POST':
        print(request.json)
        ai = AIManager()
        response = ai.get_next_move(request.json)
        return response, 200
    else:
        print(2)


if __name__ == "__main__":
    app.run(debug=True)
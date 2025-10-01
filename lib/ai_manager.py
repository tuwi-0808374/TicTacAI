from lib.gemini_model import GeminiModel
from lib.ollama_model import OllamaModel
from lib.random_model import RandomModel
from lib.grok_model import GrokModel

class AIManager():
    def __init__(self):
        pass

    def create_model(self, model_name):
        if model_name == "gemini-2.5-flash-lite":
            return GeminiModel()
        elif model_name == "llama3.1:8b":
            return OllamaModel(10, 50)
        elif model_name == "grok-3-mini":
            return GrokModel(25, 50)
        else:
            return RandomModel()

    def get_next_move(self, grid, prompt, model_name):
        model = self.create_model(model_name)
        response = model.get_next_move(grid, prompt, model_name)
        return response
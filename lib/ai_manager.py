from lib.ai_models.gemini_model import GeminiModel
from lib.ai_models.ollama_model import OllamaModel
from lib.ai_models.random_model import RandomModel
from lib.ai_models.open_router_model import OpenRouter
from lib.ai_models.openai_model import OpenAIAPI

class AIManager():
    def __init__(self):
        pass

    def create_model(self, ai_model):
        if ai_model == "gemini":
            return GeminiModel()
        elif ai_model == "ollama":
            return OllamaModel(10, 50)
        elif ai_model == "openrouter":
            return OpenRouter(25, 50)
        elif ai_model == "openai":
            return OpenAIAPI(25, 50)
        else:
            return RandomModel()

    def get_next_move(self, grid, prompt, model_name, ai_model):
        model = self.create_model(ai_model)
        response = model.get_next_move(grid, prompt, model_name)
        return response
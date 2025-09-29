import copy
import json
from flask import *
from lib.ai_model import AIModel

class RandomModel(AIModel):
    def __init__(self, timeout, max_retries):
        super().__init__(timeout, max_retries)
        pass

    def get_next_move(self, grid, prompt, model_name):
        grid_copy = copy.deepcopy(grid)
        content = f"""{self.random_move(grid_copy)}"""
        parsed_response = json.loads(content)

        print(parsed_response)
        return parsed_response

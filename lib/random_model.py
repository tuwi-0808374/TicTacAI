import copy
import json
from flask import *
from lib.ai_model import AIModel

class RandomModel(AIModel):

    def get_next_move(self, grid, prompt, model_name):
        grid_copy = copy.deepcopy(grid)
        new_grid = self.random_move(grid_copy)
        self.grid_is_valid(new_grid, grid)
        content = f"""{new_grid}"""
        parsed_response = json.loads(content)

        return parsed_response, 0, model_name, 0

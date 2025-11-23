import copy
import json
import random

from flask import *
from lib.ai_models.ai_model import AIModel

class RandomModel(AIModel):

    def get_next_move(self, grid, prompt, model_name):
        grid_copy = copy.deepcopy(grid)
        new_grid = self.random_move(grid_copy)
        self.grid_is_valid(new_grid, grid)
        content = f"""{new_grid}"""
        parsed_response = json.loads(content)

        return parsed_response, model_name, []

    def random_move(self, grid):
        """Randomly select a move from the given grid."""
        potential_cells = []
        for i in range(5):
            for j in range(5):
                if grid[i][j] == 0:
                    potential_cells.append((i, j))
        if potential_cells:
            random_cell = random.choice(potential_cells)
            grid[random_cell[0]][random_cell[1]] = 1
            return grid
        else:
            return None

import random
from abc import ABC, abstractmethod


class AIModel(ABC):
    """Abstract product that represents an AI model api"""
    def __init__(self, timeout = 10, max_retries = 50):
        self.timeout = timeout
        self.max_retries = max_retries

    @abstractmethod
    def get_next_move(self, grid, prompt, model):
        """Return new grid and other results from the AI"""
        pass

    def make_prompt(self, grid_json, prompt):
        json_prompt = f"""
                {prompt}
                Current grid:
                {grid_json}
                """
        print(json_prompt)
        return json_prompt

    def is_valid_grid(self, grid):
        """Validate that grid is 5x5 and contains only 0, 1, or 2."""
        if not isinstance(grid, list) or len(grid) != 5:
            return False
        for row in grid:
            if not isinstance(row, list) or len(row) != 5:
                return False
            if not all(isinstance(x, int) and x in (0, 1, 2) for x in row):
                return False
        return True

    def has_one_new_move(self, old_grid, new_grid):
        """Check that new_grid has exactly one new '1' in a previously '0' cell."""
        differences = 0
        for i in range(5):
            for j in range(5):
                if old_grid[i][j] != new_grid[i][j]:
                    if old_grid[i][j] != 0 or new_grid[i][j] != 1:
                        return False
                    differences += 1
        return differences == 1

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

    def grid_is_valid(self, new_grid, old_grid):
        if not self.is_valid_grid(new_grid):
            raise ValueError("Invalid response grid: Must be a 5x5 grid with values 0, 1, or 2")
        if not self.has_one_new_move(old_grid, new_grid):
            raise ValueError("Invalid response: Must place exactly one new '1' in an empty '0' cell")
        return True
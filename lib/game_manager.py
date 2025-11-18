from lib.game_model import Game

class GameManager:
    def __init__(self):
        self.turn = 0
        self.history = []

    def next_turn(self):
        self.turn += 1

    def get_current_turn(self):
        return self.turn

    def restart_game(self):
        self.turn = 0
        self.history = []

    def add_history(self, history):
        self.history.append(history)

    def save_history(self):
        game = Game()
        last_turn = self.history[len(self.history) - 1]
        last_turn["turns"] = self.turn
        last_turn["total_time"] = 99
        last_turn["total_attempts"] = 99
        game.add_game(last_turn)

    def check_win(self, grid):
        size = 5
        check = 4
        # Horizontal 4 in a row check
        for row in range(size):
            for col in range(size):
                if grid[row][col] > 0 and col <= size - check:
                    match = True
                    for cell in range(1, check):
                        if grid[row][col] != grid[row][col + cell]:
                            match = False
                            break
                    if match:
                        return grid[row][col]

        # Vertical 4 in a row check
        for col in range(size):
            for start_row in range(size):
                if grid[start_row][col] > 0 and start_row <= size - check:
                    match = True
                    for cell in range(1, check):
                        if grid[start_row][col] != grid[start_row + cell][col]:
                            match = False
                            break
                    if match:
                        return grid[start_row][col]

        # Diagonal 4 in a row check (from right to left)
        for row in range(size):
            for col in range(size):
                if grid[row][col] > 0 and col <= size - check and row <= size - check:
                    match = True
                    for next_cell in range(1, check):
                        # Go to next cell but also one cell down
                        # print(f"{row + next_cell} - {col + next_cell} = {grid[row + next_cell][col + next_cell]}")
                        if grid[row][col] != grid[row + next_cell][col + next_cell]:
                            match = False
                            break
                    if match:
                        return grid[row][col]

        # Diagonal 4 in a row check other side (from left to right)
        for row in range(size):
            for col in range(size):
                if grid[row][col] > 0 and col >= check - 1 and row <= size - check:
                    print(f"\n# {row} - {col} start {grid[row][col]}")
                    match = True
                    for next_cell in range(1, check):
                        # Go to next cell but also one cell down
                        print(f"\n# {row + next_cell} - {col - next_cell} = {grid[row + next_cell][col - next_cell]}")
                        if grid[row][col] != grid[row + next_cell][col - next_cell]:
                            match = False
                            break
                    if match:
                        return grid[row][col]

        return 0

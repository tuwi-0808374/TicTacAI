
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

    def add_history(self, history):
        self.history.append(history)

    def check_win(self, grid):
        size = 5
        check = 4
        # Horizontal 4 in a row check
        for row in range(size):
            for col in range(size):
                if grid[row][col] > 0 and col <= size - check:
                    match = True
                    for cell in range(check):
                        if grid[row][col] != grid[row][col + cell]:
                            match = False
                    if match:
                        return grid[row][col]

        # Vertical 4 in a row check
        for col in range(size):
            for start_row in range(size):
                if grid[start_row][col] > 0 and start_row <= size - check:
                    match = True
                    for cell in range(check):
                        if grid[start_row][col] != grid[start_row + cell][col]:
                            match = False
                    if match:
                        return grid[start_row][col]

        return 0

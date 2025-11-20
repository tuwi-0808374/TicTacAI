from lib.game_model import Game

class GameManager:
    def __init__(self):
        self.turn = 0
        self.moves = []

    def next_turn(self):
        self.turn += 1

    def get_current_turn(self):
        return self.turn

    def restart_game(self):
        self.turn = 0
        self.moves = []

    def add_move(self, move):
        self.moves.append(move)

    def save_move(self):
        game = Game()

        # add game to db
        game_data = self.moves[len(self.moves) - 1]
        game_data["turns"] = self.turn
        total_time = 0
        total_attempts = 0
        for move in self.moves:
            if "attempt" in move:
                total_attempts += len(move["attempt"])
                for attempt_item in move["attempt"]:
                    total_time += attempt_item["elapsed_time"]
        game_data["total_time"] = total_time
        game_data["total_attempts"] = total_attempts
        game_id = game.add_game(game_data)

        # add move to db
        for move in self.moves:
            move_data = {}
            move_data["game_id"] = game_id
            move_data["turn"] = move["turn"]
            move_data["grid"] = str(move["grid"])
            print(move_data)
            game.add_move(move_data)



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

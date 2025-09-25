import copy
import json
import random
import re
import time

from google import genai
from google.genai import types
from flask import *

import ollama

class AIManager():
    def __init__(self):
        self.max_retries = 50
        self.timeout = 10
        self.api_type = 1
        pass

    def get_next_move(self, grid):
        grid_json = json.dumps(grid)

        json_prompt = f"""
        Play a 5x5 Tic-Tac-Toe variant as '1' (AI). Rules:
        - Grid uses ONLY numeric values: '0' (empty), '1' (AI), '2' (opponent).
        - Place ONE numeric '1' in any empty '0' cell.
        - Prioritize winning (four '1's in a row, column, or diagonal).
        - If no win, block opponent (four '2's in a row, column, or diagonal).
        - If neither, choose an empty '0' cell, preferring central positions (e.g., row 2, column 2).
        - Output ONLY a 5x5 grid in JSON format as an array of arrays (e.g., [[0,0,0,0,0],[0,1,0,0,0],[0,2,0,0,0],[0,0,0,0,0],[0,0,0,0,0]]), using ONLY numeric values (0, 1, 2), no strings, no extra text, no other numbers (e.g., no '3'), no object keys (e.g., no {{"grid": [...]}}).
        - Use compact JSON: no indentation, no newlines, no extra spaces.
        - You MUST place a new '1' in an empty '0' cell and MUST NOT repeat the input grid.

        Current grid:
        {grid_json}
        """
        print(json_prompt)

        # Retry loop
        for attempt in range(self.max_retries):
            print(f"Attempt {attempt}")
            try:
                start_time = time.time()

                if self.api_type == 0:
                    # Send prompt to model
                    json_response = ollama.chat(
                        model="llama3.1:8b",
                        messages=[{"role": "user", "content": json_prompt}],
                    )

                    content = json_response["message"]["content"]

                    # Clean response (remove Markdown)
                    content = content.replace('```json', '').replace('```', '').strip()

                    # Parse response
                    parsed_response = json.loads(content)

                elif self.api_type == 1:
                    time_out = self.timeout * 1000
                    client = genai.Client(http_options=types.HttpOptions(timeout=time_out)) # timeout is in milliseconds

                    json_response = client.models.generate_content(
                        model="gemini-2.5-flash-lite", contents=json_prompt
                    )

                    elapsed_time = time.time() - start_time
                    print(f"The response took: {elapsed_time} seconds.")
                    if elapsed_time > self.timeout:
                        raise TimeoutError(f"GenAI call timed out after {elapsed_time:.2f} seconds (limiet: {self.timeout}s)")

                    print(json_response.text)
                    content = json_response.text

                    # Clean response (remove Markdown)
                    content = content.replace('```json', '').replace('```', '').strip()

                    # Extract the first valid JSON array to handle multiple objects
                    json_objects = re.findall(r'\[\[.*?\]\]', content)
                    if json_objects:
                        content = json_objects[0]
                    else:
                        raise ValueError(f"No valid JSON array found in response: {content}")

                    # Attempts to parse the JSON response.
                    parsed_response = json.loads(content)
                else:
                    grid_copy = copy.deepcopy(grid)
                    content = f"""{self.random_move(grid_copy)}"""
                    parsed_response = json.loads(content)

                # Handle wrapped response (e.g., {"grid": [...]})
                if isinstance(parsed_response, dict) and "grid" in parsed_response:
                    new_grid = parsed_response["grid"]
                else:
                    new_grid = parsed_response

                print(new_grid)

                if not self.is_valid_grid(new_grid):
                    raise ValueError("Invalid response grid: Must be a 5x5 grid with values 0, 1, or 2")
                if not self.has_one_new_move(grid, new_grid):
                    raise ValueError("Invalid response: Must place exactly one new '1' in an empty '0' cell")

                return new_grid

            except TimeoutError as e:
                print(f"Timeout op attempt {attempt}: {str(e)}")
                if attempt < self.max_retries - 1:
                    time.sleep(1)
                    continue
                raise RuntimeError(f"Model timed out after {self.max_retries} attempts")

            except genai.errors.ServerError as e:
                print(f"GenAI ServerError op attempt {attempt}: {str(e)}")
                if attempt < self.max_retries - 1:
                    time.sleep(1)
                    continue
                raise RuntimeError(f"GenAI server failed after {self.max_retries} attempts: {str(e)}")

            except ollama.ResponseError as e:
                raise RuntimeError(f"Failed to get response from model: {str(e)}")
            except ValueError as e:
                if attempt < self.max_retries - 1:
                    time.sleep(1)
                    continue
                raise ValueError(f"Model failed to produce valid grid after {self.max_retries} attempts: {str(e)}")
            except Exception as e:
                raise RuntimeError(f"Unexpected error: {str(e)}")

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
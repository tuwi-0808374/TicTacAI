import copy
import google.genai.errors
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
        pass

    def get_next_move(self, grid, prompt, model, timeout, max_retries):
        grid_json = json.dumps(grid)

        json_prompt = f"""
        {prompt}
        Current grid:
        {grid_json}
        """
        print(json_prompt)

        # Retry loop
        for attempt in range(max_retries):
            print(f"Attempt {attempt}")
            try:
                start_time = time.time()

                if model == "llama3.1:8b":
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

                elif model == "gemini-2.5-flash-lite":
                    time_out = timeout * 1000
                    client = genai.Client(http_options=types.HttpOptions(timeout=time_out)) # timeout is in milliseconds

                    json_response = client.models.generate_content(
                        model="gemini-2.5-flash-lite", contents=json_prompt
                    )

                    elapsed_time = time.time() - start_time
                    print(f"The response took: {elapsed_time} seconds.")
                    if elapsed_time > timeout:
                        raise TimeoutError(f"GenAI call timed out after {elapsed_time:.2f} seconds (limiet: {timeout}s)")

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
                if attempt < max_retries - 1:
                    time.sleep(1)
                    continue
                raise RuntimeError(f"Model timed out after {max_retries} attempts")

            except google.genai.errors.APIError as e:
                print(f"GenAI API error op attempt {attempt}: {str(e)}")
                if attempt < max_retries - 1:
                    time.sleep(1)
                    continue
                raise RuntimeError(f"GenAI API failed after {max_retries} attempts: {str(e)}")

            except ollama.ResponseError as e:
                raise RuntimeError(f"Failed to get response from model: {str(e)}")
            except ValueError as e:
                if attempt < max_retries - 1:
                    time.sleep(1)
                    continue
                raise ValueError(f"Model failed to produce valid grid after {max_retries} attempts: {str(e)}")
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
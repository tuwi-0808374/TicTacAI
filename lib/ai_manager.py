import copy
import json
import random
import time
from flask import *
from lib.gemini_model import GeminiModel

import ollama

class AIManager():
    def __init__(self):
        pass

    def create_model(self, model_name):
        if model_name == "gemini-2.5-flash-lite":
            return GeminiModel()
        else:
            return None

    def get_next_move(self, grid, prompt, model_name, timeout, max_retries):
        model = self.create_model(model_name)
        response = model.get_next_move(grid, prompt, model_name, timeout, max_retries)

        return response

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
                    pass
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

            except ollama.ResponseError as e:
                raise RuntimeError(f"Failed to get response from model: {str(e)}")
            except ValueError as e:
                if attempt < max_retries - 1:
                    time.sleep(1)
                    continue
                raise ValueError(f"Model failed to produce valid grid after {max_retries} attempts: {str(e)}")
            except Exception as e:
                raise RuntimeError(f"Unexpected error: {str(e)}")
import json
from google import genai
from flask import *

import ollama

class AIManager():
    def __init__(self):
        self.max_retries = 10
        self.api_type = 3
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
                if self.api_type == 0:
                    # Send prompt to model
                    json_response = ollama.chat(
                        model="llama3.1:8b",
                        # llama3.1:8b-text-q4_0 bad
                        # llama3.1:8b OK but slow 30 seconds
                        # llama3.1:8b-instruct-q4_0 bad
                        # mistral:7b-instruct-v0.3-q4_K_M
                        # phi3:3.8b OK but slow lots of bad attempts
                        # granite3.3:2b 3/10
                        # granite3.3:8b bad
                        # phi4-mini:3.8b bad
                        # deepseek-r1:7b bad never ending
                        # deepseek-r1:8b-llama-distill-q4_K_M bad
                        # deepseek-r1:1.5b bad
                        messages=[{"role": "user", "content": json_prompt}],
                    )

                    content = json_response["message"]["content"]

                    # Clean response (remove Markdown)
                    content = content.replace('```json', '').replace('```', '').strip()

                    # Parse response
                    parsed_response = json.loads(content)

                elif self.api_type == 1:
                    client = genai.Client()

                    json_response = client.models.generate_content(
                        model="gemini-2.5-flash-lite", contents= json_prompt
                        # gemini-2.5-flash-lite very fast
                        # gemini-2.5-flash slower but smart
                    )

                    print(json_response.text)
                    content = json_response.text

                    # Clean response (remove Markdown)
                    # Markdown Cleaning: content.replace('```json', '').replace('```', '').strip()
                    # is a way to handle the common case where LLMs wrap their JSON output
                    # in Markdown code blocks.
                    # This improves the chances of successful JSON parsing.

                    content = content.replace('```json', '').replace('```', '').strip()

                    # Attempts to parse the JSON response.
                    parsed_response = json.loads(content)
                else:
                    content = """[
                              [0, 0, 0, 0, 0],
                              [0, 0, 1, 0, 0],
                              [0, 0, 0, 1, 0],
                              [0, 0, 1, 2, 1],
                              [0, 0, 2, 0, 2]
                                ]"""
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

            except ollama.ResponseError as e:
                raise RuntimeError(f"Failed to get response from model: {str(e)}")
            except json.JSONDecodeError:
                if attempt < self.max_retries - 1:
                    continue
                raise ValueError(f"Invalid JSON response from model after {self.max_retries} attempts: {content}")
            except ValueError as e:
                if attempt < self.max_retries - 1:
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
import json
import time
import ollama

from lib.ai_model import AIModel


class OllamaModel(AIModel):
    def __init__(self, timeout = 20, max_retries = 50):
        super().__init__(timeout, max_retries)
        pass

    def get_next_move(self, grid, prompt, model):
        grid_json = json.dumps(grid)
        json_prompt = self.make_prompt(grid_json, prompt)

        for attempt in range(self.max_retries):
            try:
                start_time = time.time()
                print(f"Attempt {attempt}")
                time_out = self.timeout * 1000

                # Send prompt to model
                json_response = ollama.chat(
                    model=model,
                    messages=[{"role": "user", "content": json_prompt}],
                )

                content = json_response["message"]["content"]

                # Clean response (remove Markdown)
                content = content.replace('```json', '').replace('```', '').strip()

                # Parse response
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

            except ollama.ResponseError as e:
                raise RuntimeError(f"Failed to get response from model: {str(e)}")

            except ValueError as e:
                if attempt < self.max_retries - 1:
                    time.sleep(1)
                    continue
                raise ValueError(f"Model failed to produce valid grid after {self.max_retries} attempts: {str(e)}")
            except Exception as e:
                raise RuntimeError(f"Unexpected error: {str(e)}")


import json
import time
import ollama
from ollama import Client

from lib.ai_models.ai_model import AIModel


class OllamaModel(AIModel):
    def __init__(self, timeout = 30, max_retries = 50):
        super().__init__(timeout, max_retries)
        pass

    def get_next_move(self, grid, prompt, model):
        grid_json = json.dumps(grid)
        json_prompt = self.make_prompt(grid_json, prompt)

        print(self.timeout)

        for attempt in range(self.max_retries):
            try:
                start_time = time.time()
                print(f"Attempt {attempt}")
                time_out = self.timeout * 1000

                client = Client(timeout = time_out)

                # Send prompt to model
                json_response = client.chat(
                    model=model,
                    messages=[{"role": "user", "content": json_prompt}],
                )

                elapsed_time = time.time() - start_time
                print(f"The response took: {elapsed_time} seconds.")
                if elapsed_time > self.timeout:
                    raise TimeoutError(f"Ollama call timed out after {elapsed_time:.2f} seconds (limiet: {self.timeout}s)")

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

                self.grid_is_valid(new_grid, grid)

                return new_grid, elapsed_time, model, attempt

            except TimeoutError as e:
                print(f"Timeout op attempt {attempt}: {str(e)}")
                if attempt < self.max_retries - 1:
                    time.sleep(1)
                    continue
                raise RuntimeError(f"Model timed out after {self.max_retries} attempts")

            except ollama.ResponseError as e:
                raise RuntimeError(f"Failed to get response from model: {str(e)}")

            except ollama.RequestError as e:
                raise RuntimeError(f"Failed to get response from model: {str(e)}")

            except ValueError as e:
                if attempt < self.max_retries - 1:
                    time.sleep(1)
                    continue
                raise ValueError(f"Model failed to produce valid grid after {self.max_retries} attempts: {str(e)}")
            except Exception as e:
                raise RuntimeError(f"Unexpected error: {str(e)}")


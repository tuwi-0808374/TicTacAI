import json
import re
import time
import google.genai.errors

from google import genai
from google.genai import types
from flask import *
from lib.ai_models.ai_model import AIModel

class GeminiModel(AIModel):
    def __init__(self, timeout = 10, max_retries = 50):
        super().__init__(timeout, max_retries)
        self.attempts = []
        pass

    def get_next_move(self, grid, prompt, model_name):
        grid_json = json.dumps(grid)
        json_prompt = self.make_prompt(grid_json, prompt)

        for attempt in range(self.max_retries):
            try:
                start_time = time.time()
                print(f"Attempt {attempt}")
                time_out = self.timeout * 1000

                client = genai.Client(http_options=types.HttpOptions(timeout=time_out))  # timeout is in milliseconds

                json_response = client.models.generate_content(
                    model=model_name, contents=json_prompt
                )

                elapsed_time = time.time() - start_time
                print(f"The response took: {elapsed_time} seconds.")
                if elapsed_time > self.timeout:
                    raise TimeoutError(f"Gemini call timed out after {elapsed_time:.2f} seconds (limiet: {self.timeout}s)")

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

                # Handle wrapped response (e.g., {"grid": [...]})
                if isinstance(parsed_response, dict) and "grid" in parsed_response:
                    new_grid = parsed_response["grid"]
                else:
                    new_grid = parsed_response

                print(new_grid)


                new_attempt = {"id": attempt, "elapsed_time": elapsed_time}
                self.attempts.append(new_attempt)

                self.grid_is_valid(new_grid, grid)

                return new_grid, model_name, self.attempts

            except TimeoutError as e:
                print(f"Timeout op attempt {attempt}: {str(e)}")
                if attempt < self.max_retries - 1:
                    time.sleep(1)
                    continue
                raise RuntimeError(f"Model timed out after {self.max_retries} attempts")

            except google.genai.errors.APIError as e:
                print(f"GenAI API error op attempt {attempt}: {str(e)}")
                if attempt < self.max_retries - 1:
                    time.sleep(1)
                    continue
                raise RuntimeError(f"GenAI API failed after {self.max_retries} attempts: {str(e)}")

            except ValueError as e:
                if attempt < self.max_retries - 1:
                    time.sleep(1)
                    continue
                raise ValueError(f"Model failed to produce valid grid after {self.max_retries} attempts: {str(e)}")
            except Exception as e:
                raise RuntimeError(f"Unexpected error: {str(e)}")


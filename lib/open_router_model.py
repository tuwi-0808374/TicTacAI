import json
import os
import re
import time
import openai

from flask import *
from openai import OpenAI

from lib.ai_model import AIModel

class OpenRouter(AIModel):
    def __init__(self, timeout = 10, max_retries = 50):
        super().__init__(timeout, max_retries)
        pass

    def get_next_move(self, grid, prompt, model_name):
        grid_json = json.dumps(grid)
        json_prompt = self.make_prompt(grid_json, prompt)

        for attempt in range(self.max_retries):
            try:
                start_time = time.time()
                print(f"Attempt {attempt}")
                time_out = self.timeout * 1000

                api_key = os.environ.get('OPENROUTER_API_KEY')

                # Configure the client with your OpenRouter API key
                client = OpenAI(
                    base_url="https://openrouter.ai/api/v1",
                    api_key=api_key
                )

                # For Grok 3 Mini with high reasoning
                response = client.chat.completions.create(
                    model=f"{ model_name }",
                    messages=[{"role": "user", "content": json_prompt}],
                )

                print(response.choices[0].message.content)
                json_response = response.choices[0].message.content

                elapsed_time = time.time() - start_time
                print(f"The response took: {elapsed_time} seconds.")
                if elapsed_time > self.timeout:
                    raise TimeoutError(f"{model_name} call timed out after {elapsed_time:.2f} seconds (limiet: {self.timeout}s)")

                content = json_response

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

                self.grid_is_valid(new_grid, grid)

                return new_grid, elapsed_time, model_name, attempt

            except TimeoutError as e:
                print(f"Timeout op attempt {attempt}: {str(e)}")
                if attempt < self.max_retries - 1:
                    time.sleep(1)
                    continue
                raise RuntimeError(f"Model: { model_name } timed out after {self.max_retries} attempts")

            except ValueError as e:
                if attempt < self.max_retries - 1:
                    time.sleep(1)
                    continue
                raise ValueError(f"Model { model_name } failed to produce valid grid after {self.max_retries} attempts: {str(e)}")
            except Exception as e:
                raise RuntimeError(f"Unexpected error: {str(e)}")


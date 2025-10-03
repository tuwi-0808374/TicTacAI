

model_data = {
    "gemini-2.5-flash-lite" : {
        "ai_model": "gemini",
        "icon" : "gemini.png"
    },
    "llama3.1:8b": {
        "ai_model": "ollama",
        "icon": "ollama.png"
    },
    "random": {
        "ai_model": "random",
        "icon": "random.png"
    },
    "grok-3-mini": {
        "ai_model": "grok",
        "icon": "grok.png"
    }

}

prompt_data = {
    "default" : f"""
            Play a 5x5 Tic-Tac-Toe variant as '1' (AI). Rules:
                    - Grid uses ONLY numeric values: '0' (empty), '1' (AI), '2' (opponent).
                    - Place ONE numeric '1' in any empty '0' cell.
                    - Prioritize winning (four '1's in a row, column, or diagonal).
                    - If no win, block opponent (four '2's in a row, column, or diagonal).
                    - If neither, choose an empty '0' cell, preferring central positions (e.g., row 2, column 2).
                    - Output ONLY a 5x5 grid in JSON format as an array of arrays (e.g., [[0,0,0,0,0],[0,0,0,0,0],[0,0,0,0,0],[0,0,0,0,0],[0,0,0,0,0]]), using ONLY numeric values (0, 1, 2), no strings, no extra text, no other numbers (e.g., no '3'), no object keys (e.g., no {{"grid": [...]}}).
                    - Use compact JSON: no indentation, no newlines, no extra spaces.
                    - You MUST place a new '1' in an empty '0' cell and MUST NOT repeat the input grid.
                    - You need to change the current "Current grid".
            """
}
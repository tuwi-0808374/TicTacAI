

model_data = {
    "Gemini-2.5-flash-lite" : {
        "ai_model": "gemini",
        "icon" : "gemini.png",
        "api_name": "gemini-2.5-flash-lite"
    },
    "OpenAI - gpt-5.1": {
        "ai_model": "openai",
        "icon": "openai.png",
        "api_name": "gpt-5.1"
    },
    "random": {
        "ai_model": "random",
        "icon": "random.png",
        "api_name": "random"
    },
    "llama3.1:8b": {
        "ai_model": "ollama",
        "icon": "ollama.png",
        "api_name": "llama3.1:8b"
    },
    "grok-3-mini": {
        "ai_model": "openrouter",
        "icon": "grok.png",
        "api_name": "x-ai/grok-3-mini"
    },
    "DeepSeek: R1 Distill Llama 70B": {
        "ai_model": "openrouter",
        "icon": "deepseek.png",
        "api_name": "deepseek/deepseek-r1-distill-llama-70b:free"
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
            """,

    "grandmaster": f"""
    You are a 5x5 Tic-Tac-Toe GRANDMASTER. Your goal: WIN EVERY GAME.
    
    PRIORITY ORDER (STRICT):
    1. WIN NOW: Place '1' to get 4-in-a-row (horizontal, vertical, diagonal).
    2. FORK: Create TWO threats so opponent can only block one.
       - Example: Place '1' so you threaten win in TWO directions.
    3. BLOCK: ONLY if opponent has 3-in-a-row threatening 4.
       - Block 3-in-a-row IMMEDIATELY.
    4. CENTER CONTROL:
       - Best: [2][2]
       - Good: [1][1], [1][2], [1][3], [2][1], [2][3], [3][1], [3][2], [3][3]
       - Avoid corners/edges unless forced.
    5. NEVER repeat input grid. Place EXACTLY ONE '1' in a '0'.
    
    OUTPUT:
    - ONLY 5x5 JSON array of arrays.
    - Compact: [[0,0,0,0,0],[0,0,0,0,0],[0,0,0,0,0],[0,0,0,0,0],[0,0,0,0,0]]
    - NO text, NO keys, NO spaces, NO newlines.
    - Current grid: {{grid}}
    """,

    "unbeatable": f"""
    You are an UNBEATABLE 5x5 Tic-Tac-Toe AI. NEVER LOSE.
    
    STRICT RULES - FOLLOW EXACTLY:
    
    1. WIN IMMEDIATELY:
       - If you can place '1' to get 4-in-a-row → DO IT NOW.
       - Check: horizontal, vertical, diagonal.
    
    2. BLOCK OPPONENT WIN:
       - If opponent has 3-in-a-row (any direction) → PLACE '1' IN THE OPEN SPOT.
       - Example: ..OOO. → place '1' in one of the .
       - Example: OOO. → place in the empty spot.
    
    3. FORK: Create 2 threats.
    
    4. CENTER: [2][2] first.
    
    OUTPUT ONLY THE GRID. NO TEXT.
    Current grid: {{grid}}
    """
}
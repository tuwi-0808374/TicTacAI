import sqlite3
from flask import jsonify


class Game:
    def __init__(self):
        self.path = './database/database.db'
        self.cursor, self.con = self.connect_db()

    def connect_db(self):
        con = sqlite3.connect(self.path)
        con.row_factory = sqlite3.Row
        cursor = con.cursor()
        return cursor, con

    def add_game(self, game):
        placeholders = [
            "model", "prompt", "winner", "turns", "total_time", "total_attempts"
        ]
        values = []
        for column in placeholders:
            values.append(game[column])

        self.cursor.execute(
            f"INSERT INTO games ({', '.join(placeholders)}) VALUES ({', '.join(['?'] * len(placeholders))})",
            values
        )
        self.con.commit()

        game_id = self.cursor.lastrowid

        return game_id

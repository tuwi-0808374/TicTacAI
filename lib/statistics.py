import sqlite3

class Statistics:
    def __init__(self):
        self.path = './database/database.db'
        self.cursor, self.con = self.connect_db()

    def connect_db(self):
        con = sqlite3.connect(self.path)
        con.row_factory = sqlite3.Row
        cursor = con.cursor()
        return cursor, con

    def get_most_used_models(self):
        result = self.cursor.execute(
            "SELECT COUNT(model) AS count, model FROM games GROUP BY model ORDER BY count DESC"
        ).fetchall()

        # return [dict(row) for row in result]
        return dict(result)


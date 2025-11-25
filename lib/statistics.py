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

    def get_winning_model(self):
        result = self.cursor.execute(
            "SELECT COUNT(model) AS model_count, model FROM games WHERE winner == 1 GROUP BY model ORDER BY model_count DESC"
        ).fetchall()
        return dict(result)

    def get_user_vs_ai(self):
        result = self.cursor.execute(
            """SELECT 
                    COUNT(*) AS win_count,
                    CASE winner
                        WHEN 1 THEN 'AI'
                        WHEN 2 THEN 'User'
                        ELSE 'Draw'
                    END AS winner_name
                FROM games
                GROUP BY winner
                ORDER BY winner DESC;"""
        ).fetchall()
        return dict(result)
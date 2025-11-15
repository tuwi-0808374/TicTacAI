import sqlite3
from pathlib import Path

class DatabaseGenerator:
    def __init__(self, database_file, overwrite=False, initial_data=False):
        self.database_file = Path(database_file)
        self.create_initial_data = initial_data
        self.database_overwrite = overwrite
        self.test_file_location()
        self.conn = sqlite3.connect(self.database_file)

    def generate_database(self):
        self.create_table_games()
        self.create_table_moves()
        self.create_table_attempts()

        if self.create_initial_data:
            pass

    def create_table_games(self):
        create_statement = """
        CREATE TABLE IF NOT EXISTS games (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            model TEXT NOT NULL,
            winner INTEGER NOT NULL,
            turns INTEGER NOT NULL,
            total_time REAL,
            total_attempts INTEGER,
            created_at DATETIME DEFAULT CURRENT_TIMESTAMP
        );
        """
        self.__execute_transaction_statement(create_statement)
        print("games table created")

    def create_table_moves(self):
        create_statement = """
        CREATE TABLE IF NOT EXISTS moves (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            game_id INTEGER NOT NULL,
            turn INTEGER NOT NULL,
            grid TEXT NOT NULL,
            response_time REAL NOT NULL,
            attempt_count INTEGER NOT NULL,
            FOREIGN KEY (game_id) REFERENCES games (id)
        );
        """
        self.__execute_transaction_statement(create_statement)
        print("moves table created")

    def create_table_attempts(self):
        create_statement = """
        CREATE TABLE IF NOT EXISTS attempts (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            move_id INTEGER NOT NULL,
            attempt_number INTEGER NOT NULL,
            elapsed_time REAL,
            FOREIGN KEY (move_id) REFERENCES moves (id)
        );
        """
        self.__execute_transaction_statement(create_statement)
        print("attemps table created")

    def __execute_transaction_statement(self, create_statement, parameters=()):
        c = self.conn.cursor()
        c.execute(create_statement, parameters)
        self.conn.commit()

    def __execute_many_transaction_statement(
            self, create_statement, list_of_parameters=()
    ):
        c = self.conn.cursor()
        c.executemany(create_statement, list_of_parameters)
        self.conn.commit()

    def test_file_location(self):
        if not self.database_file.parent.exists():
            raise ValueError(
                f"Database file location {self.database_file.parent} does not exist"
            )
        if self.database_file.exists():
            if not self.database_overwrite:
                raise ValueError(
                    f"Database file {self.database_file} already exists, set overwrite=True to overwrite"
                )
            else:
                self.database_file.unlink()
                print("Database already exists, deleted")
        if not self.database_file.exists():
            try:
                self.database_file.touch()
                print("New database setup")
            except Exception as e:
                raise ValueError(
                    f"Could not create database file {self.database_file} due to error {e}"
                )


if __name__ == "__main__":
    my_path = Path(__file__)
    project_root = my_path.parent.parent
    database_path = project_root / "database" / "database.db"
    database_generator = DatabaseGenerator(
        database_path, overwrite=True, initial_data=True
    )
    database_generator.generate_database()
import sqlite3
import os

db_path = os.path.join(os.path.dirname(__file__), 'data', 'inventory.db')

class Database:
    def __init__(self):
        self.conn = sqlite3.connect(db_path)
        self.cursor = self.conn.cursor()

    def execute_query(self, query, params=()):
        """Executes a query and commits changes."""
        self.cursor.execute(query, params)
        self.conn.commit()

    def fetch_all(self, query, params=()):
        """Fetches all results for a query."""
        self.cursor.execute(query, params)
        return self.cursor.fetchall()

    def fetch_one(self, query, params=()):
        """Fetches a single result for a query."""
        self.cursor.execute(query, params)
        return self.cursor.fetchone()

    def close(self):
        """Closes the database connection."""
        self.conn.close()

# Initialize the database
if __name__ == "__main__":
    db = Database()
    # Ensure the schema includes the removed_items table
    with open(os.path.join(os.path.dirname(__file__), 'schema.sql'), 'r') as schema_file:
        db.cursor.executescript(schema_file.read())
    db.conn.commit()
    db.close()
    print("Database initialized successfully.")


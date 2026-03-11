import sqlite3

# writing db connection handler...
class DBAgent:
    """
    SQLite DB Agent for querying and managing structured data.
    Can be used for schema exploration and result formatting.
    """

    def __init__(self, db_path: str = "local_database.db"):
        # initializing SQLite connection...
        self.db_path = db_path
        self.connection = None

    def _connect(self):
        # establishing basic connection...
        if not self.connection:
            self.connection = sqlite3.connect(self.db_path)
            # setting row factory to return dict-like objects...
            self.connection.row_factory = sqlite3.Row
        return self.connection

    def query_db(self, query: str) -> list:
        """
        Executes a query and returns result in JSON-like structure (list of dicts).
        Uses standard sqlite3 Row objects.
        """
        # writing query execution logic...
        conn = self._connect()
        try:
            cursor = conn.cursor()
            cursor.execute(query)
            rows = cursor.fetchall()
            # converting Row objects to standard dictionaries...
            result = [dict(row) for row in rows]
            return result
        except Exception as e:
            # adding basic query error handling...
            return {"error": f"Query failed: {str(e)}", "query": query}

    def fetch_schema(self) -> list:
        """
        Retrieves table schemas for the orchestrator to understand the DB structure.
        """
        # adding schema fetcher for the orchestrator...
        query = "SELECT name, sql FROM sqlite_master WHERE type='table';"
        return self.query_db(query)

    def close(self):
        # closing connections...
        if self.connection:
            self.connection.close()

# adding a quick internal test example...
if __name__ == "__main__":
    agent = DBAgent()
    print("Agent Initialized. Schema Search query example:")
    print("SELECT * FROM sqlite_master;")

import sqlite3

class Database:
    def __init__(self, db_path="nodes.db"):
        self.conn = sqlite3.connect(db_path, check_same_thread=False)
        self._initialize_db()

    def _initialize_db(self):
        with self.conn:
            self.conn.execute("""
            CREATE TABLE IF NOT EXISTS nodes (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                node_info TEXT NOT NULL
            )
            """)

    def add_node(self, node_info):
        with self.conn:
            self.conn.execute("INSERT INTO nodes (node_info) VALUES (?)", (node_info,))

    def get_nodes(self):
        with self.conn:
            return [row[0] for row in self.conn.execute("SELECT node_info FROM nodes")]

    def remove_node(self, index):
        with self.conn:
            nodes = self.get_nodes()
            if 0 <= index < len(nodes):
                self.conn.execute("DELETE FROM nodes WHERE id = (SELECT id FROM nodes LIMIT 1 OFFSET ?)", (index,))
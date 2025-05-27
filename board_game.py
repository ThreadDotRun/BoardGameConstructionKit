import sqlite3
import json

class BoardGame:
    def __init__(self, size, db_name=":memory:"):
        """Initialize a 2D game board with given size (n x n) and SQLite database.
        
        Args:
            size (int): Length of each dimension (square board).
            db_name (str): SQLite database file (default ':memory:' for in-memory).
        """
        self.size = size
        self.conn = sqlite3.connect(db_name)
        self.cursor = self.conn.cursor()
        self._create_table()
        self.board = self._load_board()

    def _create_table(self):
        """Create the board state table if it doesn't exist."""
        self.cursor.execute("""
            CREATE TABLE IF NOT EXISTS board (
                x INTEGER,
                y INTEGER,
                attributes TEXT,
                PRIMARY KEY (x, y)
            )
        """)
        self.conn.commit()

    def _load_board(self):
        """Load board state from SQLite into dictionary."""
        board = {}
        self.cursor.execute("SELECT x, y, attributes FROM board")
        for x, y, attr_json in self.cursor.fetchall():
            board[(x, y)] = json.loads(attr_json)
        return board

    def validate_coord(self, x, y):
        """Check if coordinates are within board bounds."""
        return 0 <= x < self.size and 0 <= y < self.size

    def set_position(self, x, y, attributes):
        """Set attributes for a board position and save to SQLite."""
        if not self.validate_coord(x, y):
            return False
        attr_json = json.dumps(attributes)
        self.cursor.execute("""
            INSERT OR REPLACE INTO board (x, y, attributes)
            VALUES (?, ?, ?)
        """, (x, y, attr_json))
        self.conn.commit()
        self.board[(x, y)] = attributes
        return True

    def get_position(self, x, y):
        """Get attributes for a board position."""
        if not self.validate_coord(x, y):
            return None
        return self.board.get((x, y), None)

    def update_attribute(self, x, y, key, value):
        """Update a specific attribute at a board position and save to SQLite."""
        if not self.validate_coord(x, y) or (x, y) not in self.board:
            return False
        attributes = self.board[(x, y)]
        for attr in attributes:
            if attr[0] == key:
                attr[1] = value
                break
        else:
            attributes.append([key, value])
        attr_json = json.dumps(attributes)
        self.cursor.execute("""
            UPDATE board SET attributes = ? WHERE x = ? AND y = ?
        """, (attr_json, x, y))
        self.conn.commit()
        return True

    def remove_position(self, x, y):
        """Remove all attributes from a board position and delete from SQLite."""
        if not self.validate_coord(x, y) or (x, y) not in self.board:
            return False
        self.cursor.execute("DELETE FROM board WHERE x = ? AND y = ?", (x, y))
        self.conn.commit()
        del self.board[(x, y)]
        return True

    def get_board_state(self):
        """Return the entire board state."""
        return self.board.copy()

    def close(self):
        """Close the SQLite connection."""
        self.conn.close()
import unittest
import sqlite3
import json
import os

# Define BoardGame class with SQLite persistence
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

# Test suite
class TestBoardGame(unittest.TestCase):
    def setUp(self):
        """Set up a fresh BoardGame instance before each test."""
        self.game = BoardGame(5, ":memory:")  # Use in-memory SQLite for tests
        print("\n=== Setting up test ===")

    def tearDown(self):
        """Clean up database connections and test database file."""
        try:
            self.game.close()
        except AttributeError:
            pass  # Handle case where game is not initialized
        if os.path.exists("test_board.db"):
            try:
                os.remove("test_board.db")
            except OSError:
                pass  # Ignore file removal errors

    def test_init(self):
        """Test BoardGame initialization."""
        print("Testing __init__")
        self.assertEqual(self.game.size, 5, "Board size should be 5")
        self.assertEqual(self.game.board, {}, "Board should initialize as empty dict")
        print("  __init__: Size and empty board - PASSED")

    def test_validate_coord(self):
        """Test coordinate validation."""
        print("Testing validate_coord")
        self.assertTrue(self.game.validate_coord(0, 0), "Coordinate (0,0) should be valid")
        self.assertTrue(self.game.validate_coord(4, 4), "Coordinate (4,4) should be valid")
        self.assertFalse(self.game.validate_coord(5, 0), "Coordinate (5,0) should be invalid")
        self.assertFalse(self.game.validate_coord(-1, 0), "Coordinate (-1,0) should be invalid")
        self.assertFalse(self.game.validate_coord(0, 5), "Coordinate (0,5) should be invalid")
        print("  validate_coord: Valid and invalid coordinates - PASSED")

    def test_set_position(self):
        """Test setting attributes at a position."""
        print("Testing set_position")
        attrs = [['unit', 'tank'], ['health', 5]]
        self.assertTrue(self.game.set_position(2, 3, attrs), "Setting valid position should return True")
        self.assertEqual(self.game.board[(2, 3)], attrs, "Position (2,3) should have correct attributes")
        print("  set_position: Valid position - PASSED")

        self.assertFalse(self.game.set_position(5, 0, attrs), "Setting invalid position should return False")
        self.assertNotIn((5, 0), self.game.board, "Invalid position should not be in board")
        print("  set_position: Invalid position - PASSED")

        new_attrs = [['unit', 'soldier'], ['health', 10]]
        self.assertTrue(self.game.set_position(2, 3, new_attrs), "Overwriting position should return True")
        self.assertEqual(self.game.board[(2, 3)], new_attrs, "Position (2,3) should have new attributes")
        print("  set_position: Overwrite position - PASSED")

    def test_get_position(self):
        """Test retrieving attributes from a position."""
        print("Testing get_position")
        attrs = [['unit', 'tank'], ['health', 5]]
        self.game.set_position(1, 1, attrs)

        self.assertEqual(self.game.get_position(1, 1), attrs, "Should return correct attributes")
        print("  get_position: Valid position with data - PASSED")

        self.assertIsNone(self.game.get_position(0, 0), "Empty position should return None")
        print("  get_position: Valid position, no data - PASSED")

        self.assertIsNone(self.game.get_position(5, 0), "Invalid position should return None")
        print("  get_position: Invalid position - PASSED")

    def test_update_attribute(self):
        """Test updating attributes at a position."""
        print("Testing update_attribute")
        attrs = [['unit', 'tank'], ['health', 5]]
        self.game.set_position(2, 2, attrs)

        self.assertTrue(self.game.update_attribute(2, 2, 'health', 3), "Updating existing attribute should return True")
        self.assertEqual(self.game.get_position(2, 2), [['unit', 'tank'], ['health', 3]], "Health should be updated to 3")
        print("  update_attribute: Update existing attribute - PASSED")

        self.assertTrue(self.game.update_attribute(2, 2, 'player', 'blue'), "Adding new attribute should return True")
        self.assertEqual(self.game.get_position(2, 2), [['unit', 'tank'], ['health', 3], ['player', 'blue']], 
                         "New attribute should be added")
        print("  update_attribute: Add new attribute - PASSED")

        self.assertFalse(self.game.update_attribute(5, 0, 'unit', 'soldier'), "Invalid position should return False")
        print("  update_attribute: Invalid position - PASSED")

        self.assertFalse(self.game.update_attribute(0, 0, 'unit', 'soldier'), "Empty position should return False")
        print("  update_attribute: Empty position - PASSED")

    def test_remove_position(self):
        """Test removing attributes from a position."""
        print("Testing remove_position")
        attrs = [['unit', 'tank'], ['health', 5]]
        self.game.set_position(3, 3, attrs)

        self.assertTrue(self.game.remove_position(3, 3), "Removing valid position should return True")
        self.assertNotIn((3, 3), self.game.board, "Position should be removed")
        print("  remove_position: Valid position - PASSED")

        self.assertFalse(self.game.remove_position(5, 0), "Invalid position should return False")
        print("  remove_position: Invalid position - PASSED")

        self.assertFalse(self.game.remove_position(0, 0), "Empty position should return False")
        print("  remove_position: Empty position - PASSED")

    def test_get_board_state(self):
        """Test retrieving the entire board state."""
        print("Testing get_board_state")
        attrs1 = [['unit', 'tank'], ['health', 5]]
        attrs2 = [['unit', 'soldier'], ['health', 10]]
        self.game.set_position(1, 1, attrs1)
        self.game.set_position(2, 2, attrs2)

        board_state = self.game.get_board_state()
        expected = {(1, 1): attrs1, (2, 2): attrs2}
        self.assertEqual(board_state, expected, "Board state should match expected")
        print("  get_board_state: Correct state - PASSED")

        board_state[(1, 1)] = [['unit', 'plane']]
        self.assertEqual(self.game.get_board_state(), expected, "Original board state should be unchanged")
        print("  get_board_state: Copy protection - PASSED")

    def test_persistence(self):
        """Test SQLite persistence across instances."""
        print("Testing persistence")
        attrs = [['unit', 'tank'], ['health', 5]]
        self.game.set_position(1, 1, attrs)
        self.game.close()

        # Create a new instance with the same database
        new_game = BoardGame(5, ":memory:")  # Use same DB (in-memory for testing)
        self.assertEqual(new_game.get_position(1, 1), None, "Data should not persist in-memory after close")
        new_game.close()
        
        # Test with file-based database
        file_db = "test_board.db"
        game_with_file = BoardGame(5, file_db)
        game_with_file.set_position(1, 1, attrs)
        game_with_file.close()

        new_game_with_file = BoardGame(5, file_db)
        self.assertEqual(new_game_with_file.get_position(1, 1), attrs, "Data should persist in file-based DB")
        new_game_with_file.close()
        print("  persistence: File-based persistence - PASSED")

if __name__ == '__main__':
    unittest.main(verbosity=0)
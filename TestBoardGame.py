import unittest
from board_game import BoardGame  # Assuming BoardGame is in board_game.py

class TestBoardGame(unittest.TestCase):
    def setUp(self):
        """Set up a fresh BoardGame instance before each test."""
        self.game = BoardGame(5)
        print("\n=== Setting up test ===")

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
        # Valid position
        attrs = [['unit', 'tank'], ['health', 5]]
        self.assertTrue(self.game.set_position(2, 3, attrs), "Setting valid position should return True")
        self.assertEqual(self.game.board[(2, 3)], attrs, "Position (2,3) should have correct attributes")
        print("  set_position: Valid position - PASSED")

        # Invalid position
        self.assertFalse(self.game.set_position(5, 0, attrs), "Setting invalid position should return False")
        self.assertNotIn((5, 0), self.game.board, "Invalid position should not be in board")
        print("  set_position: Invalid position - PASSED")

        # Overwrite existing position
        new_attrs = [['unit', 'soldier'], ['health', 10]]
        self.assertTrue(self.game.set_position(2, 3, new_attrs), "Overwriting position should return True")
        self.assertEqual(self.game.board[(2, 3)], new_attrs, "Position (2,3) should have new attributes")
        print("  set_position: Overwrite position - PASSED")

    def test_get_position(self):
        """Test retrieving attributes from a position."""
        print("Testing get_position")
        attrs = [['unit', 'tank'], ['health', 5]]
        self.game.set_position(1, 1, attrs)

        # Valid position with data
        self.assertEqual(self.game.get_position(1, 1), attrs, "Should return correct attributes")
        print("  get_position: Valid position with data - PASSED")

        # Valid position, no data
        self.assertIsNone(self.game.get_position(0, 0), "Empty position should return None")
        print("  get_position: Valid position, no data - PASSED")

        # Invalid position
        self.assertIsNone(self.game.get_position(5, 0), "Invalid position should return None")
        print("  get_position: Invalid position - PASSED")

    def test_update_attribute(self):
        """Test updating attributes at a position."""
        print("Testing update_attribute")
        attrs = [['unit', 'tank'], ['health', 5]]
        self.game.set_position(2, 2, attrs)

        # Update existing attribute
        self.assertTrue(self.game.update_attribute(2, 2, 'health', 3), "Updating existing attribute should return True")
        self.assertEqual(self.game.get_position(2, 2), [['unit', 'tank'], ['health', 3]], "Health should be updated to 3")
        print("  update_attribute: Update existing attribute - PASSED")

        # Add new attribute
        self.assertTrue(self.game.update_attribute(2, 2, 'player', 'blue'), "Adding new attribute should return True")
        self.assertEqual(self.game.get_position(2, 2), [['unit', 'tank'], ['health', 3], ['player', 'blue']], 
                         "New attribute should be added")
        print("  update_attribute: Add new attribute - PASSED")

        # Invalid position
        self.assertFalse(self.game.update_attribute(5, 0, 'unit', 'soldier'), "Invalid position should return False")
        print("  update_attribute: Invalid position - PASSED")

        # Empty position
        self.assertFalse(self.game.update_attribute(0, 0, 'unit', 'soldier'), "Empty position should return False")
        print("  update_attribute: Empty position - PASSED")

    def test_remove_position(self):
        """Test removing attributes from a position."""
        print("Testing remove_position")
        attrs = [['unit', 'tank'], ['health', 5]]
        self.game.set_position(3, 3, attrs)

        # Valid position
        self.assertTrue(self.game.remove_position(3, 3), "Removing valid position should return True")
        self.assertNotIn((3, 3), self.game.board, "Position should be removed")
        print("  remove_position: Valid position - PASSED")

        # Invalid position
        self.assertFalse(self.game.remove_position(5, 0), "Invalid position should return False")
        print("  remove_position: Invalid position - PASSED")

        # Empty position
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

        # Modify returned state, ensure original is unchanged
        board_state[(1, 1)] = [['unit', 'plane']]
        self.assertEqual(self.game.get_board_state(), expected, "Original board state should be unchanged")
        print("  get_board_state: Copy protection - PASSED")

if __name__ == '__main__':
    unittest.main(verbosity=0)  # Run tests with minimal default output, custom print statements handle real-time feedback
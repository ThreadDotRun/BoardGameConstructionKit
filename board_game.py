class BoardGame:
    def __init__(self, size):
        """Initialize a 2D game board with given size (n x n).
        
        Args:
            size (int): Length of each dimension (square board).
        """
        self.size = size
        self.board = {}  # Dictionary to store game state: (x, y) -> list of [key, value] pairs

    def validate_coord(self, x, y):
        """Check if coordinates are within board bounds.
        
        Args:
            x (int): X-coordinate.
            y (int): Y-coordinate.
            
        Returns:
            bool: True if valid, False otherwise.
        """
        return 0 <= x < self.size and 0 <= y < self.size

    def set_position(self, x, y, attributes):
        """Set attributes for a board position.
        
        Args:
            x (int): X-coordinate.
            y (int): Y-coordinate.
            attributes (list): List of [key, value] pairs (e.g., [['unit', 'tank'], ['health', 5]]).
            
        Returns:
            bool: True if successful, False if invalid coordinates.
        """
        if not self.validate_coord(x, y):
            return False
        self.board[(x, y)] = attributes
        return True

    def get_position(self, x, y):
        """Get attributes for a board position.
        
        Args:
            x (int): X-coordinate.
            y (int): Y-coordinate.
            
        Returns:
            list: List of [key, value] pairs if position exists, None if invalid or empty.
        """
        if not self.validate_coord(x, y):
            return None
        return self.board.get((x, y), None)

    def update_attribute(self, x, y, key, value):
        """Update a specific attribute at a board position.
        
        Args:
            x (int): X-coordinate.
            y (int): Y-coordinate.
            key (str): Attribute key to update.
            value: New value for the attribute.
            
        Returns:
            bool: True if successful, False if invalid coordinates or position empty.
        """
        if not self.validate_coord(x, y) or (x, y) not in self.board:
            return False
        attributes = self.board[(x, y)]
        for attr in attributes:
            if attr[0] == key:
                attr[1] = value
                return True
        attributes.append([key, value])  # Add new attribute if key doesn't exist
        return True

    def remove_position(self, x, y):
        """Remove all attributes from a board position.
        
        Args:
            x (int): X-coordinate.
            y (int): Y-coordinate.
            
        Returns:
            bool: True if successful, False if invalid coordinates or position empty.
        """
        if not self.validate_coord(x, y) or (x, y) not in self.board:
            return False
        del self.board[(x, y)]
        return True

    def get_board_state(self):
        """Return the entire board state.
        
        Returns:
            dict: Copy of the board state dictionary.
        """
        return self.board.copy()
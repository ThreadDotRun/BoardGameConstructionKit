# BoardGame SQLite 🕹️

A Python library for managing a 2D game board with SQLite persistence, designed for board game applications. The `BoardGame` class allows you to set, retrieve, update, and remove attributes at board positions, with state stored in a SQLite database (in-memory or file-based). Comprehensive unit tests ensure reliability.

![Python](https://img.shields.io/badge/Python-3.6+-blue.svg)
![SQLite](https://img.shields.io/badge/SQLite-3.0+-green.svg)
![License](https://img.shields.io/badge/license-MIT-orange.svg)

## 📖 Overview

This project provides a `BoardGame` class to manage a square game board (n x n) where each position can hold attributes (e.g., `unit: tank`, `health: 5`) stored as key-value pairs. The board state is persisted using SQLite, supporting both in-memory (for testing) and file-based storage (for persistence across sessions). The included test suite (`TestBoardGame.py`) verifies all functionality, including initialization, coordinate validation, position operations, and persistence.

## ✨ Features

- 🗺️ **2D Board Management**: Initialize a square board of any size and manage positions with attributes.
- 💾 **SQLite Persistence**: Store board state in SQLite (in-memory or file-based) for durability.
- 🔧 **Flexible Operations**:
  - Set attributes at a position (e.g., `set_position(x, y, [['unit', 'tank'], ['health', 5]])`).
  - Retrieve attributes (`get_position(x, y)`).
  - Update specific attributes (`update_attribute(x, y, key, value)`).
  - Remove attributes (`remove_position(x, y)`).
  - Get a copy of the board state (`get_board_state()`).
- ✅ **Comprehensive Tests**: 8 unit tests cover all methods and SQLite persistence.
- 🛠️ **Error Handling**: Robust coordinate validation and database cleanup.

## 🚀 Getting Started

### Prerequisites

- 🐍 Python 3.6 or higher
- 📦 SQLite (included in Python’s standard library via `sqlite3`)

### Installation

1. **Clone the repository**:
   ```bash
   git clone https://github.com/your-username/boardgame-sqlite.git
   cd boardgame-sqlite
   ```

2. **No dependencies required**! The project uses only Python’s standard library (`sqlite3`, `json`, `unittest`, `os`).

### Usage

1. **Using the BoardGame class**:
   ```python
   from board_game import BoardGame

   # Initialize a 5x5 board with file-based SQLite
   game = BoardGame(size=5, db_name="game.db")

   # Set attributes at position (2, 3)
   game.set_position(2, 3, [["unit", "tank"], ["health", 5]])

   # Retrieve attributes
   print(game.get_position(2, 3))  # [['unit', 'tank'], ['health', 5]]

   # Update an attribute
   game.update_attribute(2, 3, "health", 3)
   print(game.get_position(2, 3))  # [['unit', 'tank'], ['health', 3]]

   # Remove position
   game.remove_position(2, 3)
   print(game.get_position(2, 3))  # None

   # Close database connection
   game.close()
   ```

2. **Running Tests**:
   ```bash
   python3 TestBoardGame.py
   ```
   Expected output:
   ```
   === Setting up test ===
   Testing __init__
     __init__: Size and empty board - PASSED
   ...
   Testing persistence
     persistence: File-based persistence - PASSED
   Ran 8 tests in X.XXXs
   OK
   ```

## 📂 Project Structure

```
boardgame-sqlite/
├── README.md          📜 Project documentation
├── board_game.py      🕹️ BoardGame class with SQLite persistence
├── TestBoardGame.py   🧪 Unit tests (includes BoardGame class)
├── header.txt         📄 Empty placeholder
├── footer.txt         📄 Empty placeholder
├── additional.txt     📄 Empty placeholder
```

- **board_game.py**: Defines the `BoardGame` class with SQLite-backed board management.
- **TestBoardGame.py**: Contains unit tests and an embedded `BoardGame` class to avoid import issues in some environments (e.g., Grok.com sandbox).
- **header.txt, footer.txt, additional.txt**: Empty placeholder files, reserved for future use (e.g., documentation or metadata).

## 🧪 Testing

The test suite (`TestBoardGame.py`) includes 8 unit tests covering:

1. `test_init`: Verifies board initialization.
2. `test_validate_coord`: Checks coordinate bounds.
3. `test_set_position`: Tests setting and overwriting attributes.
4. `test_get_position`: Ensures correct attribute retrieval.
5. `test_update_attribute`: Validates attribute updates and additions.
6. `test_remove_position`: Confirms position removal.
7. `test_get_board_state`: Tests board state retrieval and copy protection.
8. `test_persistence`: Verifies SQLite persistence (in-memory and file-based).

Run tests with:
```bash
python3 TestBoardGame.py
```

## 🤝 Contributing

Contributions are welcome! 🎉 Follow these steps:

1. Fork the repository.
2. Create a feature branch (`git checkout -b feature/YourFeature`).
3. Commit changes (`git commit -m 'Add YourFeature'`).
4. Push to the branch (`git push origin feature/YourFeature`).
5. Open a Pull Request.

Please ensure tests pass and add new tests for new features.

## 📝 License

This project is licensed under the MIT License. See [LICENSE](LICENSE) for details.

## 🙌 Acknowledgments

- Built with ❤️ using Python and SQLite.
- Inspired by board game mechanics and persistent storage needs.

---

⭐ **Star this repo** if you find it useful!  
📧 For questions, open an [issue](https://github.com/your-username/boardgame-sqlite/issues) or contact the maintainer.
# 🧠 Quoridor Game AI Project

A Python implementation of the strategic board game **Quoridor**, supporting both human and AI players. The project is modular and object-oriented, with core components managing players, board state, and movement logic. It includes support for wall placement validation using BFS to ensure fair gameplay.

---

## 📁 Project Structure

```text
├── Board.py         # Main board logic and game state
├── Player.py        # Player logic (movement, validation)
├── AIPlayer.py      # (Expected) AI behavior for Player 2
├── README.md        # Project documentation
```

---

## 🎮 Game Overview

* **Game Board:** 9x9 pawn grid with a 17x17 matrix internally, to account for walls between cells.
* **Players:** Two players (human vs human or human vs AI).
* **Objective:** Reach the opposite side of the board.
* **Movement:** Includes direct and diagonal movement with validation.
* **Walls:** Players can place walls to block opponents, but must not completely block access to the goal.

---

## 🧩 Core Components

### `Board` Class (`Board.py`)

Handles the game state and initialization.

#### Attributes:

* `dimPawnBoard`: Size of the pawn grid (default 9).
* `dimWallBoard`: Space between cells for walls (8).
* `dimBoard`: Total grid size (17x17).
* `board`: 2D NumPy array representing the board.
* `p1`, `p2`: Instances of `Player` or `AIPlayer`.

#### Methods:

* `__init__(dim=9, againest_ai=False)`: Initializes the board, including players and dimensions.
* `get_state()`: Returns a snapshot of the current game state.

---

### `Player` Class (`Player.py`)

Represents a player in the game with movement and wall-checking logic.

#### Attributes:

* `id`: Player number (1 or 2).
* `pos`: Current position on the board.
* `available_walls`: Number of remaining walls.
* `objective`: Row the player must reach to win.
* `color`: Player color (for UI, if used).

#### Movement Methods:

* `handle_move(direction)`: Handles move input and validates it.
* `move(direction)`: Calls appropriate movement check (top, down, diagonal, etc.).
* `checkDirection(axis, dir)`: Validates movement in cardinal directions.
* `checkDiagonalDirection(x_dir, y_dir)`: Validates diagonal movement.

#### Validation Method:

* `WallRestrictionAlgorithmsBFS(new_board)`: Checks if players can reach their goals using BFS. Prevents wall placements that would completely block a player.

---

## 🧠 AIPlayer

You referenced `AIPlayer` in `Board.py`, though the file wasn't provided. It likely inherits from `Player` and overrides some decision-making methods to make intelligent moves based on the game state.

---

## 🛠 Setup Instructions

1. Clone the repository:

   ```bash
   git clone https://github.com/your-username/Quoridor-Game-AI-Project.git
   cd Quoridor-Game-AI-Project
   ```

2. Install dependencies:

   ```bash
   pip install numpy
   ```

3. Run the game:

   ```bash
   python main.py  # if a main file is created
   ```

---

## 📌 Future Improvements

* Add `AIPlayer.py` logic for smarter decisions.
* Implement a full game loop (CLI or GUI).
* Add wall placement interface.
* Visualize the board using Pygame or Tkinter.

---



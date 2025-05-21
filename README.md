# Quoridor-Game-AI-Project
# Quoridor AI Project Documentation

## Overview
This project implements an AI player for the classic board game Quoridor using Python and Pygame. The AI uses alpha-beta pruning with a heuristic evaluation function to make strategic decisions about pawn movement and wall placement.

## Game Rules (Brief)
Quoridor is a 2-player strategy game where:
- Each player controls a pawn that must reach the opposite side of the board
- Players can either move their pawn or place walls to obstruct their opponent
- Walls cannot completely block a player's path to their goal
- The first player to reach their opposite side wins

## Code Structure

### Main Components

1. **Board.py** - Core game board implementation
   - Manages game state including player positions and wall placements
   - Provides methods to get and update the game state
   - Handles initialization of both human and AI players

2. **Player.py** - Base player class
   - Handles basic pawn movement logic
   - Validates wall placements using BFS pathfinding
   - Manages player attributes (position, walls remaining, color)

3. **AIPlayer.py** - AI player implementation
   - Extends the base Player class with AI capabilities
   - Implements alpha-beta pruning for decision making
   - Uses a heuristic function to evaluate board states
   - Generates valid moves considering game rules

4. **main.py** - Pygame GUI and game loop
   - Handles rendering of the board, players, and walls
   - Processes user input for human players
   - Manages game flow and turn switching
   - Displays game information and win conditions

5. **Config.py** - Game constants
   - Defines codes for different move types and wall orientations

### Key Algorithms

1. **Alpha-Beta Pruning**
   - Used by the AI to efficiently search possible moves
   - Cuts off branches that cannot possibly influence the final decision
   - Depth-limited to ensure reasonable performance

2. **Heuristic Evaluation**
   - Considers:
     - Path distance to goal for both players
     - Number of walls remaining
     - Immediate win conditions
   - Weighted to balance offensive and defensive play

3. **Pathfinding (BFS)**
   - Used both for wall placement validation and heuristic calculation
   - Ensures players always have a path to their goal
   - Efficiently checks reachability from current positions

## How the AI Works

The AI makes decisions using the following process:

1. **Move Generation**
   - Enumerates all legal pawn moves considering:
     - Basic movement (up, down, left, right)
     - Jumping over opponent pawns
     - Diagonal moves when blocked
   - Generates valid wall placements that don't block paths

2. **Board Evaluation**
   - For each possible move, evaluates the resulting board state using:
     - Difference in path lengths to goal
     - Wall advantage (bonus for having more walls remaining)
     - Immediate win/loss conditions

3. **Search Algorithm**
   - Uses alpha-beta pruning to explore possible moves
   - Looks ahead specified number of turns (search_depth)
   - Selects move leading to most advantageous future position

## How to Run

1. Install dependencies:
   ```
   pip install pygame numpy
   ```

2. Run the game:
   ```
   python main.py
   ```

3. Game controls:
   - Use arrow keys for basic movement
   - Q/E/Z/C for diagonal moves
   - Click to place walls (select two connected positions)

## Customization Options

The game can be customized by modifying:

- Board size (in Board.py)
- AI search depth (in AIPlayer.py initialization)
- Visual parameters like colors and sizes (in main.py)
- Heuristic weights (wall_bonus_weight in AIPlayer.py)

## Implementation Challenges

1. **Move Validation**
   - Complex rules for pawn movement and jumping
   - Ensuring wall placements don't block paths completely

2. **Performance Optimization**
   - Efficient board state representation
   - Minimizing expensive pathfinding calculations
   - Balancing AI search depth with responsiveness

3. **Game State Representation**
   - Hybrid board tracking both pawn positions and walls
   - Virtual board for AI simulation of future moves

## Future Improvements

1. **Enhanced AI**
   - More sophisticated heuristic evaluation
   - Opening book for common starting moves
   - Adaptive search depth based on game phase

2. **UI Improvements**
   - Animated moves
   - Move history and undo functionality
   - Improved wall placement visualization

3. **Multiplayer Options**
   - Network play
   - Tournament mode with multiple AI difficulty levels

## Dependencies

- Python 3.x
- Pygame (for GUI)
- NumPy (for efficient board representation)

This implementation provides a strong foundation for a Quoridor AI that balances strategic decision-making with performance considerations. The modular design makes it easy to extend or modify components like the AI strategy or game rules.

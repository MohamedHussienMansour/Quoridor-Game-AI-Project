from Player import Player
from Config import VERTICAL_CONNECTOR_CODE, HORIZONTAL_CONNECTOR_CODE
import math
from collections import deque
import time
import pickle

class AIPlayer(Player):
    def __init__(self, *args, search_depth=1, wall_bonus_weight=1.2, **kwargs):
        super().__init__(*args, **kwargs)
        self.search_depth = search_depth
        self.wall_bonus_weight = wall_bonus_weight

    def apply_move(self, virtual_board, move, maximizing_player, is_virtural=True):
        if is_virtural:
            new_virtual_board = pickle.loads(pickle.dumps(virtual_board, protocol=-1))
            if move[0] == 'move':
                new_virtual_board[2][virtual_board[maximizing_player][0][0], virtual_board[maximizing_player][0][1]] = 0
                new_virtual_board[maximizing_player][0] = move[1]
                new_virtual_board[2][new_virtual_board[maximizing_player][0][0], new_virtual_board[maximizing_player][0][1]] = self.board.p2.id if maximizing_player else  self.board.p1.id
                
            else:
                coordinate1, coordinate2, coordinate3 = move[1]

                new_virtual_board[2][coordinate1[0], coordinate1[1]] = 1
                new_virtual_board[2][coordinate2[0], coordinate2[1]] = HORIZONTAL_CONNECTOR_CODE if coordinate1[0] == coordinate2[0] else VERTICAL_CONNECTOR_CODE
                new_virtual_board[2][coordinate3[0], coordinate3[1]] = 1
            
            return new_virtual_board
        else:
            board = virtual_board
            player = board.p2 if maximizing_player else board.p1
            
            if move[0] == 'move':
                board.board[player.pos[0], player.pos[1]] = 0
                player.pos = move[1]
                board.board[player.pos[0], player.pos[1]] = player.id
                
            else:
                coordinate1, coordinate2, coordinate3 = move[1]

                board.board[coordinate1[0], coordinate1[1]] = 1
                board.board[coordinate2[0], coordinate2[1]] = HORIZONTAL_CONNECTOR_CODE if coordinate1[0] == coordinate2[0] else VERTICAL_CONNECTOR_CODE
                board.board[coordinate3[0], coordinate3[1]] = 1

            return board

    
    def get_valid_moves(self, virtual_board, maximizing_player):
        moves = []

        by, bx = virtual_board[1][0] if maximizing_player else virtual_board[0][0]
        oy, ox = virtual_board[0][0] if maximizing_player else virtual_board[1][0]
        remaining_walls = virtual_board[1][1] if maximizing_player else virtual_board[0][1]

        directions = {
            'up':    (-2, 0, -1, 0),
            'down':  (2, 0, 1, 0),
            'left':  (0, -2, 0, -1),
            'right': (0, 2, 0, 1),
        }

        for dir_name, (dy, dx, wy, wx) in directions.items():
            ny, nx = by + dy, bx + dx
            wall_y, wall_x = by + wy, bx + wx

            # Check for wall blocking movement
            if not (0 <= wall_y < self.board.dimBoard and 0 <= wall_x < self.board.dimBoard) or virtual_board[2][wall_y][wall_x]:
                continue

            # If moving into opponent's space
            if ny == oy and nx == ox:
                jump_y, jump_x = ny + dy, nx + dx
                jump_wall_y, jump_wall_x = ny + wy, nx + wx

                if (0 <= jump_y < self.board.dimBoard and 0 <= jump_x < self.board.dimBoard and 
                    not virtual_board[2][jump_wall_y][jump_wall_x] and 
                    not virtual_board[2][jump_y][jump_x]):
                    # Jump over opponent
                    moves.append(('move', [jump_y, jump_x]))
                    continue

                # Side steps if jump is blocked
                if dy != 0:  # up/down → try left/right side steps
                    for sdx, swx in [(-2, -1), (2, 1)]:
                        side_y, side_x = ny, nx + sdx
                        wall_side_y, wall_side_x = ny, nx + swx
                        if (0 <= side_x < self.board.dimBoard and not virtual_board[2][wall_side_y][wall_side_x] and 
                            not virtual_board[2][side_y][side_x]):
                            moves.append(('move', [side_y, side_x]))
                else:  # left/right → try up/down side steps
                    for sdy, swy in [(-2, -1), (2, 1)]:
                        side_y, side_x = ny + sdy, nx
                        wall_side_y, wall_side_x = ny + swy, nx
                        if (0 <= side_y < self.board.dimBoard and not virtual_board[2][wall_side_y][wall_side_x] and 
                            not virtual_board[2][side_y][side_x]):
                            moves.append(('move', [side_y, side_x]))
            else:
                if 0 <= ny < self.board.dimBoard and 0 <= nx < self.board.dimBoard and not virtual_board[2][ny][nx]:
                    moves.append(('move', [ny, nx]))

        # Wall placements — return full wall parts as 3 coordinate tuples
        if remaining_walls > 0:
            for y in range(1, self.board.dimBoard - 1, 2):  # odd y
                for x in range(1, self.board.dimBoard - 1, 2):  # odd x
                    # Horizontal wall: spans (y, x-1), (y, x), (y, x+1)
                    if (x >= 1 and x <= self.board.dimBoard - 2 and
                        not virtual_board[2][y][x - 1] and
                        not virtual_board[2][y][x] and
                        not virtual_board[2][y][x + 1]):
                        moves.append(('wall', [(y, x - 1), (y, x), (y, x + 1)]))

                    # Vertical wall: spans (y-1, x), (y, x), (y+1, x)
                    if (y >= 1 and y <= self.board.dimBoard - 2 and
                        not virtual_board[2][y - 1][x] and
                        not virtual_board[2][y][x] and
                        not virtual_board[2][y + 1][x]):
                        moves.append(('wall', [(y - 1, x), (y, x), (y + 1, x)]))

        return moves

    def heuristic(self, virtual_board):
        """Simplified and more effective heuristic function using virtual_board[2]"""
        def calculate_path(y, x, target_row):
            visited = [[False] * self.board.dimBoard for _ in range(self.board.dimBoard)]
            queue = deque([(y, x, 0)])
            visited[y][x] = True

            while queue:
                cy, cx, steps = queue.popleft()
                if cy == target_row:
                    return steps
                # Up
                if cy >= 2 and not virtual_board[2][cy - 1][cx] and not visited[cy - 2][cx]:
                    visited[cy - 2][cx] = True
                    queue.append((cy - 2, cx, steps + 1))
                # Down
                if cy <= self.board.dimBoard - 2 and not virtual_board[2][cy + 1][cx] and not visited[cy + 2][cx]:
                    visited[cy + 2][cx] = True
                    queue.append((cy + 2, cx, steps + 1))
                # Left
                if cx >= 2 and not virtual_board[2][cy][cx - 1] and not visited[cy][cx - 2]:
                    visited[cy][cx - 2] = True
                    queue.append((cy, cx - 2, steps + 1))
                # Right
                if cx <= self.board.dimBoard - 2 and not virtual_board[2][cy][cx + 1] and not visited[cy][cx + 2]:
                    visited[cy][cx + 2] = True
                    queue.append((cy, cx + 2, steps + 1))

            return float('inf')  # No path found

        p1_path = calculate_path(virtual_board[0][0][0], virtual_board[0][0][1], self.board.p1.objective)
        p2_path = calculate_path(virtual_board[1][0][0], virtual_board[1][0][1], self.board.p2.objective)

        # Base score components
        path_diff = (p1_path - p2_path)

        # Wall bonus calculation
        wall_bonus = virtual_board[1][1] * self.wall_bonus_weight

        # Immediate win conditions
        if p1_path == 0:
            return -math.inf
        if p2_path == 0:
            return math.inf

        return path_diff + wall_bonus


    def alpha_beta(self, virtual_board, depth, alpha, beta, maximizing_player):
        """Optimized alpha-beta pruning using virtual_board[2]"""
        if virtual_board[0][0][0] == self.board.p1.objective:
            return -math.inf if maximizing_player else math.inf
        if virtual_board[1][0][0] == self.board.p2.objective:
            return math.inf if maximizing_player else -math.inf

        if depth == 0:
            return self.heuristic(virtual_board)

        valid_moves = self.get_valid_moves(virtual_board, maximizing_player)

        valid_moves.sort(key=lambda m: 0 if m[0] == 'move' and (
            (maximizing_player and m[1] == self.board.p2.objective) or
            (not maximizing_player and m[1] == self.board.p1.objective)
        ) else 1)

        if maximizing_player:
            max_eval = -math.inf
            for move in valid_moves:
                next_virtual_board = self.apply_move(virtual_board, move, maximizing_player)
                eval = self.alpha_beta(next_virtual_board, depth - 1, alpha, beta, False)
                max_eval = max(max_eval, eval)
                alpha = max(alpha, eval)
                if beta <= alpha:
                    break
            return max_eval
        else:
            min_eval = math.inf
            for move in valid_moves:
                next_virtual_board = self.apply_move(virtual_board, move, maximizing_player)
                eval = self.alpha_beta(next_virtual_board, depth - 1, alpha, beta, True)
                min_eval = min(min_eval, eval)
                beta = min(beta, eval)
                if beta <= alpha:
                    break
            return min_eval

    # Update ai_move function
    def ai_move(self):
        virtual_board = self.board.get_state()

        best_move = None
        best_value = -math.inf
        valid_moves = self.get_valid_moves(virtual_board, True)
        
        for move in valid_moves:
            next_virtual_board = self.apply_move(virtual_board, move, True)
            
            value = self.alpha_beta(next_virtual_board, self.search_depth, -math.inf, math.inf, False)
            
            if value > best_value:
                best_value = value
                best_move = move
    
        self.apply_move(self.board, best_move, True, is_virtural=False)


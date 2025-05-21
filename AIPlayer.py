from Player import Player
from Config import WALL_MOVE_CODE, PAWN_MOVE_CODE, VERTICAL_CONNECTOR_CODE, HORIZONTAL_CONNECTOR_CODE
import math
from collections import deque
import heapq

class AIPlayer(Player):
    def __init__(self, *args, search_depth=1, wall_bonus_weight=1, **kwargs):
        super().__init__(*args, **kwargs)
        self.search_depth = search_depth
        self.wall_bonus_weight = wall_bonus_weight

    def apply_move(self, virtual_board, move, maximizing_player, is_virtural=True):
        if is_virtural:
            new_virtual_board = [
                [virtual_board[0][0].copy(), virtual_board[0][1]],
                [virtual_board[1][0].copy(), virtual_board[1][1]],
                virtual_board[2].copy()
            ]

            if move[0] == PAWN_MOVE_CODE:
                new_virtual_board[2][virtual_board[maximizing_player][0][0], virtual_board[maximizing_player][0][1]] = 0
                new_virtual_board[maximizing_player][0] = move[1]
                new_virtual_board[2][new_virtual_board[maximizing_player][0][0], new_virtual_board[maximizing_player][0][1]] = self.board.p2.id if maximizing_player else self.board.p1.id

            else:
                coordinate1, coordinate2, coordinate3 = move[1]

                new_virtual_board[2][coordinate1[0], coordinate1[1]] = 1
                new_virtual_board[2][coordinate2[0], coordinate2[1]] = HORIZONTAL_CONNECTOR_CODE if coordinate1[0] == coordinate2[0] else VERTICAL_CONNECTOR_CODE
                new_virtual_board[2][coordinate3[0], coordinate3[1]] = 1

                new_virtual_board[maximizing_player][1] -= 1

            return new_virtual_board
        else:
            board = virtual_board
            player = board.p2 if maximizing_player else board.p1

            if move[0] == PAWN_MOVE_CODE:
                board.board[player.pos[0], player.pos[1]] = 0
                player.pos = move[1]
                board.board[player.pos[0], player.pos[1]] = player.id

            else:
                coordinate1, coordinate2, coordinate3 = move[1]

                board.board[coordinate1[0], coordinate1[1]] = 1
                board.board[coordinate2[0], coordinate2[1]] = HORIZONTAL_CONNECTOR_CODE if coordinate1[0] == coordinate2[0] else VERTICAL_CONNECTOR_CODE
                board.board[coordinate3[0], coordinate3[1]] = 1

                player.available_walls -= 1

            return board

    def get_valid_moves(self, virtual_board, maximizing_player):
        moves = []

        # Determine player positions and remaining walls
        by, bx = virtual_board[1][0] if maximizing_player else virtual_board[0][0]
        oy, ox = virtual_board[0][0] if maximizing_player else virtual_board[1][0]
        remaining_walls = virtual_board[1][1] if maximizing_player else virtual_board[0][1]

        # Directions for pawn moves
        directions = {
            'up':    (-2, 0, -1, 0),
            'down':  (2, 0, 1, 0),
            'left':  (0, -2, 0, -1),
            'right': (0, 2, 0, 1),
        }

        # Helper: check path exists from start to any goal row
        def has_path(board, start, goal_rows):
            from collections import deque
            visited = [[False]*self.board.dimBoard for _ in range(self.board.dimBoard)]
            dq = deque([tuple(start)])
            visited[start[0]][start[1]] = True
            while dq:
                y, x = dq.popleft()
                if y in goal_rows:
                    return True
                for dy, dx, wy, wx in directions.values():
                    ny, nx = y + dy, x + dx
                    wy_, wx_ = y + wy, x + wx
                    if (0 <= ny < self.board.dimBoard and 0 <= nx < self.board.dimBoard
                            and not board[2][wy_][wx_] and not visited[ny][nx]):
                        visited[ny][nx] = True
                        dq.append((ny, nx))
            return False

        # Generate pawn moves
        for dy, dx, wy, wx in directions.values():
            ny, nx = by + dy, bx + dx
            wall_y, wall_x = by + wy, bx + wx
            # Skip if wall blocks direct move or out of bounds
            if not (0 <= wall_y < self.board.dimBoard and 0 <= wall_x < self.board.dimBoard) or virtual_board[2][wall_y][wall_x]:
                continue
            # Opponent jump logic
            if (ny, nx) == (oy, ox):
                # Attempt jump
                jy, jx = ny + dy, nx + dx
                jwy, jwx = ny + wy, nx + wx
                if (0 <= jy < self.board.dimBoard and 0 <= jx < self.board.dimBoard
                        and not virtual_board[2][jwy][jwx] and not virtual_board[2][jy][jx]):
                    moves.append((PAWN_MOVE_CODE, [jy, jx]))
                    continue
                # Side steps
                if dy != 0:
                    for sdx, swx in [(-2, -1), (2, 1)]:
                        sy, sx = ny, nx + sdx
                        swy, swx = ny, nx + swx
                        if (0 <= sx < self.board.dimBoard
                                and not virtual_board[2][swy][swx] and not virtual_board[2][sy][sx]):
                            moves.append((PAWN_MOVE_CODE, [sy, sx]))
                else:
                    for sdy, swy in [(-2, -1), (2, 1)]:
                        sy, sx = ny + sdy, nx
                        swy, swx = ny + swy, nx
                        if (0 <= sy < self.board.dimBoard
                                and not virtual_board[2][swy][swx] and not virtual_board[2][sy][sx]):
                            moves.append((PAWN_MOVE_CODE, [sy, sx]))
            else:
                if (0 <= ny < self.board.dimBoard and 0 <= nx < self.board.dimBoard
                        and not virtual_board[2][ny][nx]):
                    moves.append((PAWN_MOVE_CODE, [ny, nx]))

        # Wall placements — ensure not caging any player
        if remaining_walls > 0:
            # Define goal rows for each player
            p2_goal = {
                True: range(self.objective, self.objective + 1),
                False: range(self.board.p1.objective, self.board.p1.objective + 1)
            }
            p1_goal = {
                True: range(self.board.p1.objective, self.board.p1.objective + 1),
                False: range(self.objective, self.objective + 1)
            }
            for y in range(1, self.board.dimBoard-1, 2):
                for x in range(1, self.board.dimBoard-1, 2):
                    # Try both horizontal and vertical
                    for coords in [[(y, x-1), (y, x), (y, x+1)], [(y-1, x), (y, x), (y+1, x)]]:
                        # Check cells free
                        if any(virtual_board[2][wy][wx] for wy, wx in coords):
                            continue
                        # Copy board and place wall
                        new_b = [
                            [virtual_board[0][0].copy(), virtual_board[0][1]],
                            [virtual_board[1][0].copy(), virtual_board[1][1]],
                            [row.copy() for row in virtual_board[2]]
                        ]
                        for wy, wx in coords:
                            new_b[2][wy][wx] = True
                        # Ensure both players have a path
                        if (has_path(new_b, new_b[1][0], p2_goal[maximizing_player]) and
                                has_path(new_b, new_b[0][0], p1_goal[maximizing_player])):
                            moves.append((WALL_MOVE_CODE, coords))
        return moves



    def heuristic(self, virtual_board):
        """Heuristic function using A* for both players"""
        def manhattan_distance(y1, x1, y2):
            return abs(y1 - y2)  # Only vertical movement matters for goal row

        def a_star_path(y, x, target_row):
            visited = [[False] * self.board.dimBoard for _ in range(self.board.dimBoard)]
            heap = [(manhattan_distance(y, x, target_row), 0, y, x)]  # (f, g, y, x)

            while heap:
                f, g, cy, cx = heapq.heappop(heap)
                if cy == target_row:
                    return g
                if visited[cy][cx]:
                    continue
                visited[cy][cx] = True

                # Directions: (dy, dx, wall_y, wall_x)
                directions = [
                    (-2, 0, cy - 1, cx),  # Up
                    (2, 0, cy + 1, cx),   # Down
                    (0, -2, cy, cx - 1),  # Left
                    (0, 2, cy, cx + 1)    # Right
                ]

                for dy, dx, wy, wx in directions:
                    ny, nx = cy + dy, cx + dx
                    if 0 <= ny < self.board.dimBoard and 0 <= nx < self.board.dimBoard:
                        if not virtual_board[2][wy][wx] and not visited[ny][nx]:
                            h = manhattan_distance(ny, nx, target_row)
                            heapq.heappush(heap, (g + 1 + h, g + 1, ny, nx))

            return math.inf  # No path found

        p1_path = a_star_path(virtual_board[0][0][0], virtual_board[0][0][1], self.board.p1.objective)
        p2_path = a_star_path(virtual_board[1][0][0], virtual_board[1][0][1], self.objective)

        path_diff = (p1_path - p2_path) * 4
        wall_bonus = virtual_board[1][1] * self.wall_bonus_weight

        if p1_path == 0:
            return -math.inf
        if p2_path == 0:
            return math.inf

        return path_diff + wall_bonus



    def alpha_beta(self, virtual_board, depth, alpha, beta, maximizing_player):
        """Optimized alpha-beta pruning using virtual_board[2]"""
        if virtual_board[0][0][0] == self.board.p1.objective:
            return -math.inf if maximizing_player else math.inf
        if virtual_board[1][0][0] == self.objective:
            return math.inf if maximizing_player else -math.inf

        if depth == 0:
            return self.heuristic(virtual_board)

        valid_moves = self.get_valid_moves(virtual_board, maximizing_player)

        valid_moves.sort(key=lambda m: 0 if m[0] == PAWN_MOVE_CODE and (
            (maximizing_player and m[1][0] == self.board.p2.objective) or
            (not maximizing_player and m[1][0] == self.board.p1.objective)
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

        fast_win_move = next((m for m in valid_moves if m[0] == PAWN_MOVE_CODE and m[1][0] == self.board.p2.objective), None)

        if not fast_win_move:
            for move in valid_moves:
                next_virtual_board = self.apply_move(virtual_board, move, True)
                value = self.alpha_beta(next_virtual_board, self.search_depth, -math.inf, math.inf, False)

                if value > best_value:
                    best_value = value
                    best_move = move

            self.apply_move(self.board, best_move, True, is_virtural=False)

        else:
            self.apply_move(self.board, fast_win_move, True, is_virtural=False)


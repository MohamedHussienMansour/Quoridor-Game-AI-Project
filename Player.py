from collections import deque

class Player:
    colors = ["#467C9E", "#E63946"]
    players = []
    pid = 1

    def __init__(self, board, pos, objective, available_walls=10):
        self.objective = objective
        self.id = Player.pid
        self.pos = pos
        self.available_walls = available_walls
        self.board = board
        self.board.board[pos[0], pos[1]] = self.id
        self.color = Player.colors[self.id - 1]

        Player.pid += 1
        Player.players.append(self)

    def handle_move(self, direction):
        if not self.move(direction):
            print("Invalid Move")
            return False

        return True

    def checkDirection(self, movement_axis, movement_direction):
        if self.pos[movement_axis] + 2 * movement_direction < 0:
            return False
        if self.pos[movement_axis] + 2 * movement_direction >= self.board.dimBoard:
            return False

        if movement_axis == 0:
            if self.board.board[self.pos[0] + movement_direction, self.pos[1]] != 0:
                return False
            if self.board.board[self.pos[0] + 2 * movement_direction, self.pos[1]] != 0:
                if self.pos[0] + 4 * movement_direction < 0:
                    return False
                if self.pos[0] + 4 * movement_direction >= self.board.dimBoard:
                    return False
                if self.board.board[self.pos[0] + 3 * movement_direction, self.pos[1]] != 0:
                    return False

                self.board.board[self.pos[0], self.pos[1]] = 0
                self.pos[0] = self.pos[0] + 4 * movement_direction
                self.board.board[self.pos[0], self.pos[1]] = self.id

                return True

        elif movement_axis == 1:
            if self.board.board[self.pos[0], self.pos[1] + movement_direction] != 0:
                return False
            if self.board.board[self.pos[0], self.pos[1] + 2 * movement_direction] != 0:
                if self.pos[1] + 4 * movement_direction < 0:
                    return False
                if self.pos[1] + 4 * movement_direction >= self.board.dimBoard:
                    return False
                if self.board.board[self.pos[0], self.pos[1] + 3 * movement_direction] != 0:
                    return False


                self.board.board[self.pos[0], self.pos[1]] = 0
                self.pos[1] = self.pos[1] + 4 * movement_direction
                self.board.board[self.pos[0], self.pos[1]] = self.id

                return True

        self.board.board[self.pos[0], self.pos[1]] = 0
        self.pos[movement_axis] = self.pos[movement_axis] + 2 * movement_direction
        self.board.board[self.pos[0], self.pos[1]] = self.id

        return True

    def checkDiagonalDirection(self, x_direction, y_direction):
        # Check if move is out of bounds for either axis
        if self.pos[0] + 2 * x_direction < 0 or self.pos[1] + 2 * y_direction < 0:
            return False

        player_in_x = self.board.board[self.pos[0] + 2 * x_direction, self.pos[1]] != 0
        player_in_y = self.board.board[self.pos[0], self.pos[1] + 2 * y_direction] != 0

        # Check if there is a player two steps away in x or y direction
        if player_in_x or player_in_y:
            if player_in_x:
                # Check if jump over player in x direction is out of bounds
                if self.pos[0] + 4 * x_direction < 0:
                    return False
                # Check if there is a wall beyond the player
                if self.board.board[self.pos[0] + 3 * x_direction, self.pos[1]] == 0:
                    return False
                # Check if there is a wall restricting the move
                if self.board.board[self.pos[0] + 2 * x_direction, self.pos[1] + y_direction] != 0:
                    return False

            if player_in_y:
                # Check if jump over player in y direction is out of bounds
                if self.pos[1] + 4 * y_direction < 0:
                    return False
                # Check if there is a wall beyond the player
                if self.board.board[self.pos[0], self.pos[1] + 3 * y_direction] == 0:
                    return False
                # Check if there is a wall restricting the move
                if self.board.board[self.pos[0] + x_direction, self.pos[1] + 2 * y_direction] != 0:
                    return False

            # Valid jump: clear current position and update position
            self.board.board[self.pos[0], self.pos[1]] = 0
            self.pos[0] += 2 * x_direction
            self.pos[1] += 2 * y_direction
            self.board.board[self.pos[0], self.pos[1]] = self.id
            return True

        return False

    def move(self, direction):
        if direction == "top":
            return self.checkDirection(0, -1)

        elif direction == "down":
            return self.checkDirection(0, 1)

        elif direction == "right":
            return self.checkDirection(1, 1)

        elif direction == "left":
            return self.checkDirection(1, -1)

        elif direction == "topLeft":
            return self.checkDiagonalDirection(-1, -1)

        elif direction == "topRight":
            return self.checkDiagonalDirection(1, -1)

        elif direction == "downLeft":
            return self.checkDiagonalDirection(-1, 1)

        elif direction == "downRight":
            return self.checkDiagonalDirection(1, 1)

    def WallRestrictionAlgorithmsBFS(self, new_board):
        directions = [(-2, 0), (2, 0), (0, -2), (0, 2)]  # up, down, left, right
        wall_offsets = [(-1, 0), (1, 0), (0, -1), (0, 1)]  # walls are between tiles

        for player in Player.players:
            start_y, start_x = player.pos
            visited = set()
            queue = deque([(start_y, start_x)])
            visited.add((start_y, start_x))

            # Determine the goal row based on the player's objective
            goal_row = player.objective

            found_path = False
            while queue:
                y, x = queue.popleft()

                if y == goal_row:
                    found_path = True
                    break  # Found path to the goal row, no need to continue BFS for this player

                for (dy, dx), (wy, wx) in zip(directions, wall_offsets):
                    ny, nx = y + dy, x + dx
                    wy, wx = y + dy // 2, x + dx // 2

                    # Check bounds
                    if 0 <= ny < self.board.dimBoard and 0 <= nx < self.board.dimBoard:
                        # Check for wall between current and new position
                        if new_board[wy, wx] == 0 and new_board[ny, nx] == 0:
                            if (ny, nx) not in visited:
                                visited.add((ny, nx))
                                queue.append((ny, nx))

            if not found_path:
                return False  # This player is restricted, so the board state is invalid

        return True  # Both players can reach their goals

import pygame

## start test boards ##
#############################
# initialize board
test_board = [[0 for _ in range(17)] for _ in range(17)]

# Players moved
test_board[4][8] = 1  # Player 1
test_board[12][8] = 2  # Player 2

# walls placed
test_board[5][6] = 1
test_board[5][8] = 1
test_board[5][7] = 1

## end test boards ##
#############################


PLAYER_1_CODE = 1
PLAYER_2_CODE = 2

HORIZONTAL_CONNECTOR_CODE = 1
VERTICAL_CONNECTOR_CODE = 2


class GameGUI:
    def __init__(
        self,
        board,
        screen_width=800,
        screen_height=600,
        game_size=9,
        margin=10,
        wall_to_wall_gap=8,
    ):
        pygame.init()
        self.board = board
        self.screen_width = screen_width
        self.screen_height = screen_height
        self.game_size = game_size
        self.margin = margin
        self.wall_to_wall_gap = wall_to_wall_gap

        self.hovered_pos = None
        self.first_wall_part = None

        self.game_surface_side = min(self.screen_height, self.screen_width) * 0.9
        self.game_x_pos = (self.screen_width - self.game_surface_side) / 2
        self.game_y_pos = (self.screen_height - self.game_surface_side) / 2

        self.cell_side = round(
            (self.game_surface_side - ((game_size + 1) * self.margin)) / self.game_size
        )
        self.player_radius = round(self.cell_side * 0.4)

        self.screen = pygame.display.set_mode((self.screen_width, self.screen_height))
        self.clock = pygame.time.Clock()
        self.running = True
        self.dt = 0

    def get_hovered_board_position(self, mouse_pos):
        x_offset = mouse_pos[0] - self.game_x_pos
        y_offset = mouse_pos[1] - self.game_y_pos

        if not (
            0 <= x_offset < self.game_surface_side
            and 0 <= y_offset < self.game_surface_side
        ):
            return None

        for y in range(len(self.board)):
            for x in range(len(self.board[y])):
                is_wall = y % 2 != x % 2  # wall positions only
                if not is_wall:
                    continue

                left, top = self.map_board_pos(x, y)
                width = self.margin if x % 2 == 1 else self.cell_side
                height = self.margin if y % 2 == 1 else self.cell_side

                rect = pygame.Rect(
                    left + self.game_x_pos, top + self.game_y_pos, width, height
                )
                if rect.collidepoint(mouse_pos):
                    return (x, y)
        return None

    def handle_click(self):
        if self.hovered_pos is None:
            return

        x, y = self.hovered_pos

        if self.first_wall_part is None:
            if self.board[y][x] == 0:
                self.board[y][x] = 1
                self.first_wall_part = (x, y)
        else:
            fx, fy = self.first_wall_part
            if (y, x) == (fy, fx):
                self.board[y][x] = 0
                self.first_wall_part = None
            elif self.is_valid_second_part(x, y, fx, fy):
                # Set second part
                self.board[y][x] = 1
                my = (fy + y) // 2
                mx = (fx + x) // 2
                self.board[my][mx] = (
                    HORIZONTAL_CONNECTOR_CODE if y == fy else VERTICAL_CONNECTOR_CODE
                )
                self.first_wall_part = None

    def is_valid_second_part(self, x, y, fx, fy):
        if self.board[y][x] != 0:
            return False

        if fy % 2 == 1 and fx % 2 == 0:
            # Horizontal wall
            if y != fy or abs(x - fx) != 2:
                return False  # Must be 2 columns apart in same row
            my, mx = fy, (fx + x) // 2

            # Prevent crossing vertical wall (check above and below the midpoint)
            if (
                self.board[my - 1][mx] == 1
                and self.board[my][mx] == 2
                and self.board[my + 1][mx] == 1
            ):
                return False

        elif fy % 2 == 0 and fx % 2 == 1:
            # Vertical wall
            if x != fx or abs(y - fy) != 2:
                return False  # Must be 2 rows apart in same column
            my, mx = (fy + y) // 2, fx

            # Prevent crossing horizontal wall (check left and right of midpoint)
            if (
                self.board[my][mx - 1] == 1
                and self.board[my][mx] == 1
                and self.board[my][mx + 1] == 1
            ):
                return False
        else:
            return False

        return True

    def map_board_pos(self, x, y):
        left = (
            (x // 2) * (self.cell_side + self.margin)
            + (x % 2) * self.cell_side
            + self.margin
        )
        top = (
            (y // 2) * (self.cell_side + self.margin)
            + (y % 2) * self.cell_side
            + self.margin
        )

        return left, top

    def check_wall_type(self, x, y):
        is_vertical_wall = y % 2 == 0 and x % 2 == 1
        is_horizontal_wall = y % 2 == 1 and x % 2 == 0

        return is_horizontal_wall, is_vertical_wall

    def get_wall(self, x, y):
        is_horizontal_wall, is_vertical_wall = self.check_wall_type(x, y)

        left, top = self.map_board_pos(x, y)

        left = left + self.wall_to_wall_gap / 2 if is_horizontal_wall else left
        top = top + self.wall_to_wall_gap / 2 if is_vertical_wall else top
        height = (
            self.cell_side - self.wall_to_wall_gap if is_vertical_wall else self.margin
        )
        width = (
            self.margin if is_vertical_wall else self.cell_side - self.wall_to_wall_gap
        )

        return left, top, width, height

    def get_wall_connector(self, x, y, is_horizontal_connector, is_vertical_connector):
        left, top = self.map_board_pos(x, y)

        left = left - self.wall_to_wall_gap / 2 if is_horizontal_connector else left
        top = top - self.wall_to_wall_gap / 2 if is_vertical_connector else top
        width = (
            self.margin
            if is_vertical_connector
            else self.margin + self.wall_to_wall_gap
        )
        height = (
            self.margin
            if is_horizontal_connector
            else self.margin + self.wall_to_wall_gap
        )

        return left, top, width, height

    def draw_preview_wall(self, surface, x, y):
        color = (255, 255, 255, 120)
        left, top, width, height = self.get_wall(x, y)
        is_horizontal_wall, is_vertical_wall = self.check_wall_type(x, y)
        is_second_part = self.first_wall_part

        if is_vertical_wall or is_horizontal_wall:
            s = pygame.Surface((width, height), pygame.SRCALPHA)
            s.fill(color)
            surface.blit(s, (left, top))

        if is_second_part:
            fx, fy = self.first_wall_part
            connector_props = None

            if x + 2 == fx:
                connector_props = self.get_wall_connector(x + 1, y, True, False)
            elif x - 2 == fx:
                connector_props = self.get_wall_connector(x - 1, y, True, False)
            elif y + 2 == fy:
                connector_props = self.get_wall_connector(x, y + 1, False, True)
            elif y - 2 == fy:
                connector_props = self.get_wall_connector(x, y - 1, False, True)

            if connector_props:
                left, top, width, height = connector_props
                s = pygame.Surface((width, height), pygame.SRCALPHA)
                s.fill(color)
                surface.blit(s, (left, top))

    def handle_events(self):
        mouse_pos = pygame.mouse.get_pos()
        self.hovered_pos = self.get_hovered_board_position(mouse_pos)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False
            elif event.type == pygame.MOUSEBUTTONDOWN:
                self.handle_click()

    def draw_board(self):
        self.screen.fill("#f3f3f3")
        surface = pygame.Surface((self.game_surface_side, self.game_surface_side))
        surface.fill("#A66676")

        for y in range(len(self.board)):
            for x in range(len(self.board[y])):
                is_cell = y % 2 == 0 and x % 2 == 0
                is_horizontal_wall, is_vertical_wall = self.check_wall_type(x, y)
                is_connector = (
                    not (is_cell or is_vertical_wall or is_horizontal_wall)
                    and self.board[y][x] > 0
                )

                left, top = self.map_board_pos(x, y)
                width = self.cell_side
                height = self.cell_side

                if is_cell:
                    cell = pygame.Rect(left, top, width, height)
                    pygame.draw.rect(
                        surface,
                        pygame.Color("#611111"),
                        cell,
                        border_radius=round(self.cell_side * 0.1),
                    )

                if self.board[y][x] > 0 and is_cell:
                    player_pos = (
                        left + round(self.cell_side / 2),
                        top + round(self.cell_side / 2),
                    )
                    player_color = (
                        pygame.Color("#FFAAAA")
                        if self.board[y][x] == PLAYER_1_CODE
                        else pygame.Color("#FF0000")
                    )

                    pygame.draw.circle(
                        surface, player_color, player_pos, self.player_radius
                    )
                elif (is_vertical_wall or is_horizontal_wall) and self.board[y][x] > 0:
                    left, top, width, height = self.get_wall(x, y)
                    pygame.draw.rect(
                        surface,
                        pygame.Color("#F3F3F3"),
                        pygame.Rect(left, top, width, height),
                    )
                elif is_connector:
                    is_vertical_connector = self.board[y][x] == VERTICAL_CONNECTOR_CODE
                    is_horizontal_connector = (
                        self.board[y][x] == HORIZONTAL_CONNECTOR_CODE
                    )

                    left, top, width, height = self.get_wall_connector(
                        x, y, is_horizontal_connector, is_vertical_connector
                    )

                    connector = pygame.Rect(left, top, width, height)
                    pygame.draw.rect(surface, pygame.Color("#F3F3F3"), connector)

        if self.hovered_pos:
            x, y = self.hovered_pos

            if self.first_wall_part is None:
                if self.board[y][x] == 0:
                    self.draw_preview_wall(surface, x, y)
            else:
                fx, fy = self.first_wall_part
                if self.is_valid_second_part(x, y, fx, fy):
                    self.draw_preview_wall(surface, x, y)

        self.screen.blit(surface, (self.game_x_pos, self.game_y_pos))
        pygame.display.flip()

    def run(self):
        while self.running:
            self.handle_events()
            self.draw_board()
            self.dt = self.clock.tick(60) / 1000

        pygame.quit()


if __name__ == "__main__":
    # Initialize the game with test board
    game = GameGUI(test_board)
    game.run()

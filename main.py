import pygame
from Board import Board
from Config import HORIZONTAL_CONNECTOR_CODE, VERTICAL_CONNECTOR_CODE
import sys
import time

class GameGUI:
    def __init__(
        self,
        againest_ai=True,
        screen_width=800,
        screen_height=600,
        game_size=9,
        margin=10,
        wall_to_wall_gap=8,
        background_color="#333333",
        board_background_color="#929292",
        board_cell_color = "#1E1E2E",
        wall_color = "#99DD11"
    ):
        pygame.init()
        self.board = Board(againest_ai=againest_ai)
        self.screen_width = screen_width
        self.screen_height = screen_height
        self.game_size = game_size
        self.margin = margin
        self.wall_to_wall_gap = wall_to_wall_gap
        self.board.current_player_turn = self.board.p1
        self.ai_move_pending = False

        self.hovered_pos = None
        self.first_wall_part = None

        self.game_surface_side = min(self.screen_height, self.screen_width) * 0.85
        self.game_x_pos = (self.screen_width - self.game_surface_side) / 2
        self.game_y_pos = min(self.screen_height, self.screen_width) * 0.025

        self.cell_side = round(
            (self.game_surface_side - ((game_size + 1) * self.margin)) / self.game_size
        )
        self.player_radius = round(self.cell_side * 0.4)

        self.board_background_color = board_background_color
        self.board_cell_color = board_cell_color
        self.background_color = background_color
        self.wall_color = wall_color
        self.screen = pygame.display.set_mode((self.screen_width, self.screen_height))
        self.font = pygame.font.SysFont("arial", 20)
        self.clock = pygame.time.Clock()
        self.running = True
        self.dt = 0

    def check_winning_condition(self):
        if (self.board.p1.pos[0] == self.board.p1.objective):
            self.running = False
            self.winner = "Player 1"
        if (self.board.p2.pos[0] == self.board.p2.objective):
            self.running = False
            self.winner = "AI" if self.board.againest_ai else "Player 1"

    def get_hovered_board_position(self, mouse_pos):
        x_offset = mouse_pos[0] - self.game_x_pos
        y_offset = mouse_pos[1] - self.game_y_pos

        if not (
            0 <= x_offset < self.game_surface_side
            and 0 <= y_offset < self.game_surface_side
        ):
            return None

        for y in range(len(self.board.board)):
            for x in range(len(self.board.board[y])):
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
            return False

        x, y = self.hovered_pos

        if self.first_wall_part is None:
            if self.board.board[y][x] == 0 and self.board.current_player_turn.available_walls > 0:
                self.board.board[y][x] = 1
                self.first_wall_part = (x, y)

        else:
            fx, fy = self.first_wall_part
            if (y, x) == (fy, fx):
                self.board.board[y][x] = 0
                self.first_wall_part = None
            elif self.is_valid_second_part(x, y, fx, fy):
                # Set second part
                self.board.board[y][x] = 1
                my = (fy + y) // 2
                mx = (fx + x) // 2
                self.board.board[my][mx] = (
                    HORIZONTAL_CONNECTOR_CODE if y == fy else VERTICAL_CONNECTOR_CODE
                )
                self.first_wall_part = None
                self.board.current_player_turn.available_walls -= 1

                return True

        return False

    def is_valid_second_part(self, x, y, fx, fy):
        if self.board.board[y][x] != 0:
            return False

        if fy % 2 == 1 and fx % 2 == 0:
            # Horizontal wall
            if y != fy or abs(x - fx) != 2:
                return False  # Must be 2 columns apart in same row
            my, mx = fy, (fx + x) // 2

            # Prevent crossing vertical wall (check above and below the midpoint)
            if (
                self.board.board[my - 1][mx] == 1
                and self.board.board[my][mx] == 2
                and self.board.board[my + 1][mx] == 1
            ):
                return False

        elif fy % 2 == 0 and fx % 2 == 1:
            # Vertical wall
            if x != fx or abs(y - fy) != 2:
                return False  # Must be 2 rows apart in same column
            my, mx = (fy + y) // 2, fx

            # Prevent crossing horizontal wall (check left and right of midpoint)
            if (
                self.board.board[my][mx - 1] == 1
                and self.board.board[my][mx] == 1
                and self.board.board[my][mx + 1] == 1
            ):
                return False
        else:
            return False

        new_board = self.board.board.copy()
        new_board[y][x] = 1

        return self.board.current_player_turn.WallRestrictionAlgorithmsBFS(new_board)

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

    def get_wall_properties(self, x, y):
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
        color = self.wall_color + "99"
        left, top, width, height = self.get_wall_properties(x, y)
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
        self.hovered_pos = None if (self.board.againest_ai and self.board.current_player_turn == self.board.p2) else self.get_hovered_board_position(mouse_pos)

        if self.ai_move_pending and self.board.current_player_turn == self.board.p2:
            self.board.p2.ai_move()
            self.check_winning_condition()
            self.board.current_player_turn = self.board.p1
            self.ai_move_pending = False

        for event in pygame.event.get():
            switch_play = False

            if event.type == pygame.QUIT:
                self.running = False

            elif not (self.board.againest_ai and self.board.current_player_turn == self.board.p2):
                if event.type == pygame.MOUSEBUTTONDOWN:
                    switch_play = self.handle_click()
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_DOWN:
                        switch_play = self.board.current_player_turn.handle_move("down")
                    elif event.key == pygame.K_UP:
                        switch_play = self.board.current_player_turn.handle_move("top")
                    elif event.key == pygame.K_LEFT:
                        switch_play = self.board.current_player_turn.handle_move("left")
                    elif event.key == pygame.K_RIGHT:
                        switch_play = self.board.current_player_turn.handle_move("right")
                    elif event.key == pygame.K_q:
                        switch_play = self.board.current_player_turn.handle_move("topLeft")
                    elif event.key == pygame.K_e:
                        switch_play = self.board.current_player_turn.handle_move("topRight")
                    elif event.key == pygame.K_z:
                        switch_play = self.board.current_player_turn.handle_move("bottomLeft")
                    elif event.key == pygame.K_c:
                        switch_play = self.board.current_player_turn.handle_move("bottomRight")

            if switch_play:
                self.check_winning_condition()
                if self.board.current_player_turn == self.board.p1:
                    self.board.current_player_turn = self.board.p2

                    # Defer AI move
                    if self.board.againest_ai:
                        self.ai_move_pending = True
                else:
                    self.board.current_player_turn = self.board.p1


    def draw_indicators(self):
        # Texts and colors
        p1_text_str = f"Player 1 walls: {self.board.p1.available_walls}"
        p2_text_str = f"Player 2 walls: {self.board.p2.available_walls}"
        is_p1_turn = self.board.current_player_turn == self.board.p1

        p1_text = self.font.render(p1_text_str, True, self.board.p1.color)  # Red
        p2_text = self.font.render(p2_text_str, True, self.board.p2.color)  # Green

        turn_text_str = "Player 1 turn" if is_p1_turn else "Player 2 turn"
        turn_color = self.board.p1.color if is_p1_turn else self.board.p2.color

        turn_text = self.font.render(turn_text_str, True, (0, 0, 0))
        turn_bg_rect = turn_text.get_rect()
        padding = 10
        turn_bg_rect.inflate_ip(padding * 2, padding)

        # Combined layout size
        spacing = 20
        total_width = (
            p1_text.get_width() + spacing +
            turn_bg_rect.width + spacing +
            p2_text.get_width()
        )
        y_pos = self.screen_height - 50  # Near bottom
        x_start = (self.screen_width - total_width) // 2

        # Blit Player 1
        self.screen.blit(p1_text, (x_start, y_pos))

        # Blit Turn Indicator Box
        turn_box_x = x_start + p1_text.get_width() + spacing
        turn_box_y = y_pos - (turn_bg_rect.height - turn_text.get_height()) // 2
        pygame.draw.rect(self.screen, turn_color, (turn_box_x, turn_box_y, turn_bg_rect.width, turn_bg_rect.height))
        pygame.draw.rect(self.screen, (0, 0, 0), (turn_box_x, turn_box_y, turn_bg_rect.width, turn_bg_rect.height), 2)  # border
        self.screen.blit(turn_text, (turn_box_x + padding, turn_box_y + padding // 2))

        # Blit Player 2
        p2_x = turn_box_x + turn_bg_rect.width + spacing
        self.screen.blit(p2_text, (p2_x, y_pos))

    def draw_board(self):
        self.screen.fill(self.background_color)
        surface = pygame.Surface((self.game_surface_side, self.game_surface_side))
        surface.fill(self.board_background_color)

        for y in range(len(self.board.board)):
            for x in range(len(self.board.board[y])):
                is_cell = y % 2 == 0 and x % 2 == 0
                is_horizontal_wall, is_vertical_wall = self.check_wall_type(x, y)
                is_connector = (
                    not (is_cell or is_vertical_wall or is_horizontal_wall)
                    and self.board.board[y][x] > 0
                )

                left, top = self.map_board_pos(x, y)
                width = self.cell_side
                height = self.cell_side

                if is_cell:
                    cell = pygame.Rect(left, top, width, height)
                    pygame.draw.rect(
                        surface,
                        pygame.Color(self.board_cell_color),
                        cell,
                        border_radius=round(self.cell_side * 0.1),
                    )

                if self.board.board[y][x] > 0 and is_cell:
                    player_pos = (
                        left + round(self.cell_side / 2),
                        top + round(self.cell_side / 2),
                    )
                    player_color = (
                        pygame.Color(self.board.p1.color)
                        if self.board.board[y][x] == self.board.p1.id
                        else pygame.Color(self.board.p2.color)
                    )

                    pygame.draw.circle(
                        surface, player_color, player_pos, self.player_radius
                    )
                elif (is_vertical_wall or is_horizontal_wall) and self.board.board[y][x] > 0:
                    left, top, width, height = self.get_wall_properties(x, y)
                    pygame.draw.rect(
                        surface,
                        pygame.Color(self.wall_color),
                        pygame.Rect(left, top, width, height),
                    )
                elif is_connector:
                    is_vertical_connector = self.board.board[y][x] == VERTICAL_CONNECTOR_CODE
                    is_horizontal_connector = (
                        self.board.board[y][x] == HORIZONTAL_CONNECTOR_CODE
                    )

                    left, top, width, height = self.get_wall_connector(
                        x, y, is_horizontal_connector, is_vertical_connector
                    )

                    connector = pygame.Rect(left, top, width, height)
                    pygame.draw.rect(surface, pygame.Color(self.wall_color), connector)

        if self.hovered_pos:
            x, y = self.hovered_pos

            if self.first_wall_part is None:
                if self.board.board[y][x] == 0:
                    self.draw_preview_wall(surface, x, y)
            else:
                fx, fy = self.first_wall_part
                if self.is_valid_second_part(x, y, fx, fy):
                    self.draw_preview_wall(surface, x, y)

        self.screen.blit(surface, (self.game_x_pos, self.game_y_pos))
        self.draw_indicators()
        pygame.display.flip()

    def show_result_screen(winner):
        screen = pygame.display.set_mode((400, 200))
        pygame.display.set_caption("Game Over")
        font = pygame.font.SysFont(None, 36)
        clock = pygame.time.Clock()

        message = f"{winner} Won!" if winner else "Draw!"
        text = font.render(message, True, (255, 255, 255))
        text_rect = text.get_rect(center=(200, 100))

        waiting = True
        start_time = time.time()

        while waiting:
            screen.fill((0, 0, 0))
            screen.blit(text, text_rect)

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                if event.type == pygame.KEYDOWN or event.type == pygame.MOUSEBUTTONDOWN:
                    waiting = False

            # Auto-exit after 3 seconds
            if time.time() - start_time > 3:
                waiting = False

            pygame.display.flip()
            clock.tick(60)

    def run(self):
        while self.running:
            self.handle_events()
            self.draw_board()
            self.dt = self.clock.tick(60) / 1000

        return self.winner


class Menu:
    def __init__(self):
        pygame.init()
        self.screen = pygame.display.set_mode((400, 200))
        pygame.display.set_caption("Select Game Mode")
        self.clock = pygame.time.Clock()
        self.running = True
        self.selected_ai_mode = None  # Will be set to True or False

        self.buttons = {
            "vs_ai": pygame.Rect(50, 70, 130, 50),
            "vs_human": pygame.Rect(220, 70, 130, 50),
        }

    def draw_buttons(self):
        font = pygame.font.SysFont(None, 24)

        def draw_button(rect, label):
            pygame.draw.rect(self.screen, (70, 130, 180), rect)
            text = font.render(label, True, (255, 255, 255))
            text_rect = text.get_rect(center=rect.center)
            self.screen.blit(text, text_rect)

        draw_button(self.buttons["vs_ai"], "VS AI")
        draw_button(self.buttons["vs_human"], "VS Human")

    def run(self):
        while self.running:
            self.screen.fill((30, 30, 30))
            self.draw_buttons()

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.running = False
                    pygame.quit()
                    sys.exit()
                if event.type == pygame.MOUSEBUTTONDOWN:
                    pos = event.pos
                    if self.buttons["vs_ai"].collidepoint(pos):
                        self.selected_ai_mode = True
                        self.running = False
                    elif self.buttons["vs_human"].collidepoint(pos):
                        self.selected_ai_mode = False
                        self.running = False

            pygame.display.flip()
            self.clock.tick(60)

        return self.selected_ai_mode

if __name__ == "__main__":
    while True:
        menu = Menu()
        against_ai = menu.run()

        game = GameGUI(againest_ai=against_ai)
        result = game.run()

        GameGUI.show_result_screen(result)

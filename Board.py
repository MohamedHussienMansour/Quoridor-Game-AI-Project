import numpy as np
from Player import Player


class Board:
    HORIZONTAL_CONNECTOR_CODE = 1
    VERTICAL_CONNECTOR_CODE = 2

    def __init__(self, dim=9):
        self.dimPawnBoard = dim
        self.dimWallBoard = self.dimPawnBoard - 1
        self.dimBoard = self.dimPawnBoard + self.dimWallBoard
        self.board = np.zeros((self.dimBoard, self.dimBoard))
        self.p1 = Player(board=self, pos=[16, 8], objective=0)
        self.p2 = Player(board=self, pos=[0, 8], objective=self.dimBoard-1)

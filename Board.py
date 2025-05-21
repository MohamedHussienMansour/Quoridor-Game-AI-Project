import numpy as np
from Player import Player
from AIPlayer import AIPlayer
import json


class Board:
    def __init__(self, dim=9, againest_ai=False):
        self.dimPawnBoard = dim
        self.dimWallBoard = self.dimPawnBoard - 1
        self.dimBoard = self.dimPawnBoard + self.dimWallBoard

        self.board = np.zeros((self.dimBoard, self.dimBoard))
        self.againest_ai = againest_ai

        self.p1 = Player(1, self, pos=np.array([16, 8]), objective=0)

        if self.againest_ai:
            self.p2 = AIPlayer(2, self, pos=np.array([0, 8]), objective=self.dimBoard - 1)
        else:
            self.p2 = Player(2, self, pos=np.array([0, 8]), objective=self.dimBoard - 1)

    def get_state(self):
        return [
                [self.p1.pos.copy(), self.p1.available_walls],
                [self.p2.pos.copy(), self.p2.available_walls],
                self.board.copy()
            ]

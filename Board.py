import numpy as np
class Board:


    def __init__(self,no_players = 2,dim=9):
        
        self.dimPawnBoard=dim
        self.dimWallBoard=self.dimPawnBoard-1
        self.dimBoard=self.dimPawnBoard+self.dimWallBoard
        self.board=np.zeros((self.dimBoard,self.dimBoard))
        self.no_players = no_players
        self.codesPlayers=range(1,no_players+1)
        
        


if __name__=="__main__":
    b=Board()
    print(b.board)
        





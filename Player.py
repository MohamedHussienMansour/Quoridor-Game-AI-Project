from Board import Board
from collections import deque
import math
import copy
class Player:
    players=[]
    positions=[]
    objectives=[]
    board=Board()
    pid=0
    def __init__(self,pos,objective,no_wall=10):
        self.objective=objective
        Player.objectives.append(objective)
        Player.pid+=1
        self.id=Player.pid
        Player.players.append(Player.pid)
        self.pos=pos
        Player.positions.append(self.pos)
        self.no_wall = no_wall
        Player.board.board[pos[0],[pos[1]]]=self.id
        
    def move(self,direction):
        # up
        row, column = self.pos
        if (not self.rule(direction,self.pos)):
            print("Invalid Move")
            return 



        if(direction=="up"):
            self.pos[0]-=2
            Player.board.board[self.pos[0], self.pos[1]]=self.id
        elif(direction=="down"):
            self.pos[0]+=2
            Player.board.board[self.pos[0], self.pos[1]]=self.id
        elif(direction=="right"):
            self.pos[1]+=2
            Player.board.board[self.pos[0], self.pos[1]]=self.id
        elif(direction=="left"):
            self.pos[1]-=2
            Player.board.board[self.pos[0], self.pos[1]]=self.id
        elif(direction=="topLeft"):
            Player.board.board[self.pos[0], self.pos[1]]=0
            self.pos[0]-=2
            self.pos[1]-=2
            Player.board.board[self.pos[0], self.pos[1]]=self.id
        elif(direction=="topRight"):
            Player.board.board[self.pos[0], self.pos[1]]=0
            self.pos[0]-=2
            self.pos[1]+=2
            Player.board.board[self.pos[0], self.pos[1]]=self.id
        elif(direction=="downRight"):
            Player.board.board[self.pos[0], self.pos[1]]=0
            self.pos[0]-=2
            self.pos[1]+=2
            Player.board.board[self.pos[0], self.pos[1]]=self.id
        elif(direction=="downleft"):
            Player.board.board[self.pos[0], self.pos[1]]=0
            self.pos[0]-=2
            self.pos[1]+=2
            Player.board.board[self.pos[0], self.pos[1]]=self.id
        else:
            print("Invalid Move")
            return
        Player.positions[self.id-1]=[self.pos[0],self.pos[1]]

        
    def rule(self,direction,pos):

        if(direction=="up"):
            if(pos[0]-2<0): #player out of Board
                return False
            if(Player.board.board[pos[0]-1,pos[1]]!=0): # there is wall restricted move
                return False
            if(Player.board.board[pos[0]-2,pos[1]]!=0): #there is player front of me
                if(pos[0]-4<0): #player out of Board with respect there is player front of me
                    return False
                if(Player.board.board[pos[0]-3,pos[1]]!=0): # there is no wall restricted  to jump double
                    return False
                Player.board.board[self.pos[0], self.pos[1]]=0
                pos[0]-=2
                return True
            Player.board.board[self.pos[0], self.pos[1]]=0
            return True
        
        elif(direction=="down"):
            if(pos[0]+2>16): #player out of Board
                return False
            if(Player.board.board[pos[0]+1,pos[1]]!=0): # there is wall restricted move
                return False
            if(Player.board.board[pos[0]+2,pos[1]]!=0): #there is player front of me
                if(pos[0]+4>16): #player out of Board with respect there is player front of me
                    return False
                if(Player.board.board[pos[0]+3,pos[1]]!=0):
                    return False
                Player.board.board[self.pos[0], self.pos[1]]=0
                pos[0]+=2
                return True
              
            Player.board.board[self.pos[0], self.pos[1]]=0
            return True
        
        elif(direction=="right"):
            if(pos[1]+2>16): #player out of Board
                return False
            if(Player.board.board[pos[0],pos[1]+1]!=0): # there is wall restricted move
                return False
            if(Player.board.board[pos[0],pos[1]+2]!=0): #there is player front of me
                if(pos[1]+4>16): #player out of Board with respect there is player front of me
                    return False
                if(Player.board.board[pos[0],pos[1]+3]!=0):
                    return False
                Player.board.board[self.pos[0], self.pos[1]]=0
                pos[1]+=2
                return True
            Player.board.board[self.pos[0], self.pos[1]]=0
            return True
        
        elif(direction=="left"):
            if(pos[1]-2<0): #player out of Board
                return False
            if(Player.board.board[pos[0],pos[1]-1]!=0): # there is wall restricted move
                return False
            if(Player.board.board[pos[0],pos[1]-2]!=0): #there is player front of me
                if(pos[1]-4<0): #player out of Board with respect there is player front of me
                    return False
                if(Player.board.board[pos[0],pos[1]-3]!=0):
                    return False
                Player.board.board[self.pos[0], self.pos[1]]=0
                pos[1]-=2
                return True
            Player.board.board[self.pos[0], self.pos[1]]=0
            return True
        
        elif(direction=="topLeft"):
            if(Player.board.board[pos[0]-2,pos[1]]!=0 or 
               Player.board.board[pos[0],pos[1]-2]!=0):
                if(Player.board.board[pos[0]-2,pos[1]]!=0): #there is player front of me
                    if(pos[0]-4<0): #player out of Board with respect there is player front of me
                        return False
                    if(Player.board.board[pos[0]-3,pos[1]]==0): # there must be wall
                        return False
                    if(pos[1]-2<0 or pos[0] -2<0): #player out of Board
                        return False
                    if(Player.board.board[pos[0]-2,pos[1]-1]!=0 ): # there is wall restricted move
                        return False
                
                if(Player.board.board[pos[0],pos[1]-2]!=0): #there is player front of me
                    if(pos[1]-4<0): #player out of Board with respect there is player front of me
                        return False
                    if(Player.board.board[pos[0],pos[1]-3]==0):
                        return False
                    if(pos[1]-2<0 or pos[0] -2<0): #player out of Board
                        return False
                    if(Player.board.board[pos[0]-1,pos[1]-2]!=0 ): # there is wall restricted move
                        return False
                return True
            else:
                return False
        elif(direction=="topRight"):
            if((Player.board.board[pos[0]-2,pos[1]]!=0 or 
               Player.board.board[pos[0],pos[1]+2]!=0) and
               pos[1]+2>16 or pos[0] -2<0):
                if(Player.board.board[pos[0]-2,pos[1]]!=0): #there is player front of me
                    if(pos[0]-4<0): #player out of Board with respect there is player front of me
                        return False
                    if(Player.board.board[pos[0]-3,pos[1]]==0): # there must be wall
                        return False
                    if(Player.board.board[pos[0]-2,pos[1]+1]!=0 ): # there is wall restricted move
                        return False
                
                if(Player.board.board[pos[0],pos[1]+2]!=0): #there is player right of me
                    if(pos[1]+4>16): #player out of Board with respect there is player front of me
                        return False
                    if(Player.board.board[pos[0],pos[1]+3]==0):
                        return False
                    if(Player.board.board[pos[0]-1,pos[1]+2]!=0 ): # there is wall restricted move
                        return False
                return True
            else:
                return False

        elif(direction=="downRight"):
            if((Player.board.board[pos[0]+2,pos[1]]!=0 or 
               Player.board.board[pos[0],pos[1]+2]!=0) and
              not (pos[1]+2>16 or pos[0] +2>16)):
                if(Player.board.board[pos[0]+2,pos[1]]!=0): #there is player front of me
                    if(pos[0]+4>16): #player out of Board with respect there is player front of me
                        return False
                    if(Player.board.board[pos[0]+3,pos[1]]==0): # there must be wall
                        return False
                    if(Player.board.board[pos[0]+2,pos[1]+1]!=0 ): # there is wall restricted move
                        return False
                
                if(Player.board.board[pos[0],pos[1]+2]!=0): #there is player right of me
                    if(pos[1]+4>16): #player out of Board with respect there is player front of me
                        return False
                    if(Player.board.board[pos[0],pos[1]+3]==0):
                        return False
                    if(Player.board.board[pos[0]+1,pos[1]+2]!=0 ): # there is wall restricted move
                        return False
                return True
            else:
                return False
        elif(direction=="downLeft"):
            if((Player.board.board[pos[0]+2,pos[1]]!=0 or 
               Player.board.board[pos[0],pos[1]-2]!=0) and
               (pos[1]+2<16 or pos[0]-2>0)):
                if(Player.board.board[pos[0]+2,pos[1]]!=0): #there is player front of me
                    if(pos[0]+4>16): #player out of Board with respect there is player front of me
                        return False
                    if(Player.board.board[pos[0]+3,pos[1]]==0): # there must be wall
                        return False
                    if(Player.board.board[pos[0]+2,pos[1]+1]!=0 ): # there is wall restricted move
                        return False
                
                if(Player.board.board[pos[0],pos[1]-2]!=0): #there is player right of me
                    if(pos[1]-4<0): #player out of Board with respect there is player front of me
                        return False
                    if(Player.board.board[pos[0],pos[1]-3]==0):
                        return False
                    if(Player.board.board[pos[0]+1,pos[1]-2]!=0 ): # there is wall restricted move
                        return False
                return True
            else:
                return False
            
        
        



    def walls(self,X1,Y1,X2,Y2):
        meanX=0;meanY=0
        if ((X1+Y1)%2==0 or (X2+Y2)%2==0):
            print("invalid ")
            return False
        if (X1%2 != 0): #first one is odd
            if(abs(X1-X2) == 2 and Y1==Y2): # check diff  == 2 
                X1-=1;Y1-=1;X2-=1;Y2-=1;meanX=(X1+X2)//2;meanY=Y1
                if(Player.board.board[X1,Y1]==0 and
                    Player.board.board[X2,Y2]==0 and
                    Player.board.board[meanX,Y2]==0):
                    Player.board.board[meanX][meanY]=-1
                else:
                    print("invalid ")
                    return False
            else:
                print("invalid ")
                return False
        elif(Y1%2 != 0):
            if(abs(Y1-Y2) == 2 and X1==X2): # check diff  == 2 
                X1-=1;Y1-=1;X2-=1;Y2-=1;meanY=(Y1+Y2)//2;meanX=X1
                if(Player.board.board[X1,Y1]==0 and
                    Player.board.board[X2,Y2]==0 and
                    Player.board.board[X1,meanY]==0):
                    Player.board.board[meanX,meanY]=-1
                else:
                    print("invalid ")
                    return False
            else:
                print("invalid ")
                return False
        else:
            
            print("invalid ")
            return False
        Player.board.board[meanX,meanY]=-1
        Player.board.board[X1,Y1]=-1
        Player.board.board[X2,Y2]=-1
  

    def WallRestrictionAlgorithmsBFS(self):
        directions = [(-2, 0), (2, 0), (0, -2), (0, 2)]  # up, down, left, right
        wall_offsets = [(-1, 0), (1, 0), (0, -1), (0, 1)]  # walls are between tiles

        for i in range(1, Player.pid + 1):


            start_y, start_x = Player.positions[i - 1]
            visited = set()
            queue = deque([(start_y, start_x)])
            visited.add((start_y, start_x))

            # Determine the goal row based on the player's objective
            goal_row = Player.objectives[i-1]

            while queue:
                y, x = queue.popleft()

                if y == goal_row:
                    return True  # Found path to the goal row

                for (dy, dx), (wy, wx) in zip(directions, wall_offsets):
                    ny, nx = y + dy, x + dx
                    wy, wx = y + dy // 2, x + dx // 2

                    # Check bounds
                    if 0 <= ny < Player.board.dimBoard and 0 <= nx < Player.board.dimBoard:
                        # Check for wall between current and new position
                        if Player.board.board[wy, wx] == 0 and Player.board.board[ny, nx] == 0:
                            if (ny, nx) not in visited:
                                visited.add((ny, nx))
                                queue.append((ny, nx))

            # If the queue empties without reaching the goal row
            return False

        return True
   

if __name__=="__main__":
    p1 = Player(pos=[16,8], objective=0)  # Human player
    p2 = Player(pos=[0,8], objective=16)  # AI player with search depth 3

    moves =int(input("Give me number of Moves: "))
    print(p1.board.board)
    
    while(moves!=0):

            if(i%2==0):
                M_W = input("Move or Wall:enter M or W: ")
                if(M_W == 'M'):
                    direction=input("Give me Next move of player: ")
                    print("the player ")
                    p1.move(direction)
                    print(p1.board.board)
                    print("the player position become ",p1.pos)
                elif (M_W =='W'):
                    X1 = int(input("Give me Next move X1 of wall: "))
                    Y1 = int(input("Give me Next move Y1 of wall: "))
                    X2 = int(input("Give me Next move X2 of wall: "))
                    Y2 = int(input("Give me Next move Y2 of wall: "))
                    p1.walls(X1,Y1,X2,Y2)
                    print(p1.board.board)
                    moves-=1

            else:
                M_W = input("Move or Wall:enter M or W: ")
                if(M_W == 'M'):
                    direction=input("Give me Next move of player: ")
                    print("the player ")
                    p2.move(direction)
                    print(p2.board.board)
                    print("the player position become ",p2.pos)
                elif (M_W =='W'):
                    X1 = int(input("Give me Next move X1 of wall: "))
                    Y1 = int(input("Give me Next move Y1 of wall: "))
                    X2 = int(input("Give me Next move X2 of wall: "))
                    Y2 = int(input("Give me Next move Y2 of wall: "))
                    p2.walls(X1,Y1,X2,Y2)
                    print(p2.board.board)
                    moves-=1
                

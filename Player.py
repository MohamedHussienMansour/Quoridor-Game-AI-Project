from Board import Board
class Player:
    def __init__(self,id,pos,objective,board,no_wall=10):
        self.objective=objective
        self.id=id
        self.pos=pos
        self.no_wall = no_wall
        self.board=board
        self.board.board[pos[0],[pos[1]]]=self.id
        
    def move(self,direction):
        # up
        row, column = self.pos
        if (not self.rule(direction,self.pos)):
            print("Invalid Move")
            return 



        if(direction=="up"):
            self.pos[0]-=2
            self.board.board[self.pos[0], self.pos[1]]=self.id
        elif(direction=="down"):
            self.pos[0]+=2
            self.board.board[self.pos[0], self.pos[1]]=self.id
        elif(direction=="right"):
            self.pos[1]+=2
            self.board.board[self.pos[0], self.pos[1]]=self.id
        elif(direction=="left"):
            self.pos[1]-=2
            self.board.board[self.pos[0], self.pos[1]]=self.id
        elif(direction=="topLeft"):
            self.board.board[self.pos[0], self.pos[1]]=0
            self.pos[0]-=2
            self.pos[1]-=2
            self.board.board[self.pos[0], self.pos[1]]=self.id
        elif(direction=="topRight"):
            self.board.board[self.pos[0], self.pos[1]]=0
            self.pos[0]-=2
            self.pos[1]+=2
            self.board.board[self.pos[0], self.pos[1]]=self.id
        elif(direction=="downRight"):
            self.board.board[self.pos[0], self.pos[1]]=0
            self.pos[0]-=2
            self.pos[1]+=2
            self.board.board[self.pos[0], self.pos[1]]=self.id
        elif(direction=="downleft"):
            self.board.board[self.pos[0], self.pos[1]]=0
            self.pos[0]-=2
            self.pos[1]+=2
            self.board.board[self.pos[0], self.pos[1]]=self.id
        else:
            print("Invalid Move")

            

        
    def rule(self,direction,pos):

        if(direction=="up"):
            if(pos[0]-2<0): #player out of Board
                return False
            if(self.board.board[pos[0]-1,pos[1]]!=0): # there is wall restricted move
                return False
            if(self.board.board[pos[0]-2,pos[1]]!=0): #there is player front of me
                if(pos[0]-4<0): #player out of Board with respect there is player front of me
                    return False
                if(self.board.board[pos[0]-3,pos[1]]!=0): # there is no wall restricted  to jump double
                    return False
                self.board.board[self.pos[0], self.pos[1]]=0
                pos[0]-=2
                return True
            self.board.board[self.pos[0], self.pos[1]]=0
            return True
        
        elif(direction=="down"):
            if(pos[0]+2>16): #player out of Board
                return False
            if(self.board.board[pos[0]+1,pos[1]]!=0): # there is wall restricted move
                return False
            if(self.board.board[pos[0]+2,pos[1]]!=0): #there is player front of me
                if(pos[0]+4>16): #player out of Board with respect there is player front of me
                    return False
                if(self.board.board[pos[0]+3,pos[1]]!=0):
                    return False
                self.board.board[self.pos[0], self.pos[1]]=0
                pos[0]+=2
                return True
              
            self.board.board[self.pos[0], self.pos[1]]=0
            return True
        
        elif(direction=="right"):
            if(pos[1]+2>16): #player out of Board
                return False
            if(self.board.board[pos[0],pos[1]+1]!=0): # there is wall restricted move
                return False
            if(self.board.board[pos[0],pos[1]+2]!=0): #there is player front of me
                if(pos[1]+4>16): #player out of Board with respect there is player front of me
                    return False
                if(self.board.board[pos[0],pos[1]+3]!=0):
                    return False
                self.board.board[self.pos[0], self.pos[1]]=0
                pos[1]+=2
                return True
            self.board.board[self.pos[0], self.pos[1]]=0
            return True
        
        elif(direction=="left"):
            if(pos[1]-2<0): #player out of Board
                return False
            if(self.board.board[pos[0],pos[1]-1]!=0): # there is wall restricted move
                return False
            if(self.board.board[pos[0],pos[1]-2]!=0): #there is player front of me
                if(pos[1]-4<0): #player out of Board with respect there is player front of me
                    return False
                if(self.board.board[pos[0],pos[1]-3]!=0):
                    return False
                self.board.board[self.pos[0], self.pos[1]]=0
                pos[1]-=2
                return True
            self.board.board[self.pos[0], self.pos[1]]=0
            return True
        
        elif(direction=="topLeft"):
            if(self.board.board[pos[0]-2,pos[1]]!=0 or 
               self.board.board[pos[0],pos[1]-2]!=0):
                if(self.board.board[pos[0]-2,pos[1]]!=0): #there is player front of me
                    if(pos[0]-4<0): #player out of Board with respect there is player front of me
                        return False
                    if(self.board.board[pos[0]-3,pos[1]]==0): # there must be wall
                        return False
                    if(pos[1]-2<0 or pos[0] -2<0): #player out of Board
                        return False
                    if(self.board.board[pos[0]-2,pos[1]-1]!=0 ): # there is wall restricted move
                        return False
                
                if(self.board.board[pos[0],pos[1]-2]!=0): #there is player front of me
                    if(pos[1]-4<0): #player out of Board with respect there is player front of me
                        return False
                    if(self.board.board[pos[0],pos[1]-3]==0):
                        return False
                    if(pos[1]-2<0 or pos[0] -2<0): #player out of Board
                        return False
                    if(self.board.board[pos[0]-1,pos[1]-2]!=0 ): # there is wall restricted move
                        return False
                return True
            else:
                return False
        elif(direction=="topRight"):
            if((self.board.board[pos[0]-2,pos[1]]!=0 or 
               self.board.board[pos[0],pos[1]+2]!=0) and
               pos[1]+2>16 or pos[0] -2<0):
                if(self.board.board[pos[0]-2,pos[1]]!=0): #there is player front of me
                    if(pos[0]-4<0): #player out of Board with respect there is player front of me
                        return False
                    if(self.board.board[pos[0]-3,pos[1]]==0): # there must be wall
                        return False
                    if(self.board.board[pos[0]-2,pos[1]+1]!=0 ): # there is wall restricted move
                        return False
                
                if(self.board.board[pos[0],pos[1]+2]!=0): #there is player right of me
                    if(pos[1]+4>16): #player out of Board with respect there is player front of me
                        return False
                    if(self.board.board[pos[0],pos[1]+3]==0):
                        return False
                    if(self.board.board[pos[0]-1,pos[1]+2]!=0 ): # there is wall restricted move
                        return False
                return True
            else:
                return False

        elif(direction=="downRight"):
            if((self.board.board[pos[0]+2,pos[1]]!=0 or 
               self.board.board[pos[0],pos[1]+2]!=0) and
               (pos[1]+2>16 or pos[0] +2>16)):
                if(self.board.board[pos[0]+2,pos[1]]!=0): #there is player front of me
                    if(pos[0]+4>16): #player out of Board with respect there is player front of me
                        return False
                    if(self.board.board[pos[0]+3,pos[1]]==0): # there must be wall
                        return False
                    if(self.board.board[pos[0]+2,pos[1]+1]!=0 ): # there is wall restricted move
                        return False
                
                if(self.board.board[pos[0],pos[1]+2]!=0): #there is player right of me
                    if(pos[1]+4>16): #player out of Board with respect there is player front of me
                        return False
                    if(self.board.board[pos[0],pos[1]+3]==0):
                        return False
                    if(self.board.board[pos[0]+1,pos[1]+2]!=0 ): # there is wall restricted move
                        return False
                return True
            else:
                return False
        elif(direction=="downLeft"):
            if((self.board.board[pos[0]+2,pos[1]]!=0 or 
               self.board.board[pos[0],pos[1]-2]!=0) and
               (pos[1]+2>16 or pos[0]-2>16)):
                if(self.board.board[pos[0]+2,pos[1]]!=0): #there is player front of me
                    if(pos[0]+4>16): #player out of Board with respect there is player front of me
                        return False
                    if(self.board.board[pos[0]+3,pos[1]]==0): # there must be wall
                        return False
                    if(self.board.board[pos[0]+2,pos[1]+1]!=0 ): # there is wall restricted move
                        return False
                
                if(self.board.board[pos[0],pos[1]-2]!=0): #there is player right of me
                    if(pos[1]-4<0): #player out of Board with respect there is player front of me
                        return False
                    if(self.board.board[pos[0],pos[1]-3]==0):
                        return False
                    if(self.board.board[pos[0]+1,pos[1]-2]!=0 ): # there is wall restricted move
                        return False
                return True
            else:
                return False
            
        
        



    def walls(self,X1,Y1,X2,Y2):
        if ((X1+Y1)%2==0 or (X2+Y2)%2==0):
            print("invalid ")
            return False
        if (X1%2 != 0): #first one is odd
            if(abs(X1-X2) == 2 and Y1==Y2): # check diff  == 2 
                X1-=1;Y1-=1;X2-=1;Y2-=1;meanX=(X1+X2)//2
                if(self.board.board[X1,Y1]==0 and
                    self.board.board[X2,Y2]==0 and
                    self.board.board[meanX,Y2]==0):
                    self.board.board[meanX][Y1]=-1
                else:
                    print("invalid ")
                    return False
            else:
                print("invalid ")
                return False
        elif(Y1%2 != 0):
            if(abs(Y1-Y2) == 2 and X1==X2): # check diff  == 2 
                X1-=1;Y1-=1;X2-=1;Y2-=1;meanY=(Y1+Y2)//2
                if(self.board.board[X1,Y1]==0 and
                    self.board.board[X2,Y2]==0 and
                    self.board.board[X1,meanY]==0):
                    self.board.board[X1,meanY]=-1
                else:
                    print("invalid ")
                    return False
            else:
                print("invalid ")
                return False
        else:
            
            print("invalid ")
            return False
        self.board.board[X1,Y1]=-1
        self.board.board[X2,Y2]=-1
        


        
                

                






        
    

if __name__=="__main__":
    board=Board()
    p1=Player(id=1,pos=[8,8],objective=16,board=board)
    p2=Player(id=2,pos=[6,8],objective=16,board=board)
    moves =int(input("Give me number of Moves: "))
    print(p1.board.board)
    for i in range(moves):
        M_W = input("Move or Wall:enter M or W: ")
        if(M_W == 'M'):
            direction=input("Give me Next move of player: ")
            if(i%2==0):
                print("the player ")
                p1.move(direction)
                print(p1.board.board)
                print("the player position become ",p1.pos)
            else:
                            
                p2.move(direction)
                print(p2.board.board)
                print("the player position become ",p2.pos)

        elif (M_W =='W'):

            X1 = int(input("Give me Next move X1 of wall: "))
            Y1 = int(input("Give me Next move Y1 of wall: "))
            X2 = int(input("Give me Next move X2 of wall: "))
            Y2 = int(input("Give me Next move Y2 of wall: "))
            p1.walls(X1,Y1,X2,Y2)
            print(p1.board.board)
           
            
            


        

    


    
        

            

            




        
    

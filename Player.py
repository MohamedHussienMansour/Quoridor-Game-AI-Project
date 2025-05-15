from Board import Board
class Player:
    players=[]
    positions=[]
    board=Board()
    pid=0
    def __init__(self,pos,objective,no_wall=10):
        self.objective=objective
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
    def WallRestrictionAlgorithms(self):
        
        for i in range(1,Player.pid+1):
            if (i==self.id):
                continue
            stackofStates=[]
            TraveledState=[]
            posY,posX=Player.positions[i-1]
            if(self.id==1):
                direction=1
                endY=17
            else:
                direction=-1
                endY=-1
            posY+=direction
            start=False
            if (Player.board.board[posX,posY]!=0):
                start=True
            
            
            while(start or posY+1!=self.objective):
                start=False
                
                while(Player.board.board[posY,posX]==0 and posY!=endY and (posX,posY) not in TraveledState):
                    posY+=direction*2
                if (posY==endY):
                    return True
                
                rightleftChance=2
                savedX=posX
                thereIsChance=False
                
                for Xchange,end in [-1,-1],[1,17]:
                    posX=savedX
                    while(posX+Xchange!=end and Player.board.board[posY-direction,posX+Xchange]==0):
                        posX+=Xchange*2
                        if(Player.board.board[posY,posX]==0):
                             if((posX,posY) not in TraveledState):
                                stackofStates.append((posX,posY))
                                TraveledState.append((posX,posY))
                                thereIsChance=True
                    if(posX+Xchange==end and not thereIsChance):
                        rightleftChance-=1     
                    elif(posX+Xchange!=end and Player.board.board[posY-direction,posX+Xchange]!=0):
                        if((posX,posY-direction*2) not in TraveledState):
                            stackofStates.append((posX,posY-direction*2))
                            TraveledState.append((posX,posY-direction*2))
                        
                
                if(rightleftChance==0):
                    # Player.board.board[meanX,meanY]=0
                    # Player.board.board[X1,Y1]=0
                    # Player.board.board[X2,Y2]=0        
                    return False
                posX,posY=stackofStates[0]
                stackofStates.pop(0)
        return True
                

                    
        #             while(Player.board.board[posX,posY]!=0 and Player.board.board[posX+1,posY-1]==0 and posX<16):
        #                 posX-=2
        #         elif(Player.board.board[posX+1,posY-1]!=0):
        #             stackofStates.append((posX,posY-2))
        #             posX=stackofStates[0][0]
                    
        #             while(Player.board.board[posX,posY]!=0 and Player.board.board[posX-1,posY-1]==0 and posX>0):
        #                 posX-=2
        #             if(posX<1):
        #                 print("invalid ")
        #                 return False
        #             elif(Player.board.board[posX-1,posY-1]==0):
        #                 stackofStates.append((posX,posY-2))
        #                 stackofStates.pop(0)
        #                 direction=-direction

        #     stackofStates.append((posX,posY-direction))





            


        


        
                

                






        
    

if __name__=="__main__":
    p1=Player(pos=[8,8],objective=0)
    p2=Player(pos=[0,0],objective=16)
    p1.board.board[5]=[-1,-1,-1,0,-1,-1,-1,0,-1,-1,-1,0,-1,-1,-1,0,0]


    moves =int(input("Give me number of Moves: "))
    print(p1.board.board)
    for i in range(moves):
        # if(i%2==0):
        #     print("the first player who play Now (1)")
        # else:
        #     print("the Second Player who play Now (2)")
        
        M_W = input("Move or Wall:enter M or W: ")
        if(M_W == 'M'):

            direction=input("Give me Next move of player: ")
            # if(i%2==0):
                
            print("the player ")
            p1.move(direction)
            print(p1.board.board)
            print("the player position become ",p1.pos)
            # else:
                            
            #     p2.move(direction)
            #     print(p2.board.board)
            #     print("the player position become ",p2.pos)

        elif (M_W =='W'):

            X1 = int(input("Give me Next move X1 of wall: "))
            Y1 = int(input("Give me Next move Y1 of wall: "))
            X2 = int(input("Give me Next move X2 of wall: "))
            Y2 = int(input("Give me Next move Y2 of wall: "))
            p1.walls(X1,Y1,X2,Y2)
            print(p1.board.board)


                
                
        check=int(input("Do you want to chech whether the wall placement valid or not "))
        if(check==1):
            print("is the wall valid or Not: ",p2.WallRestrictionAlgorithms())
            
           
            
            


        

    


    
        

            

            




        
    

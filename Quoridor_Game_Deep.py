# ۱
import tkinter as tk
from tkinter import messagebox  

import math
import time
import copy
import random
from collections import deque

Quoridor = tk.Tk()
Quoridor.geometry('560x620+300+0')
Quoridor.title("Quoridor Game")
Quoridor.resizable(width=False, height=False)



Square = dict()
for i in range(9) :
    for j in range(9) :
        Square[f'sq{i}{j}'] = tk.Button(Quoridor , bg = "white" , bd = 0)
        Square[f'sq{i}{j}'].place(height = 50 , width = 50 , y = (i+1)*10 + 50*i + 5 , x = (j+1) * 10 + j*50 + 5)
        Square[f'sq{i}{j}'].config(command = lambda arg = Square[f'sq{i}{j}'] , y = i , x = j : move(arg,y,x))



Horizental_wall = dict()
for i in range(10):
    for j in range(9) :
        if i == 0 or i == 9 :
            Horizental_wall[f'wall{i}{j}'] = tk.Button(Quoridor , background = "gray" , bd = 0)
            Horizental_wall[f'wall{i}{j}'].place(height = 10 , width = 60 , x = j * 50 +(j+1)*10 + 5, y = i*50 + i * 10 +5)
        else :
            Horizental_wall[f'wall{i}{j}'] = tk.Button(Quoridor , background = "#aee2ff" , bd= 0)
        
            Horizental_wall[f'wall{i}{j}'].place(height = 10 , width = 50 , x = j * 50 +(j+1)*10 + 5, y = i*50 + i * 10 +5)
        Horizental_wall[f'id{i}{j}'] = -1
Horizental_wall[f'wall00'].place(height = 10 , width = 70 , x = 5, y = 5)




Vertical_wall = dict()
for i in range(9) :
    for j in range(10) :
        if j == 0 or j == 9 :
            Vertical_wall[f'wall{i}{j}'] = tk.Button(Quoridor , background = "gray" , bd = 0)
            Vertical_wall[f'wall{i}{j}'].place(height = 60 , width = 10 , x = j * 50 + (j)*10 + 5, y = i*50+(i+1)*10 + 5)
        else :
            Vertical_wall[f'wall{i}{j}'] = tk.Button(Quoridor , background = "#aee2ff" , bd =0)
        
        
            Vertical_wall[f'wall{i}{j}'].place(height = 50 , width = 10 , x = j * 50 + (j)*10 + 5, y = i*50+(i+1)*10 + 5)
        Vertical_wall[f'id{i}{j}'] = -1
        
        



for i in range(10) :
    for j in range(9) :
        if j < 8 :
            Horizental_wall[f'wall{i}{j}'].config(command = lambda arg1 = Horizental_wall[f'wall{i}{j}'] , arg2 = Horizental_wall[f'wall{i}{j+1}'] , x = j , y = i , typew = 'h' : creat_wall(arg1,arg2,x,y,typew))   
for i in range(9) :
    for j in range(10) :
        if i < 8 :
            Vertical_wall[f'wall{i}{j}'].config(command = lambda arg1 = Vertical_wall[f'wall{i}{j}'] , arg2 = Vertical_wall[f'wall{i+1}{j}'] , x = j , y = i , typew = 'v': creat_wall(arg1,arg2,x,y,typew))



class Maze :
    X = 9
    Y = 9
    step = 0
    number_of_p1_wall = 10
    xplayer1 = 4
    yplayer1 = 0
    block = list()
    for i in range(9) :
        block.append([])
        for j in range(9) :
            block[i].append({
                'u' : False ,
                'r' : False ,
                'l' : False ,
                'd' : False ,
                'v' : -1
            })
    number_of_p2_wall = 10
    xplayer2 = 4
    yplayer2 = 8

player1 = tk.Button(Quoridor , bg = "#ff4d4d" ,borderwidth=3, relief="ridge")
player2 = tk.Button(Quoridor , bg = "#00ff80" ,borderwidth=3, relief="ridge" )
player1.place(height = 40 , width = 40 , x = 260 , y = 20)
player2.place(height = 40 , width = 40, x = 260 , y = 500 )
player1.config(command = lambda arg = player1 , p = 1 : set_yellow_squarGoal(arg , p))
player2.config(command = lambda arg = player2 , p = 2 : set_yellow_squarGoal(arg , p))

lbl_nwallp1 = tk.Label(Quoridor , bg = "white" , text = "Player1 Walls : 10" , font = ("Aria" ,9 , 'bold') , fg = 'red')
lbl_nwallp1.place(height = 30 , width = 120 , x = 120 , y = 570 , )

lbl_nwallp2 = tk.Label(Quoridor , bg = "white" , text = "Player2 Walls : 10" , font = ("Aria" ,9 , 'bold') , fg = "green")
lbl_nwallp2.place(height = 30 , width = 120 , x = 320 , y = 570)

lbl_turns = tk.Label(Quoridor , text = "Red Turn" , bg = "red"  ,font = ("Helvetica" , 8 , "bold") ,borderwidth=2, relief="solid")
lbl_turns.place(height = 30 , width = 80 , x = 240 , y = 570)

def assign_wall_to_block() :
    for i in range(9) :
        for j in range(9) :
            Maze.block[i][j]['v'] = -1
            if Horizental_wall[f'wall{i}{j}']['bg'] != '#aee2ff'  : #light blue 
                Maze.block[i][j]['u'] = True 
            else :
                Maze.block[i][j]['u'] = False
            if Horizental_wall[f'wall{i+1}{j}']['bg'] != '#aee2ff' :
                Maze.block[i][j]['d'] = True
            else :
                Maze.block[i][j]['d'] = False
            if Vertical_wall[f'wall{i}{j}']['bg'] != '#aee2ff' :
                Maze.block[i][j]['l'] = True
            else :
                Maze.block[i][j]['l'] = False
            if Vertical_wall[f'wall{i}{j+1}']['bg'] != '#aee2ff' :
                Maze.block[i][j]['r'] = True
            else :
                Maze.block[i][j]['r'] = False
    #for i in range(9):
        #for j in range(9):
            #u , r , l , d , v = Maze.block[i][j]['u'] , Maze.block[i][j]['r'] , Maze.block[i][j]['l'] , Maze.block[i][j]['d'] , Maze.block[i][j]['v']
            #messagebox.showinfo(f'block info {i}{j}' , f'u : {u} , r : {r} , l : {l} , d : {d} , v : {v}')

def clear_square_color() :
    for i in range(9) :
        for j in range(9) :
            Square[f'sq{i}{j}']['bg'] = "white"
def reset_vblock() :
    for i in range(9) :
        for j in range(9) :
            Maze.block[i][j]['v'] = -1
def is_valid_wall(x , y , typew) :
    
    #return true or false
    assign_wall_to_block()
    if typew == 'h' :
        Maze.block[y][x]['u'] = True
        Maze.block[y][x+1]['u'] = True 
        Maze.block[y-1][x]['d'] = True
        Maze.block[y-1][x+1]['d'] = True 
    elif typew == 'v' :
        Maze.block[y][x]['l'] = True
        Maze.block[y+1][x]['l'] = True
        Maze.block[y][x-1]['r'] = True
        Maze.block[y+1][x-1]['r'] = True

    else :
        messagebox.showinfo("error - is_valid_wall()" , "typew is not h or v")
    
    ############################################## p1
    reset_vblock()
    validp1 = False
    Maze.block[Maze.yplayer1][Maze.xplayer1]['v'] = 0
    step = 0
    while True :
        f = False
        for i in range(9) :
            for j in range(9) :
                
                if Maze.block[i][j]['v'] == step :
                        #messagebox.showinfo("v" , f'{i} {j} : {step}')
                        if Maze.block[i][j]['u'] == False:
                            if Maze.block[i-1][j]['v'] == -1 :
                                #messagebox.showinfo("v" , f'u {i-1} {j} : {step + 1}')
                                Maze.block[i-1][j]['v'] = step + 1
                                f = True
                        if Maze.block[i][j]['r'] == False  :
                            if Maze.block[i][j+1]['v'] == -1 :
                                #messagebox.showinfo("v" , f'r {i} {j+1} : {step + 1}')
                                Maze.block[i][j+1]['v'] = step + 1
                                f = True
                        if Maze.block[i][j]['l'] == False :
                            if Maze.block[i][j-1]['v'] == -1 :
                                #messagebox.showinfo("v" , f'l {i} {j-1} : {step + 1}')
                                Maze.block[i][j-1]['v'] = step + 1
                                f = True
                        if Maze.block[i][j]['d'] == False :
                            if Maze.block[i+1][j]['v'] == -1 :
                                #messagebox.showinfo("v" , f' d {i+1} {j} : {step + 1}')
                                Maze.block[i+1][j]['v'] = step + 1
                                f = True
        step += 1
        if f == False :
            break
    for i in range(9) :
        #messagebox.showinfo(f'v block8{i}' , Maze.block[8][j]['v'])
        if Maze.block[8][i]['v'] != -1 :
            
            validp1 = True
            break
    #assign_wall_to_block()
    ########################################### p2 
    reset_vblock()
    validp2 = False
    Maze.block[Maze.yplayer2][Maze.xplayer2]['v'] = 0
    step = 0
    while True :
        f = False
        for i in range(9) :
            for j in range(9) :
                if Maze.block[i][j]['v'] == step :
                        if Maze.block[i][j]['u'] == False :
                            if Maze.block[i-1][j]['v'] == -1 :
                                Maze.block[i-1][j]['v'] = step + 1
                                f = True
                        if Maze.block[i][j]['r'] == False :
                            if Maze.block[i][j+1]['v'] == -1 :
                                Maze.block[i][j+1]['v'] = step + 1
                                f = True
                        if Maze.block[i][j]['l'] == False :
                            if Maze.block[i][j-1]['v'] == -1 :
                                Maze.block[i][j-1]['v'] = step + 1
                                f = True
                        if Maze.block[i][j]['d'] == False :
                            if Maze.block[i+1][j]['v'] == -1 :
                                Maze.block[i+1][j]['v'] = step + 1
                                f = True
        step += 1
        if f == False :
            break
    for i in range(9) :
        if Maze.block[0][i]['v'] != -1 :
            validp2 = True
            break
    #assign_wall_to_block()

    ######################### return
    if validp1 == False :
        messagebox.showinfo("wrong wall" , "Player1 will be surrounded")
    if validp2 == False :
        messagebox.showinfo("wrong wall" , "Player2 will be surrounded")
    if validp1 and validp2 :
        return True
    else :
        return False
    assign_wall_to_block()
    ######################### end is_valid_wall() 

def creat_wall(arg1 , arg2 , x , y , typew) :
    #messagebox.showinfo(" x , y" , f'{x}  {y}')
    if Maze.yplayer2 == 0 :
        messagebox.showinfo("End Game" , "Player2 Won")
    elif Maze.yplayer1 == 8 :
        messagebox.showinfo("End Game" , "Player1 Won") 
    else :
        if Maze.step % 2 == 0 :
            if arg1['bg'] == "#aee2ff" and arg2['bg'] == "#aee2ff" and Maze.number_of_p1_wall != 0 :
                clear_square_color()
                if is_valid_wall(x,y,typew) : 
                    
                    if typew == 'h' :
                        if Vertical_wall[f'id{y-1}{x+1}'] != Vertical_wall[f'id{y}{x+1}'] or Vertical_wall[f'id{y-1}{x+1}'] == -1 :
                            arg1['bg'] = "#e8002a" #red
                            arg2['bg'] = "#e8002a"
                            #Horizental_wall[f'wall{y}{x}'].lift()
                            #Horizental_wall[f'wall{y}{x+1}'].lift()
                            Horizental_wall[f'wall{y}{x}'].place(height = 10 , width = 60 , x = (x) * 50 +(x+1)*10 + 5, y = (y)*50 + (y) * 10 +5) 
                            Horizental_wall[f'id{y}{x}'] = Maze.step
                            Horizental_wall[f'id{y}{x+1}'] = Maze.step
                            Maze.step += 1
                            Maze.number_of_p1_wall -= 1
                            lbl_nwallp1['text'] = f'Player1 Walls : {Maze.number_of_p1_wall}'
                            lbl_turns['bg'] = "#00d021"
                            lbl_turns['text'] = "Green Turn"
                    else :
                        if Horizental_wall[f'id{y+1}{x-1}'] != Horizental_wall[f'id{y+1}{x}'] or Horizental_wall[f'id{y+1}{x-1}'] == -1 :
                            arg1['bg'] = "#e8002a" #red
                            arg2['bg'] = "#e8002a"
                            #Vertical_wall[f'wall{y}{x}'].lift()
                            #Vertical_wall[f'wall{y+1}{x}'].lift()
                            Vertical_wall[f'wall{y}{x}'].place(height = 60 , width = 10 , x = x * 50 + (x)*10 + 5, y = (y)*50+(y+1)*10 + 5)
                            Vertical_wall[f'id{y}{x}'] = Maze.step
                            Vertical_wall[f'id{y+1}{x}'] = Maze.step
                            
                            Maze.step += 1
                            Maze.number_of_p1_wall -= 1
                            lbl_nwallp1['text'] = f'Player1 Walls : {Maze.number_of_p1_wall}'
                            lbl_turns['bg'] = "#00d021"
                            lbl_turns['text'] = "Green Turn"
                    assign_wall_to_block()
        else :
            if arg1['bg'] == "#aee2ff" and arg2['bg'] == "#aee2ff" and Maze.number_of_p2_wall != 0:
                clear_square_color()
                if is_valid_wall(x,y,typew) :

                    
                    if typew == 'h' :
                        if Vertical_wall[f'id{y-1}{x+1}'] != Vertical_wall[f'id{y}{x+1}'] or Vertical_wall[f'id{y-1}{x+1}'] == -1:
                            arg1['bg'] = "#00d021" #green
                            arg2['bg'] = "#00d021"
                            Horizental_wall[f'id{y}{x}'] = Maze.step
                            Horizental_wall[f'id{y}{x+1}'] = Maze.step
                            #Horizental_wall[f'wall{y}{x}'].lift()
                            #Horizental_wall[f'wall{y}{x+1}'].lift()
                            Horizental_wall[f'wall{y}{x}'].place(height = 10 , width = 60 , x = (x) * 50 +(x+1)*10 + 5, y = (y)*50 + (y) * 10 +5)
                            assign_wall_to_block()
                            Maze.step += 1
                            Maze.number_of_p2_wall -= 1
                            lbl_nwallp2['text'] = f'Player2 Walls : {Maze.number_of_p2_wall}'
                            lbl_turns['bg'] = "#e8002a"
                            lbl_turns['text'] = "Red Turn"
                    else :
                        if Horizental_wall[f'id{y+1}{x-1}'] != Horizental_wall[f'id{y+1}{x}'] or Horizental_wall[f'id{y+1}{x-1}'] == -1:
                            arg1['bg'] = "#00d021" #green
                            arg2['bg'] = "#00d021"
                            #Vertical_wall[f'wall{y}{x}'].lift()
                            #Vertical_wall[f'wall{y+1}{x}'].lift()
                            Vertical_wall[f'id{y}{x}'] = Maze.step
                            Vertical_wall[f'id{y+1}{x}'] = Maze.step
                            Vertical_wall[f'wall{y}{x}'].place(height = 60 , width = 10 , x = x * 50 + (x)*10 + 5, y = (y)*50+(y+1)*10 + 5)
                            assign_wall_to_block()
                            Maze.step += 1
                            Maze.number_of_p2_wall -= 1
                            lbl_nwallp2['text'] = f'Player2 Walls : {Maze.number_of_p2_wall}'
                            lbl_turns['bg'] = "#e8002a"
                            lbl_turns['text'] = "Red Turn"

def set_yellow_squarGoal(arg,p) :
    #messagebox.showinfo("1" ,f'{Maze.yplayer1} {Maze.xplayer1}')
    #messagebox.showinfo("2" , f'{Maze.yplayer2} {Maze.xplayer2}')
    if Maze.yplayer1 == 8 :
        messagebox.showinfo("End Game" , "Player1 Won")
    elif Maze.yplayer2 == 0 :
        messagebox.showinfo("End Game" , "Player2 Won")
    else :
        if Maze.step % 2 == 0 :
            if p == 1 :
                #messagebox.showinfo("p1 xy" , f'{Maze.xplayer1}  {Maze.yplayer1}')
                clear_square_color()
                if Horizental_wall[f'wall{Maze.yplayer1}{Maze.xplayer1}']['bg'] == "#aee2ff" : #up
                    #messagebox.showinfo("up")
                    #messagebox.showinfo("p1 xy" , f'{Maze.xplayer1}   {Maze.yplayer1}')
                    if Maze.yplayer1 - 1 == Maze.yplayer2 and Maze.xplayer1 == Maze.xplayer2 :
                        if Horizental_wall[f'wall{Maze.yplayer1-1}{Maze.xplayer1}']['bg'] == "#aee2ff" :
                            Square[f'sq{Maze.yplayer1-2}{Maze.xplayer1}']['bg'] = "#ffff79"
                    else :
                        Square[f'sq{Maze.yplayer1-1}{Maze.xplayer1}']['bg'] = "#ffff79"

                if Horizental_wall[f'wall{Maze.yplayer1+1}{Maze.xplayer1}']['bg'] == "#aee2ff" : #down
                    #messagebox.showinfo("down")
                    #messagebox.showinfo("p1 xy" , f'{Maze.xplayer1}   {Maze.yplayer1}')
                    if Maze.yplayer1+1 == Maze.yplayer2 and Maze.xplayer1 == Maze.xplayer2 :
                        if Horizental_wall[f'wall{Maze.yplayer1+2}{Maze.xplayer1}']['bg'] == "#aee2ff" :
                            Square[f'sq{Maze.yplayer1+2}{Maze.xplayer1}']['bg'] = "#ffff79"
                    else :
                        Square[f'sq{Maze.yplayer1+1}{Maze.xplayer1}']['bg'] = "#ffff79"

                if Vertical_wall[f'wall{Maze.yplayer1}{Maze.xplayer1}']['bg'] == "#aee2ff" : #left
                    #messagebox.showinfo("left")
                    #messagebox.showinfo("p1 xy" , f'{Maze.xplayer1}   {Maze.yplayer1}')
                    if Maze.xplayer1 - 1 == Maze.xplayer2 and Maze.yplayer1 == Maze.yplayer2 :
                        if Vertical_wall[f'wall{Maze.yplayer1}{Maze.xplayer1 -1}']['bg'] == "#aee2ff" :
                            Square[f'sq{Maze.yplayer1}{Maze.xplayer1-2}']['bg'] = "#ffff79" 
                    else :
                        Square[f'sq{Maze.yplayer1}{Maze.xplayer1-1}']['bg'] = "#ffff79"

                if Vertical_wall[f'wall{Maze.yplayer1}{Maze.xplayer1+1}']['bg'] == "#aee2ff" : #right
                    #messagebox.showinfo("right")
                    #messagebox.showinfo("p1 xy" , f'{Maze.xplayer1}   {Maze.yplayer1}')
                    if Maze.xplayer1 + 1 == Maze.xplayer2 and Maze.yplayer1 == Maze.yplayer2 :
                        if Vertical_wall[f'wall{Maze.yplayer1}{Maze.xplayer1+2}']['bg'] == "#aee2ff" :
                            Square[f'sq{Maze.yplayer1}{Maze.xplayer1+2}']['bg'] = "#ffff79"
                    else :
                        Square[f'sq{Maze.yplayer1}{Maze.xplayer1+1}']['bg'] = "#ffff79"
        
        ###################### player 2
        else :

            if p == 2 :
                clear_square_color()
                if Horizental_wall[f'wall{Maze.yplayer2}{Maze.xplayer2}']['bg'] == "#aee2ff" :  #up
                    #messagebox.showinfo("up")
                    #messagebox.showinfo("p1 xy" , f'{Maze.xplayer1}   {Maze.yplayer1}')
                    if Maze.yplayer2 - 1 == Maze.yplayer1 and Maze.xplayer1 == Maze.xplayer2 :
                        if Horizental_wall[f'wall{Maze.yplayer2 - 1}{Maze.xplayer2}']['bg'] == "#aee2ff" : 
                            Square[f'sq{Maze.yplayer2-2}{Maze.xplayer2}']['bg'] = "#ffff79"
                    else :
                        Square[f'sq{Maze.yplayer2-1}{Maze.xplayer2}']['bg'] = "#ffff79"

                if Horizental_wall[f'wall{Maze.yplayer2+1}{Maze.xplayer2}']['bg'] == "#aee2ff" : #down
                    #messagebox.showinfo("down")
                    #messagebox.showinfo("p1 xy" , f'{Maze.xplayer1}   {Maze.yplayer1}')
                    if Maze.yplayer2 + 1 == Maze.yplayer1 and Maze.xplayer1 == Maze.xplayer2 :
                        if Horizental_wall[f'wall{Maze.yplayer2+2}{Maze.xplayer2}']['bg'] == "#aee2ff" :
                            Square[f'sq{Maze.yplayer2+2}{Maze.xplayer2}']['bg'] = "#ffff79"
                    else :
                        Square[f'sq{Maze.yplayer2+1}{Maze.xplayer2}']['bg'] = "#ffff79"

                if Vertical_wall[f'wall{Maze.yplayer2}{Maze.xplayer2}']['bg'] == "#aee2ff" : #left
                    #messagebox.showinfo("left")
                    #messagebox.showinfo("p1 xy" , f'{Maze.xplayer1}   {Maze.yplayer1}')
                    if Maze.xplayer2 - 1 == Maze.xplayer1 and Maze.yplayer1 == Maze.yplayer2 :
                        if Vertical_wall[f'wall{Maze.yplayer2}{Maze.xplayer2 -1}']['bg'] == "#aee2ff" :
                            Square[f'sq{Maze.yplayer2}{Maze.xplayer2-2}']['bg'] = "#ffff79" 
                    else :
                        Square[f'sq{Maze.yplayer2}{Maze.xplayer2-1}']['bg'] = "#ffff79"

                if Vertical_wall[f'wall{Maze.yplayer2}{Maze.xplayer2+1}']['bg'] == "#aee2ff" : #right
                    #messagebox.showinfo("right")
                    #messagebox.showinfo("p1 xy" , f'{Maze.xplayer1}   {Maze.yplayer1}')
                    if Maze.xplayer2 + 1 == Maze.xplayer1 and Maze.yplayer1 == Maze.yplayer2 :
                        if Vertical_wall[f'wall{Maze.yplayer2}{Maze.xplayer2+2}']['bg'] == "#aee2ff" :
                            Square[f'sq{Maze.yplayer2}{Maze.xplayer2+2}']['bg'] = "#ffff79"
                    else :
                        Square[f'sq{Maze.yplayer2}{Maze.xplayer2+1}']['bg'] = "#ffff79"
        
        
        #pass
        
def move(arg , y , x, ai_move=False) :
    #messagebox.showinfo("block xy " , f'{x}  {y}')
    gy = 0
    gx = 0
    xx = 0
    yy = 0
    if arg['bg'] == "#ffff79" or ai_move:

        if Maze.step % 2 == 0 :
            

            
            xx = x - Maze.xplayer1
            gx = Maze.xplayer1 + xx
            Maze.xplayer1 += xx
        
            yy = y - Maze.yplayer1
            gy = Maze.yplayer1 + yy
            Maze.yplayer1 += yy
            
            player1.place(x = (gx+1)*10 + gx*50 + 10 , y = (gy+1)*10 + gy*50 + 10)
            clear_square_color()
            Maze.step += 1
            lbl_turns['bg'] = "#00d021"
            lbl_turns['text'] = "Green Turn"
            if Maze.yplayer1 == 8 :
                
                lbl_turns['bg'] = "#b4a8ff"
                lbl_turns['text'] = "Player1 Won"
                for i in range(9) :
                    Square[f'sq{8}{i}']['bg'] = "#ffa8a8"
                
                    
                messagebox.showinfo("End Game" , "Player1 Won")
        
        ######################################################### p2
        else :
            
            xx = x - Maze.xplayer2
            gx = Maze.xplayer2 + xx
            Maze.xplayer2 += xx
        

        
            yy = y - Maze.yplayer2
            gy = Maze.yplayer2 + yy
            Maze.yplayer2 += yy
            
            player2.place(x = (gx+1)*10 + gx*50 + 10 , y = (gy+1)*10 + gy*50 + 10)
            clear_square_color()
            Maze.step += 1
            lbl_turns['bg'] = "#e8002a"
            lbl_turns['text'] = "Red Turn"
            if Maze.yplayer2 == 0 :
                lbl_turns['bg'] = "#b4a8ff"
                lbl_turns['text'] = "Player2 Won"
                for i in range(9) :
                    Square[f'sq{0}{i}']['bg'] = "#b4ffa8"
                messagebox.showinfo("End Game" , "Player2 Won")


# Constants 
MAX_WALLS = 10  
AI_WALL_SEARCH_LIMIT = 6  # Max wall positions to consider
AI_PLAYER1 = True  # Set to True to enable AI for player 1
AI_PLAYER2 = True  # Set to True to enable AI for player 2
SEARCH_DEPTH = 2 # Depth for alpha-beta search
WALL_BONUS_WEIGHT = 1.2  # New constant
_PATH_CACHE  = {}

class GameState:
    def __init__(self):
        # Player positions
        self.xplayer1 = Maze.xplayer1
        self.yplayer1 = Maze.yplayer1
        self.xplayer2 = Maze.xplayer2
        self.yplayer2 = Maze.yplayer2
        
        # Wall counts
        self.p1_walls = Maze.number_of_p1_wall
        self.p2_walls = Maze.number_of_p2_wall
        
        # Turn tracking
        self.turn = Maze.step % 2  # Important: Use actual game step
        
        # Sync walls from GUI
        self.horizontal_walls = []
        for i in range(10):
            row = []
            for j in range(9):
                # Directly check button color state
                row.append(Horizental_wall[f'wall{i}{j}']['bg'] != "#aee2ff")
            self.horizontal_walls.append(row)
            
        self.vertical_walls = []
        for i in range(9):
            col = []
            for j in range(10):
                # Directly check button color state
                col.append(Vertical_wall[f'wall{i}{j}']['bg'] != "#aee2ff")
            self.vertical_walls.append(col)
        
        # Sync block state from Maze
        self.block = [[{
            'u': Maze.block[i][j]['u'],
            'd': Maze.block[i][j]['d'],
            'l': Maze.block[i][j]['l'],
            'r': Maze.block[i][j]['r'],
            'v': Maze.block[i][j]['v']
        } for j in range(9)] for i in range(9)]

def get_pawn_moves(state, is_player1):
    moves = []
    if is_player1:
        y, x = state.yplayer1, state.xplayer1
        opponent_y, opponent_x = state.yplayer2, state.xplayer2
    else:
        y, x = state.yplayer2, state.xplayer2
        opponent_y, opponent_x = state.yplayer1, state.xplayer1

    # Regular moves
    # Up
    if y > 0 and not state.horizontal_walls[y][x]:
        if (y-1 != opponent_y or x != opponent_x):
            moves.append(('move', y-1, x))
        else:
            # Jump over opponent
            if y > 1 and not state.horizontal_walls[y-1][x]:
                moves.append(('move', y-2, x))
            # Diagonal jumps
            if x > 0 and not state.vertical_walls[y-1][x]:
                moves.append(('move', y-1, x-1))
            if x < 8 and not state.vertical_walls[y-1][x+1]:
                moves.append(('move', y-1, x+1))
    # Down
    if y < 8 and not state.horizontal_walls[y+1][x]:
        if (y+1 != opponent_y or x != opponent_x):
            moves.append(('move', y+1, x))
        else:
            if y < 7 and not state.horizontal_walls[y+2][x]:
                moves.append(('move', y+2, x))
            if x > 0 and not state.vertical_walls[y+1][x]:
                moves.append(('move', y+1, x-1))
            if x < 8 and not state.vertical_walls[y+1][x+1]:
                moves.append(('move', y+1, x+1))
    # Left
    if x > 0 and not state.vertical_walls[y][x]:
        if (y != opponent_y or x-1 != opponent_x):
            moves.append(('move', y, x-1))
        else:
            if x > 1 and not state.vertical_walls[y][x-1]:
                moves.append(('move', y, x-2))
            if y > 0 and not state.horizontal_walls[y][x-1]:
                moves.append(('move', y-1, x-1))
            if y < 8 and not state.horizontal_walls[y+1][x-1]:
                moves.append(('move', y+1, x-1))
    # Right
    if x < 8 and not state.vertical_walls[y][x+1]:
        if (y != opponent_y or x+1 != opponent_x):
            moves.append(('move', y, x+1))
        else:
            if x < 7 and not state.vertical_walls[y][x+2]:
                moves.append(('move', y, x+2))
            if y > 0 and not state.horizontal_walls[y][x+1]:
                moves.append(('move', y-1, x+1))
            if y < 8 and not state.horizontal_walls[y+1][x+1]:
                moves.append(('move', y+1, x+1))
    
    
    return moves
                  
def get_valid_moves(state, is_player1):
    moves = []
    # Existing pawn moves
    moves += get_pawn_moves(state, is_player1)
    
    # Add wall placements
    if (is_player1 and state.p1_walls > 0) or (not is_player1 and state.p2_walls > 0):
        walls = get_valid_walls(state, is_player1)
        moves += walls
    
    return moves

def get_valid_walls(state, is_player1):
    """Improved wall placement logic with better coordinate handling"""
    if (is_player1 and state.p1_walls == 0) or (not is_player1 and state.p2_walls == 0):
        return []
    
    opponent = 2 if is_player1 else 1
    opponent_path = get_shortest_path_coordinates(state, opponent)
    wall_candidates = []
    
    # Generate walls along opponent's path
    for y, x in opponent_path[:4]:  # Look 4 steps ahead
        # Horizontal walls (block vertical movement)
        if y > 0 and x < 8:
            if not state.horizontal_walls[y][x] and not state.horizontal_walls[y][x+1]:
                wall_candidates.append(('wall', x, y, 'h'))
        # Vertical walls (block horizontal movement)
        if x > 0 and y < 8:
            if not state.vertical_walls[y][x] and not state.vertical_walls[y+1][x]:
                wall_candidates.append(('wall', x, y, 'v'))
    
    # Add defensive walls near current player
    player_y, player_x = (state.yplayer1, state.xplayer1) if is_player1 else (state.yplayer2, state.xplayer2)
    for dy in [-1, 0, 1]:
        for dx in [-1, 0, 1]:
            y = player_y + dy
            x = player_x + dx
            if 0 <= y < 9 and 0 <= x < 8:
                if not state.horizontal_walls[y][x] and not state.horizontal_walls[y][x+1]:
                    wall_candidates.append(('wall', x, y, 'h'))
            if 0 <= y < 8 and 0 <= x < 9:
                if not state.vertical_walls[y][x] and not state.vertical_walls[y+1][x]:
                    wall_candidates.append(('wall', x, y, 'v'))
    
    # Validate walls and remove duplicates
    valid_walls = []
    seen = set()
    for wall in wall_candidates:
        x, y, orient = wall[1], wall[2], wall[3]
        key = (x, y, orient)
        if key not in seen and is_valid_wall_simulation(state, x, y, orient):
            seen.add(key)
            valid_walls.append(wall)
    
    return valid_walls[:AI_WALL_SEARCH_LIMIT]

def get_shortest_path_coordinates(state, player):
    """BFS to find the shortest path coordinates without caching"""
    target_row = 8 if player == 1 else 0
    start_y, start_x = (state.yplayer1, state.xplayer1) if player == 1 else (state.yplayer2, state.xplayer2)
    
    visited = [[None]*9 for _ in range(9)]
    queue = deque([(start_y, start_x)])
    visited[start_y][start_x] = (-1, -1)
    
    while queue:
        y, x = queue.popleft()
        if y == target_row:
            # Reconstruct path
            path = []
            current = (y, x)
            while current != (-1, -1):
                path.append(current)
                current = visited[current[0]][current[1]]
            return path[::-1][1:]  # Exclude starting position
        
        # Explore neighbors using block data
        # Up
        if y > 0 and not state.block[y][x]['u'] and not visited[y-1][x]:
            visited[y-1][x] = (y, x)
            queue.append((y-1, x))
        # Down
        if y < 8 and not state.block[y][x]['d'] and not visited[y+1][x]:
            visited[y+1][x] = (y, x)
            queue.append((y+1, x))
        # Left
        if x > 0 and not state.block[y][x]['l'] and not visited[y][x-1]:
            visited[y][x-1] = (y, x)
            queue.append((y, x-1))
        # Right
        if x < 8 and not state.block[y][x]['r'] and not visited[y][x+1]:
            visited[y][x+1] = (y, x)
            queue.append((y, x+1))
    
    return []

def is_move_valid(state, y, x, ny, nx):
    # Check if move from (y,x) to (ny,nx) is valid
    if ny == y - 1:  # Up
        return not state.block[y][x]['u']
    elif ny == y + 1:  # Down
        return not state.block[y][x]['d']
    elif nx == x - 1:  # Left
        return not state.block[y][x]['l']
    elif nx == x + 1:  # Right
        return not state.block[y][x]['r']
    return False


def is_valid_wall_simulation(state, x, y, wall_type):
    # Check immediate adjacency
    if wall_type == 'h' and (state.horizontal_walls[y][x] or state.horizontal_walls[y][x+1]):
        return False
    if wall_type == 'v' and (state.vertical_walls[y][x] or state.vertical_walls[y+1][x]):
        return False
    
    # # Create temp state
    # temp_state = copy.deepcopy(state)
    # Replace deepcopy with manual copy
    temp_state = GameState()
    # Copy all walls manually
    temp_state.horizontal_walls = [row.copy() for row in state.horizontal_walls]
    temp_state.vertical_walls = [col.copy() for col in state.vertical_walls]
    
    # Apply wall
    if wall_type == 'h':
        temp_state.horizontal_walls[y][x] = True
        temp_state.horizontal_walls[y][x+1] = True
        # Update block structure
        temp_state.block[y][x]['u'] = True
        temp_state.block[y][x+1]['u'] = True
        if y > 0:
            temp_state.block[y-1][x]['d'] = True
            temp_state.block[y-1][x+1]['d'] = True
    else:
        temp_state.vertical_walls[y][x] = True
        temp_state.vertical_walls[y+1][x] = True
        # Update block structure
        temp_state.block[y][x]['l'] = True
        temp_state.block[y+1][x]['l'] = True
        if x > 0:
            temp_state.block[y][x-1]['r'] = True
            temp_state.block[y+1][x-1]['r'] = True
    
    return has_valid_path(temp_state, 1) and has_valid_path(temp_state, 2)

def has_valid_path(state, player):
    visited = [[False]*9 for _ in range(9)]
    queue = deque()
    target_row = 8 if player == 1 else 0
    
    if player == 1:
        start_y, start_x = state.yplayer1, state.xplayer1
    else:
        start_y, start_x = state.yplayer2, state.xplayer2
    
    queue.append((start_y, start_x))
    visited[start_y][start_x] = True
    
    while queue:
        y, x = queue.popleft()
        if y == target_row:
            return True
        
        # Check moves using precomputed block data
        if not state.block[y][x]['u'] and y > 0 and not visited[y-1][x]:
            visited[y-1][x] = True
            queue.append((y-1, x))
        if not state.block[y][x]['d'] and y < 8 and not visited[y+1][x]:
            visited[y+1][x] = True
            queue.append((y+1, x))
        if not state.block[y][x]['l'] and x > 0 and not visited[y][x-1]:
            visited[y][x-1] = True
            queue.append((y, x-1))
        if not state.block[y][x]['r'] and x < 8 and not visited[y][x+1]:
            visited[y][x+1] = True
            queue.append((y, x+1))
    
    return False

def heuristic(state):
    """Simplified and more effective heuristic function"""
    def calculate_path(y, x, target_row):
        # Basic BFS path length calculation
        visited = [[False]*9 for _ in range(9)]
        queue = deque([(y, x, 0)])
        visited[y][x] = True
        
        while queue:
            cy, cx, steps = queue.popleft()
            if cy == target_row:
                return steps
            # Check all possible moves
            # Up
            if cy > 0 and not state.block[cy][cx]['u'] and not visited[cy-1][cx]:
                visited[cy-1][cx] = True
                queue.append((cy-1, cx, steps+1))
            # Down
            if cy < 8 and not state.block[cy][cx]['d'] and not visited[cy+1][cx]:
                visited[cy+1][cx] = True
                queue.append((cy+1, cx, steps+1))
            # Left
            if cx > 0 and not state.block[cy][cx]['l'] and not visited[cy][cx-1]:
                visited[cy][cx-1] = True
                queue.append((cy, cx-1, steps+1))
            # Right
            if cx < 8 and not state.block[cy][cx]['r'] and not visited[cy][cx+1]:
                visited[cy][cx+1] = True
                queue.append((cy, cx+1, steps+1))
        return float('inf')  # No path found
    
    p1_path = calculate_path(state.yplayer1, state.xplayer1, 8)
    p2_path = calculate_path(state.yplayer2, state.xplayer2, 0)
    
    # Base score components
    path_diff = (p2_path - p1_path) * 2.0  # Favor blocking opponent
    
    # Wall bonus calculation
    if state.turn == 0:
        wall_bonus = state.p1_walls * WALL_BONUS_WEIGHT
    else:
        wall_bonus = state.p2_walls * WALL_BONUS_WEIGHT
    
    # Immediate win conditions
    if p1_path == 0:
        return math.inf
    if p2_path == 0:
        return -math.inf
    
    return path_diff + wall_bonus

def alpha_beta(state, depth, alpha, beta, maximizing_player):
    """Optimized alpha-beta pruning with better move ordering"""
    # Immediate win check
    if state.yplayer1 == 8:
        return math.inf if maximizing_player else -math.inf
    if state.yplayer2 == 0:
        return -math.inf if maximizing_player else math.inf
    
    if depth == 0:
        return heuristic(state)
    
    valid_moves = get_valid_moves(state, maximizing_player)
    
    # Prioritize moves that reach goal immediately
    valid_moves.sort(key=lambda m: 0 if m[0] == 'move' and (
        (maximizing_player and m[1] == 8) or 
        (not maximizing_player and m[1] == 0)
    ) else 1)
    
    if maximizing_player:
        max_eval = -math.inf
        for move in valid_moves:
            new_state = apply_move(state, move)
            eval = alpha_beta(new_state, depth-1, alpha, beta, False)
            max_eval = max(max_eval, eval)
            alpha = max(alpha, eval)
            if beta <= alpha:
                break
        return max_eval
    else:
        min_eval = math.inf
        for move in valid_moves:
            new_state = apply_move(state, move)
            eval = alpha_beta(new_state, depth-1, alpha, beta, True)
            min_eval = min(min_eval, eval)
            beta = min(beta, eval)
            if beta <= alpha:
                break
        return min_eval
    
def apply_move(old_state, move):
    # Create lightweight copy
    state = GameState()
    
    # Copy primitive values directly
    state.xplayer1 = old_state.xplayer1
    state.yplayer1 = old_state.yplayer1
    state.xplayer2 = old_state.xplayer2
    state.yplayer2 = old_state.yplayer2
    state.p1_walls = old_state.p1_walls
    state.p2_walls = old_state.p2_walls
    state.turn = old_state.turn
    
    # Copy wall arrays using shallow copies
    state.horizontal_walls = [row[:] for row in old_state.horizontal_walls]
    state.vertical_walls = [col[:] for col in old_state.vertical_walls]
    
    # Copy block structure using your original format
    state.block = [[{
        'u': cell['u'],
        'r': cell['r'],
        'l': cell['l'], 
        'd': cell['d'],
        'v': cell['v']
    } for cell in row] for row in old_state.block]

    # Apply move using your original logic
    if move[0] == 'move':
        if state.turn == 0:
            state.yplayer1, state.xplayer1 = move[1], move[2]
        else:
            state.yplayer2, state.xplayer2 = move[1], move[2]
            
    elif move[0] == 'wall':
        x, y, wall_type = move[1], move[2], move[3]
        
        # Your original block update logic
        if wall_type == 'h':
            state.block[y][x]['u'] = True
            state.block[y][x+1]['u'] = True
            state.block[y-1][x]['d'] = True
            state.block[y-1][x+1]['d'] = True
        else:
            state.block[y][x]['l'] = True
            state.block[y+1][x]['l'] = True
            state.block[y][x-1]['r'] = True
            state.block[y+1][x-1]['r'] = True

        # Wall count update
        if state.turn == 0:
            state.p1_walls -= 1
        else:
            state.p2_walls -= 1

    # Turn switching remains the same
    state.turn = 1 - state.turn
    
    return state


# Update ai_move function
def ai_move():
    """Improved AI move selection with better tie-breaking"""
    if Maze.yplayer1 == 8 or Maze.yplayer2 == 0:
        return

    assign_wall_to_block()
    current_state = GameState()
    
    best_move = None
    best_value = -math.inf if current_state.turn == 0 else math.inf
    valid_moves = get_valid_moves(current_state, current_state.turn == 0)
    
    for move in valid_moves:
        new_state = apply_move(current_state, move)
        value = alpha_beta(new_state, SEARCH_DEPTH, -math.inf, math.inf, new_state.turn == 0)
        
        # Add small randomness to break ties
        if current_state.turn == 0:  # Maximizing
            if value > best_value or (value == best_value and random.random() < 0.4):
                best_value = value
                best_move = move
        else:  # Minimizing
            if value < best_value or (value == best_value and random.random() < 0.4):
                best_value = value
                best_move = move
   

    # Execute best move
    if best_move:
        # Handle pawn move
        if best_move[0] == 'move':
            y, x = best_move[1], best_move[2]
            if current_state.turn == 0:  # Player 1
                Maze.xplayer1 = x
                Maze.yplayer1 = y
                player1.place(x=(x+1)*10 + x*50 + 10, y=(y+1)*10 + y*50 + 10)
            else:  # Player 2
                Maze.xplayer2 = x
                Maze.yplayer2 = y
                player2.place(x=(x+1)*10 + x*50 + 10, y=(y+1)*10 + y*50 + 10)
                
        # Handle wall placement
        elif best_move[0] == 'wall':
            x, y, wall_type = best_move[1], best_move[2], best_move[3]
            if current_state.turn == 0:
                color = "#e8002a"
                Maze.number_of_p1_wall -= 1
            else:
                color = "#00d021"
                Maze.number_of_p2_wall -= 1

            # Update walls
            if wall_type == 'h':
                Horizental_wall[f'wall{y}{x}']['bg'] = color
                Horizental_wall[f'wall{y}{x+1}']['bg'] = color
            else:
                Vertical_wall[f'wall{y}{x}']['bg'] = color
                Vertical_wall[f'wall{y+1}{x}']['bg'] = color
            
            # Critical: Update block structure after wall placement
            assign_wall_to_block()

        # Update game state
        Maze.step += 1  # Single increment per move
        update_ui()

    # Schedule next move
    delay = random.randint(400, 800) if any([AI_PLAYER1, AI_PLAYER2]) else 1000
    Quoridor.after(delay, ai_move)
    
def update_ui():
    lbl_turns['bg'] = "#00d021" if Maze.step % 2 else "#e8002a"
    lbl_turns['text'] = "Green Turn" if Maze.step % 2 else "Red Turn"
    lbl_nwallp1['text'] = f"Player1 Walls: {Maze.number_of_p1_wall}"
    lbl_nwallp2['text'] = f"Player2 Walls: {Maze.number_of_p2_wall}"
    Quoridor.update_idletasks()  # Force UI refresh
# Start AI moves if both players are AI
if AI_PLAYER1 and AI_PLAYER2:
    Quoridor.after(1000, ai_move)

def start_ai():
    if (AI_PLAYER1 and Maze.step % 2 == 0) or (AI_PLAYER2 and Maze.step % 2 == 1):
        delay = 300 if Maze.step > 2 else 800  # Faster after first moves
        Quoridor.after(delay, ai_move)
    Quoridor.after(100, start_ai)  # Keep checking

# Quoridor.after(1000, start_ai) 
#wall = tk.Button(Quoridor , background  = "red" )
#wall.config(command = lambda arg = wall : change_color(arg))
#wall.place(height = 20 , width = 50 , x = 50 , y = 200)

#3 # loop
Quoridor.mainloop()




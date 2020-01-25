
import pygame
import math
import numpy as np
import random
import tkinter as tk
from tkinter import *
import os
import time

def pos2index(pos):
    return (int(pos[1]/100),int(pos[0]/100))

def index2pos(ind):
    return (ind[1]*100,ind[0]*100)

def toggle_player(player):
    player=(player+1)%2
    return player

class player:
    """docstring for Player"""
    def __init__(self, name, type):
        super(player, self).__init__()
        self.name = name
        self.type = type
    def play_typical_random(self,previous_position,valid_moves,chess_board):
        time.sleep(0.2)
        if previous_position[0] < 4:
            next_row= (previous_position[0]+2)%4
        else:
            next_row=4+(previous_position[0]+2)%4
        if previous_position[1]%2==0:
            next_column =previous_position[1]+1
        else:
            next_column =previous_position[1]-1
        play_position=[next_row,next_column]
        if previous_position==[-1,-1]:
            play_position=[random.randint(0,7),random.randint(0,7)]
        # elif randomness==1 or chess_board[play_position[0],play_position[1]]==1: I will remove the randomness part for  niw
        elif chess_board[play_position[0],play_position[1]]==1:
            selector = random.randint(0,len(valid_moves[0])-1)
            play_position = valid_moves[:,selector].tolist()
        return play_position

    def play_graphically(self,previous_position,chess_board):
                    while True:
                        for event in pygame.event.get():
                            if event.type == pygame.MOUSEBUTTONUP:
                                clicked_pos = pygame.mouse.get_pos()
                                knight_pos = (math.floor(clicked_pos[0]/100)*100,math.floor(clicked_pos[1]/100)*100)
                                play_position=pos2index(knight_pos)
                                checker=abs(np.subtract(play_position,previous_position))
                                if ( checker.tolist() == [2,1] or checker.tolist() == [1,2] or previous_position == [-1,-1]) and chess_board[play_position[0]][play_position[1]] == 0:
                                    return play_position
                        root.update()

    def select_move(self,chess_board,gamedisp):
        if (self.type == "AI"):
            play_position=self.play_typical_random(chess_board.current_position,chess_board.valid_moves,chess_board.chess_board)
        else:
            play_position=self.play_graphically(chess_board.current_position,chess_board.chess_board)
        return play_position

class board:
    """docstring for Player"""

    def __init__(self, size):
        super(board, self).__init__()
        self.size = size
        self.chess_board=np.zeros(size, dtype=int)
        self.current_position=[-1,-1]
        self.valid_on_board()
        self.valid_game = True
    def play_move(self, play_position):
        self.chess_board[play_position[0]][play_position[1]]=1
        self.current_position=play_position
        self.valid_on_board()
        self.valid_game = self.valid_check(self.valid_moves)
    def valid_on_board(self):
        position=self.current_position
        valid_moves=np.zeros([2,8],dtype=int)
        valid_moves[0]=([1,2, 1, 2, -1 ,-2, -1, -2])
        valid_moves[1]=([2,1, -2, -1, 2 ,1, -2, -1])
        valid_moves[0]+=position[0]
        valid_moves[1]+=position[1]
        l=len(valid_moves[0])-1
        for i in range(l,-1,-1):
            if valid_moves[0][i]> 7 or valid_moves[1][i]> 7 or valid_moves[0][i]< 0 or valid_moves[1][i]<0 or self.chess_board[valid_moves[0][i]][valid_moves[1][i]]==1:
                valid_moves=np.delete(valid_moves,i,1)
        self.valid_moves=valid_moves
    def valid_check(self,valid_moves):
        flag = True
        if not valid_moves[0].tolist():
            flag=False
        return flag

class gamedisp:
    background = pygame.image.load("chess.png");
    sprite= pygame.image.load('knight.png')
    welcom_screen=pygame.image.load("welcome.png")
    def __init__(self):
        pygame.init()
        self.gameDisplay=pygame.display.set_mode((800,800))
        self.gameDisplay.fill((255,255,255))
        self.gameDisplay.blit(self.welcom_screen,(0,0))
        pygame.display.update()

    def load_winning(self,winner):
        vbb= pygame.image.load("winning.jpg");
        self.update_end(winner,vbb)
    def load_losing(self):
        vbb= pygame.image.load("losing.png");
        self.update_end("CPU",vbb)
    def update_end(self,winner,vbb):
        font = pygame.font.Font('freesansbold.ttf', 80)
        text = font.render(str(winner)+" WINS", True, (0,255,0), (0,0,128))
        textRect = text.get_rect()
        textRect.center = (400, 700)
        while True :
            self.gameDisplay.fill((255,255,255))
            self.gameDisplay.blit(vbb,(0,0))
            self.gameDisplay.blit(text, textRect)
            pygame.display.update()
            time.sleep(2)
            break

    def update_board(self,chess_board):
        self.gameDisplay=pygame.display.set_mode((800,800))
        self.gameDisplay.blit(self.background,(0,0))
        self.renderRed(chess_board)
        pygame.display.update()

    def update_knight(self,play_position):
        knight_pos=index2pos(play_position)
        self.gameDisplay.blit(self.sprite,(knight_pos))
        pygame.display.update()
    def renderRed(self,chess_board):
        taken_square=np.where(chess_board==1)
        taken_square_r=taken_square[0]
        red_square = pygame.Surface((100,100), pygame.SRCALPHA)
        red_square.fill((255,0,0,128))
        if len(taken_square_r)>0:
            taken_square_c=taken_square[1]
            for i in range (len(taken_square_r)):
                red_pos=index2pos((taken_square_r[i],taken_square_c[i]))
                self.gameDisplay.blit(red_square, (red_pos[0],red_pos[1]))

class Window(Frame):
    def __init__(self,master=None):
        Frame.__init__(self,master)
        self.master=master
        self.init_window()
    def toggle_player2(self): #that one function is responsible for turning the choice of the name of player 2 on and off
        global n
        if not (self.active_ai):
            n=self.name2.get()
            self.name2.delete(0,END)
            self.name2.insert(0,'CPU')
            self.name2.configure(state=DISABLED)

        else:
            self.name2.configure(state=NORMAL)
            self.name2.delete(0,END)
            self.name2.insert(0,n)
        self.active_ai = not self.active_ai

    def init_window(self):
        self.master.title("Knights Game")
        self.pack(fill='both', expand=1)

        embed = tk.Frame(self, width = 800, height = 800,bg='black') #creates embed frame for pygame window
        embed.place(x=0,y=0) #packs window to the left
        os.environ['SDL_WINDOWID'] = str(embed.winfo_id())
        os.environ['SDL_VIDEODRIVER'] = 'windib'
        self.gamedisp_h=gamedisp()

        button_win=Frame(self,width=350,height=800)
        button_win.place(x=800,y=0)
        data_frame=Frame(button_win,width=350,height=100,bg='black')
        data_frame.place(x=0,y=0)

        self.quite_frame=Frame(button_win,width=350,height=50)
        self.moves_frame=Frame(master=root,width=350,height=600)
        self.moves_frame.place(x=900,y=130)


        name_label=Label(data_frame,text="Player1 Name:")
        name_label.grid(row=0)
        self.name1=Entry(data_frame)
        self.name1.grid(row=0,column=1,sticky=W)
        self.name1.insert(0, 'player1')

        checkvar = tk.BooleanVar()
        self.playAI= Checkbutton(data_frame,text="CPU player 2",variable = checkvar,command=self.toggle_player2)
        self.playAI.grid(columnspan=2,sticky=W+N+E+S)
        # self.playAI.select()
        self.active_ai=checkvar.get()

        self.player2_first = tk.BooleanVar(value=False)
        self.player2_first_button=Checkbutton(data_frame,text="Player 2 First",variable = self.player2_first)
        self.player2_first_button.grid(row=4,columnspan=2,sticky=W+N+E+S)

        self.name2_label=Label(data_frame,text="Player2 Name:")
        self.name2_label.grid(row=2)
        self.name2=Entry(data_frame)
        self.name2.grid(row=2,column=1,sticky=W)
        self.name2.insert(0,'player2')

        self.play_button=Button(data_frame,text="START!",command=self.game_transition)
        self.play_button.grid(row = 0, column = 3,rowspan = 4,columnspan=4,sticky=E+N+W+S)

    def game_transition(self):
        self.play_button.configure(state=DISABLED)
        self.name2.configure(state=DISABLED)
        self.playAI.configure(state=DISABLED)
        self.name1.configure(state=DISABLED)
        self.player2_first_button.configure(state=DISABLED)
        self.quit_button=Button(self.quite_frame,font=("Consolas 18 bold"),fg='red',text="QUIT!",width=22, height=1,borderwidth=3,command=self.quit_game)
        self.quit_button.pack(expand=YES,fill='x')
        self.quite_frame.place(x=5,y=740)
        lbl = Label(self.moves_frame,text = "A list of moves for ")
        lbl.grid(row=0,sticky=W+N+E+S)
        if not self.player2_first.get():
            lbl2 = Label(self.moves_frame,text = self.name1.get(),width=8)
            lbl3 = Label(self.moves_frame,text = self.name2.get(),width=8)
        else:
            lbl3 = Label(self.moves_frame,text = self.name1.get(),width=8)
            lbl2 = Label(self.moves_frame,text = self.name2.get(),width=8)
        lbl2.grid(row=1,column=0,sticky=W)
        lbl3.grid(row=1,column=1,sticky=W)
        self.listbox1 = Listbox(self.moves_frame)
        self.listbox1.config(width=8,height=25)
        self.listbox1.grid(row=3,column=0,columnspan=2,sticky=W)
        self.listbox2 = Listbox(self.moves_frame)
        self.listbox2.config(width=8,height=25)
        self.listbox2.grid(row=3,column=1,columnspan=2,sticky=W)
        self.start_game()

    def quit_game(self):

        self.quit_button.pack_forget()
        self.play_button.configure(state=NORMAL)
        self.player2_first_button.configure(state=NORMAL)
        self.playAI.configure(state=NORMAL)
        self.name1.configure(state=NORMAL)
        if not self.active_ai:
        	self.name2.configure(state=NORMAL)
        if self.winner:
            if self.winner=='CPU':
                self.gamedisp_h.load_losing()
            else:
                self.gamedisp_h.load_winning(self.winner)
        self.gamedisp_h=gamedisp()

    def insert_to_listbox(self,play_position,move_num):
        i=move_num
        files=['A','B','C','D','E','F','G','H']
        if i%2==1:
            self.listbox1.insert(i-1,str(math.ceil(i/2))+"."+files[play_position[1]]+str(8-play_position[0]))
        else:
            self.listbox2.insert(i-1,str(math.ceil(i/2))+"."+files[play_position[1]]+str(8-play_position[0]))

    def start_game(self):
        player1=player(self.name1.get(), "HUMAN")
        player2=player(self.name2.get(), "HUMAN")
        self.winner=None
        if self.player2_first.get():
            current_player_index=1
        else:
            current_player_index=0

        if self.active_ai:
            player2.type="AI"
        move_num=1
        board_size=[8,8]
        chess_board=board(board_size)
        self.gamedisp_h.update_board(chess_board)
        previous_position = [-1,-1]
        players=[player1,player2]
        while True:
            current_player = players[current_player_index]
            play_position = current_player.select_move(chess_board,self.gamedisp_h)
            self.gamedisp_h.update_board(chess_board.chess_board)
            chess_board.play_move(play_position)
            self.gamedisp_h.update_knight(play_position)
            pygame.display.update()
            self.insert_to_listbox(play_position,move_num)
            move_num+=1
            root.update()
            if not (chess_board.valid_game):
                break
            current_player_index=toggle_player(current_player_index)
            pygame.display.update()

        self.winner=players[current_player_index].name
        self.quit_game()
global root
root=Tk()
root.geometry("1150x800")
app=Window(root)
root.mainloop()

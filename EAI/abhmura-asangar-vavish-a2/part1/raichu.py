#
# raichu.py : Play the game of Raichu
#
# Vaibhav Vishwanath : 2000912419
#
# Based on skeleton code by D. Crandall, Oct 2021
#
import sys
import time
from typing import Collection
from copy import deepcopy
import numpy as np
import math

def board_to_string(board, N):
    return "\n".join(board[i:i+N] for i in range(0, len(board), N))

def evaluate(board,player):
    d={}
    for i in board_to_string(board,len(board)):
        if i in d:
            d[i]=d[i]+1
        else:
            d[i]=1
    if player=='w':
        return 2*(d.get('w',0)-d.get('b',0))  + 8* (d.get('W',0)-d.get('B',0))+ 64*(d.get('@',0)-d.get('$',0))
    else:
        return 2*(d.get('b',0)-d.get('w',0))  + 8* (d.get('B',0)-d.get('W',0))+ 64*(d.get('$',0)-d.get('@',0))
    
   
def count_white(board):
    count=0
    for i in board_to_string(board,len(board)):
        if i in 'wW@':
            count+=1
    return count

def count_black(board):
    count=0
    for i in board_to_string(board,len(board)):
        if i in 'bB$':
            count+=1
    return count



#Move Pichu diagonally left  
def pichu_move1(board,current,N,player):
    row,col=current
    if player=='w':
        row=row+1
        col=col-1
    else:
        row=row-1
        col=col-1
    
    if row<N and row>=0 and col >=0:
        if board[row][col] =='.':
            return (row,col)
        else:
            return None
    else:
        return None

#Move Pichu Diagonally Right
def pichu_move2(board,current,N,player):
    row,col=current
    if player=='w':
        row=row+1
        col=col+1
    else:
        row=row-1
        col=col+1
    if row<N and row>=0 and col < N:
        if board[row][col] =='.':
            return (row,col)
        else:
            return None
    else:
        return None

#Move DIagonally Left over oppositon Pichu 
def pichu_move3(board,current,N,player):
    row,col=current
    if player=='w':
        row=row+2
        col=col-2
    else:
        row=row-2
        col=col-2
    if row<N and row>=0 and col>=0:
        if board[row][col]=='.':
            return (row,col)
        else:
            return None
    else:
        return None

#Move Diagonally Right over oppositon Pichu
def pichu_move4(board,current,N,player):
    row,col=current
    if player=='w':
        row=row+2
        col=col+2
    else:
        row=row-2
        col=col+2
    if row<N and row>=0 and col<N:
        if board[row][col]=='.':
            return (row,col)
        else:
            return None
    else:
        return None
            
    


def move_pichu(board,current,N,player):
    moves=[]
    r,c=current

    moves.append((pichu_move1(board,current,N,player),1))
    moves.append((pichu_move2(board,current,N,player),2))
    
    
    if player=='w':
        opp='b'
        r=r+1
        c=c-1
        if r>=0 and r<N and c>=0:
            if board[r][c] in opp:
                moves.append((pichu_move3(board,current,N,player),3))
    
    r,c=current
    if player=='b':
        opp='w'
        r=r-1
        c=c-1
        if r>=0 and r<N and c>=0:
            if board[r][c] in opp:
                moves.append((pichu_move3(board,current,N,player),3))

    r,c=current
    if player=='w':
        opp='b'
        r=r+1
        c=c+1
        if r>=0 and r<N and c<N:
            if board[r][c] in opp:
                moves.append((pichu_move4(board,current,N,player),4))
    r,c=current
    if player=='b':
        opp='w'
        r=r-1
        c=c+1
        if r>=0 and r<N and c<N:
            if board[r][c] in opp:
                moves.append((pichu_move4(board,current,N,player),4))
    
    #print(moves)
    moves= list(filter(lambda x: x[0] is not None, moves))
    #print(moves)
    return moves
    
#Move Pikachu 1 step forward
def pikachu_move1(board,current,N,player):
    row,col=current
    if player=='w':
        row=row+1
    else:
        row=row-1
    if row<N and row>=0:
        if board[row][col]=='.':
            return (row,col)
        else:
            return None
    else:
        return None

#move Pikachu 2 steps forward
def pikachu_move2(board,current,N,player):
    row,col=current
    if player=='w':
        row=row+2
    else:
        row=row-2
    if row<N and row>=0:
        if board[row][col]=='.' and board[row-1][col]=='.':
            return (row,col)
        else:
            return None
    else:
        return None

#Move Pikachu 1 step right
def pikachu_move3(board,current,N,player):
    row,col=current
    col=col+1
    if col<N and col>=0:
        if board[row][col]=='.':
            return (row,col)
        else:
            return None
    else:
        return None

#Move Pikachu 2 step right
def pikachu_move4(board,current,N,player):
    row,col=current
    col=col+2
    if col<N and col>=0:
        if board[row][col]=='.' and board[row][col-1]=='.':
            return (row,col)
        else:
            return None
    else:
        return None

#Move Pikachu 1 step left
def pikachu_move5(board,current,N,player):
    row,col=current
    col=col-1
    if col<N and col>=0:
        if board[row][col]=='.':
            return (row,col)
        else:
            return None
    else:
        return None

#Move Pikachu 2 step left
def pikachu_move6(board,current,N,player):
    row,col=current
    col=col-2
    if col<N and col>=0:
        if board[row][col]=='.' and board[row][col+1]=='.':
            return (row,col)
        else:
            return None
    else:
        return None

#Move Pikachu 2 steps forward over a pichu or pikachu
def pikachu_move7(board,current,N,player):
    row,col=current
    if player=='w':
        row=row+2
    else:
        row=row-2
    if row < N and row>=0:
        if board[row][col]=='.':
            return (row,col)
        else:
            return None
    else:
        return None

#Move Pikachu 3 steps forward over a pichu or pikachu
def pikachu_move8(board,current,N,player):
    row,col=current
    if player=='w':
        row=row+3
    else:
        row=row-3
    if row<N and row>=0:
        if board[row][col]=='.' and board[row-2][col]=='.':
            return (row,col)
        else:
            return None
    else:
        return None

#Move Pikachu 2 steps right over a pichu or pikachu
def pikachu_move9(board,current,N,player):
    row,col=current
    if player=='w':
        col=col+2
    else:
        col=col+2
    if col<N and col>=0:
        if board[row][col]=='.':
            return (row,col)
        else:
            return None
    else:
        return None

#Move Pikachu 3 steps right over a pichu or pikachu
def pikachu_move10(board,current,N,player):
    row,col=current
    if player=='w':
        col=col+3
    else:
        col=col+3
    if col<N and col>=0:
        if board[row][col]=='.':
            return (row,col)
        else:
            return None
    else:
        return None

#Move Pikachu 2 steps left over a pichu or pikachu
def pikachu_move11(board,current,N,player):
    row,col=current
    if player=='w':
        col=col-2
    else:
        col=col-2
    if col < N and col >=0:
        if board[row][col]=='.':
            return (row,col)
        else:
            return None
    else:
        return None


#Move Pikachu 3 steps left over a pichu or pikachu
def pikachu_move12(board,current,N,player):
    row,col=current
    if player=='w':
        col=col-3
    else:
        col=col-3
    if col < N and col >=0:
        if board[row][col]=='.':
            return (row,col)
        else:
            return None
    else:
        return None


def raichu_move_fb(board,current,N,player):
    moves=[]
    row,col=current
    initial_r=row
    while row<N or initial_r>=0:
        if player=='w':
            opp='bB$'
        else:
            opp='wW@'
        row=row+1
        initial_r=initial_r-1
        if row < N:
            if(board[row][col]=='.'):
                moves.append(((row,col),'ne'))
            elif board[row][col] in opp:
                if row + 1 < N:
                    if board[row+1][col] in '.':
                        moves.append(((row+1,col),'fe'))
                        break
                    else:
                        pass
            else:
                moves.append((None,None))
                break
        if initial_r>=0:
            if board[initial_r][col]=='.':
                moves.append(((initial_r,col),'ne'))
            elif board[initial_r][col] in opp:
                if initial_r-1>=0:
                    if board[initial_r-1][col] in '.':
                        moves.append(((initial_r-1,col),'be'))
                        break
                    else:
                        pass
            else:
                moves.append((None,None))
                break

    return moves

def raichu_move_lr(board,current,N,player):
    moves=[]
    row,col=current
    initial_c=col
    while col<N or initial_c>=0:
        if player=='w':
            opp='bB$'
        else:
            opp='wW@'
        col=col+1
        initial_c=initial_c-1
        if col < N:
            if(board[row][col]=='.'):
                moves.append(((row,col),'ne'))
            elif board[row][col] in opp:
                if col + 1 < N:
                    if board[row][col+1] in '.':
                        moves.append(((row,col+1),'re'))
                        break
                    else:
                        break

            else:
                moves.append((None,None))
                break
        if initial_c>=0:
            if board[row][initial_c]=='.':
                moves.append(((row,initial_c),'ne'))
            elif board[row][initial_c] in opp:
                if initial_c-1>=0:
                    if board[row][initial_c-1] in '.':
                        moves.append(((row,initial_c-1),'le'))
                        break
                    else:
                        pass
            else:
                moves.append((None,None))
                break
    return moves

def raichu_move_diag(board,current,N,player):
    row,col=current
    moves=[]
    ir,ic=row,col
    if player=='w':
        opp='bB$'
    else:
        opp='wW@'

    #Move Raichu Bottom Right
    while ir < N and ic < N:
        ir=ir+1
        ic=ic+1
        if ir<N and ic< N:
            if board[ir][ic]=='.':
                moves.append(((ir,ic),'ne'))
            elif board[ir][ic] in opp:
                if ir+1 < N and ic+1 < N:
                    if board[ir+1][ic+1] in '.':
                        moves.append(((ir+1,ic+1),'bre'))
                        break
                    else:
                        pass
            else:
                moves.append((None,None))
                break
    ir,ic=row,col
    #Move Raichu Bottom left
    while ir < N and ic >= 0:
        ir=ir+1
        ic=ic-1
        if ir<N and ic>= 0:
            if board[ir][ic]=='.':
                moves.append(((ir,ic),'ne'))
            elif board[ir][ic] in opp:
                if ir+1 < N and ic-1 >= 0:
                    if board[ir+1][ic-1] in '.':
                        moves.append(((ir+1,ic-1),'ble'))
                        break
                    else:
                        pass
            else:
                moves.append((None,None))
                break
    ir,ic=row,col
    #Move Raichu Top Right
    while ir >=0 and ic < N:
        ir=ir-1
        ic=ic+1
        if ir>=0 and ic< N:
            if board[ir][ic]=='.':
                moves.append(((ir,ic),'ne'))
            elif board[ir][ic] in opp:
                if ir-1 < N and ic+1 < N:
                    if board[ir-1][ic+1] in '.':
                        moves.append(((ir-1,ic+1),'tre'))
                        break
                    else:
                        pass
            else:
                moves.append((None,None))
                break
    ir,ic=row,col
    #Move Raichu Top Left
    while ir >= 0 and ic >= 0:
        ir=ir-1
        ic=ic-1
        if ir>=0 and ic>=0:
            if board[ir][ic]=='.':
                moves.append(((ir,ic),'ne'))
            elif board[ir][ic] in opp:
                if ir-1>=0 and ic-1>=0:
                    if board[ir-1][ic-1] in '.':
                        moves.append(((ir-1,ic-1),'tle'))
                        break
                    else:
                        pass
            else:
                moves.append((None,None))
                break
    return moves


def moves_pikachu(board,current,N,player):
    moves=[]
    r,c=current
    moves.append((pikachu_move1(board,current,N,player),1))
    moves.append((pikachu_move2(board,current,N,player),2))
    moves.append((pikachu_move3(board,current,N,player),3))
    moves.append((pikachu_move4(board,current,N,player),4))
    moves.append((pikachu_move5(board,current,N,player),5))
    moves.append((pikachu_move6(board,current,N,player),6))
    
    if player=='w':
        opp='bB'
        r=r+1
        if r<N and r>=0:
            if board[r][c] in opp:
                moves.append((pikachu_move7(board,current,N,player),7))
    r,c=current
    if player=='b':
        opp='wW'
        r=r-1
        if r<N and r>=0:
            if board[r][c] in opp:
                moves.append((pikachu_move7(board,current,N,player),7))
    
    r,c=current
    if player=='w':
        opp='bB'
        r=r+2
        if r<N and r>=0:
            if board[r][c] in opp:
                moves.append((pikachu_move8(board,current,N,player),8))
    r,c=current
    if player=='b':
        opp='wW'
        r=r-2
        if r<N and r>=0:
            if board[r][c] in opp:
                moves.append((pikachu_move8(board,current,N,player),8))

    r,c=current
    if player=='w':
        opp='bB'
        c=c+1
        if c<N and c>=0:
            if board[r][c] in opp:
                moves.append((pikachu_move9(board,current,N,player),9))
        r,c=current
    if player=='b':
        opp='wW'
        c=c+1
        if c<N and c>=0:
            if board[r][c] in opp:
                moves.append((pikachu_move9(board,current,N,player),9))

    r,c=current
    if player=='w':
        opp='bB'
        c=c+2
        if c<N and c>=0:
            if board[r][c] in opp:
                moves.append((pikachu_move10(board,current,N,player),10))
    r,c=current
    if player=='b':
        opp='wW'
        c=c+2
        if c<N and c>=0:
            if board[r][c] in opp:
                moves.append((pikachu_move10(board,current,N,player),10))

    r,c=current
    if player=='w':
        opp='bB'
        c=c-1
        if c<N and c>=0:
            if board[r][c] in opp:
                moves.append((pikachu_move11(board,current,N,player),11))
    r,c=current
    if player=='b':
        opp='wW'
        c=c-1
        if c<N and c>=0:
            if board[r][c] in opp:
                moves.append((pikachu_move11(board,current,N,player),11))
    

    r,c=current
    if player=='w':
        opp='bB'
        c=c-2
        if c<N and c>=0:
            if board[r][c] in opp:
                moves.append((pikachu_move12(board,current,N,player),12))
    r,c=current
    if player=='b':
        opp='wW'
        c=c-2
        if c<N and c>=0:
            if board[r][c] in opp:
                moves.append((pikachu_move12(board,current,N,player),12))
    
    moves= list(filter(lambda x: x[0] is not None, moves))
    #print(moves)
    return moves
   
def moves_raichu(board,current,N,player):
    moves=[]
    for i,j in raichu_move_fb(board,current,N,player):
        moves.append((i,j))

    for i,j in raichu_move_lr(board,current,N,player):
        moves.append((i,j))
    for i,j in raichu_move_diag(board,current,N,player):
        moves.append((i,j))
    moves= list(filter(lambda x: x[0] is not None, moves))
    return moves



def convert_board(board,N):
    result=[]
    counter=0
    for i in range(N):
        temp=[]
        for j in range(N):
            temp.append(board[counter])
            counter+=1
        result.append(temp)
    return result

def find_pichus(board,N):
    positionsW=[(i//N,i%N) for i in range(len(board)) if board[i] == 'w']
    positionsB=[(i//N,i%N) for i in range(len(board)) if board[i] == 'b']
    return positionsW,positionsB

def find_pikachus(board,N):
    positionsW=[(i//N,i%N) for i in range(len(board)) if board[i] == 'W']
    positionsB=[(i//N,i%N) for i in range(len(board)) if board[i] == 'B']
    return positionsW,positionsB

def find_raichus(board,N):
    positionsW=[(i//N,i%N) for i in range(len(board)) if board[i] == '@']
    positionsB=[(i//N,i%N) for i in range(len(board)) if board[i] == '$']
    return positionsW,positionsB

def successors(board,player,N):
    succ=[]
    pichusW,pichusB=find_pichus(board,N)
    pikachusW,pikachusB=find_pikachus(board,N)
    raichusW,raichusB=find_raichus(board,N)
    board_2d=convert_board(board,N)
    if player=='w':
        for i in pichusW:
            moves=move_pichu(board_2d,i,N,player)
            
            for j,k in moves:
                new_board=deepcopy(board_2d)
                #print(j)
                #print(k)
                if(j[0]==N-1):
                    new_board[i[0]][i[1]]= '.'
                    new_board[j[0]][j[1]]= '@'
                else:
                    current_piece=board_2d[i[0]][i[1]]
                    if k==3:
                        new_board[i[0]][i[1]]= '.'
                        new_board[j[0]][j[1]]= current_piece
                        new_board[i[0]+1][i[1]-1]='.'
                    elif k==4:
                        new_board[i[0]][i[1]]= '.'
                        new_board[j[0]][j[1]]= current_piece
                        new_board[i[0]+1][i[1]+1]='.'
                    else:
                        new_board[i[0]][i[1]]= '.'
                        new_board[j[0]][j[1]]= current_piece

                succ.append(new_board)
        
        for i in pikachusW:
            moves=moves_pikachu(board_2d,i,N,player)
            
            for j,k in moves:
                new_board=deepcopy(board_2d)
                if(j[0]==N-1):
                    new_board[i[0]][i[1]]= '.'
                    new_board[j[0]][j[1]]= '@'
                else:
                    current_piece=board_2d[i[0]][i[1]]
                    if k==7:
                        new_board[i[0]][i[1]]= '.'
                        new_board[j[0]][j[1]]= current_piece
                        new_board[i[0]+1][i[1]]='.'
                    elif k==8:
                        new_board[i[0]][i[1]]= '.'
                        new_board[j[0]][j[1]]= current_piece
                        new_board[i[0]+2][i[1]]='.'
                    elif k==9:
                        new_board[i[0]][i[1]]= '.'
                        new_board[j[0]][j[1]]= current_piece
                        new_board[i[0]][i[1]+1]='.'
                    elif k==10:
                        new_board[i[0]][i[1]]= '.'
                        new_board[j[0]][j[1]]= current_piece
                        new_board[i[0]][i[1]+2]='.'
                    elif k==11:
                        new_board[i[0]][i[1]]= '.'
                        new_board[j[0]][j[1]]= current_piece
                        new_board[i[0]][i[1]-1]='.'
                    elif k==12:
                        new_board[i[0]][i[1]]= '.'
                        new_board[j[0]][j[1]]= current_piece
                        new_board[i[0]][i[1]-2]='.'
                    else:
                        new_board[i[0]][i[1]]= '.'
                        new_board[j[0]][j[1]]= current_piece
                succ.append(new_board)
        
        for i in raichusW:
            moves=moves_raichu(board_2d,i,N,player)
            for j,k in moves:
                new_board=deepcopy(board_2d)
                if(k=='ne'):
                    current_piece=board_2d[i[0]][i[1]]
                    new_board[i[0]][i[1]]= '.'
                    new_board[j[0]][j[1]]= current_piece
                elif(k=='bre'):
                    current_piece=board_2d[i[0]][i[1]]
                    new_board[i[0]][i[1]]= '.'
                    new_board[j[0]][j[1]]= current_piece
                    new_board[j[0]-1][j[1]-1]='.'
                elif(k=='tle'):
                    current_piece=board_2d[i[0]][i[1]]
                    new_board[i[0]][i[1]]= '.'
                    new_board[j[0]][j[1]]= current_piece
                    new_board[j[0]+1][j[1]+1]='.'
                elif(k=='tre'):
                    current_piece=board_2d[i[0]][i[1]]
                    new_board[i[0]][i[1]]= '.'
                    new_board[j[0]][j[1]]= current_piece
                    new_board[j[0]+1][j[1]-1]='.'
                elif(k=='ble'):
                    current_piece=board_2d[i[0]][i[1]]
                    new_board[i[0]][i[1]]= '.'
                    new_board[j[0]][j[1]]= current_piece
                    new_board[j[0]-1][j[1]+1]='.'
                elif(k=='fe'):
                    current_piece=board_2d[i[0]][i[1]]
                    new_board[i[0]][i[1]]= '.'
                    new_board[j[0]][j[1]]= current_piece
                    new_board[j[0]-1][j[1]]='.'
                elif(k=='be'):
                    current_piece=board_2d[i[0]][i[1]]
                    new_board[i[0]][i[1]]= '.'
                    new_board[j[0]][j[1]]= current_piece
                    new_board[j[0]+1][j[1]]='.'
                elif(k=='re'):
                    current_piece=board_2d[i[0]][i[1]]
                    new_board[i[0]][i[1]]= '.'
                    new_board[j[0]][j[1]]= current_piece
                    new_board[j[0]][j[1]-1]='.'
                elif(k=='le'):
                    current_piece=board_2d[i[0]][i[1]]
                    new_board[i[0]][i[1]]= '.'
                    new_board[j[0]][j[1]]= current_piece
                    new_board[j[0]][j[1]+1]='.'
                succ.append(new_board)
    else:
        for i in pichusB:
            moves=move_pichu(board_2d,i,N,player)
            
            for j,k in moves:

                new_board=deepcopy(board_2d)
                if(j[0]==0):
                    new_board[i[0]][i[1]]= '.'
                    new_board[j[0]][j[1]]= '$'
                else:
                    current_piece=board_2d[i[0]][i[1]]
                    if k==3:
                        new_board[i[0]][i[1]]= '.'
                        new_board[j[0]][j[1]]= current_piece
                        new_board[i[0]-1][i[1]-1]='.'
                    elif k==4:
                        new_board[i[0]][i[1]]= '.'
                        new_board[j[0]][j[1]]= current_piece
                        new_board[i[0]-1][i[1]+1]='.'
                    else:
                        new_board[i[0]][i[1]]= '.'
                        new_board[j[0]][j[1]]= current_piece
                succ.append(new_board)
        
        for i in pikachusB:
            moves=moves_pikachu(board_2d,i,N,player)
            
            for j,k in moves:
                new_board=deepcopy(board_2d)
                if(j[0]==0):
                    new_board[i[0]][i[1]]= '.'
                    new_board[j[0]][j[1]]= '$'
                else:
                    current_piece=board_2d[i[0]][i[1]]
                    if k==7:
                        new_board[i[0]][i[1]]= '.'
                        new_board[j[0]][j[1]]= current_piece
                        new_board[i[0]-1][i[1]]='.'
                    elif k==8:
                        new_board[i[0]][i[1]]= '.'
                        new_board[j[0]][j[1]]= current_piece
                        new_board[i[0]-2][i[1]]='.'
                    elif k==9:
                        new_board[i[0]][i[1]]= '.'
                        new_board[j[0]][j[1]]= current_piece
                        new_board[i[0]][i[1]+1]='.'
                    elif k==10:
                        new_board[i[0]][i[1]]= '.'
                        new_board[j[0]][j[1]]= current_piece
                        new_board[i[0]][i[1]+2]='.'
                    elif k==11:
                        new_board[i[0]][i[1]]= '.'
                        new_board[j[0]][j[1]]= current_piece
                        new_board[i[0]][i[1]-1]='.'
                    elif k==12:
                        new_board[i[0]][i[1]]= '.'
                        new_board[j[0]][j[1]]= current_piece
                        new_board[i[0]][i[1]-2]='.'
                    else:
                        new_board[i[0]][i[1]]= '.'
                        new_board[j[0]][j[1]]= current_piece              
                succ.append(new_board)
        
        for i in raichusB:
            moves=moves_raichu(board_2d,i,N,player)
            new_board=deepcopy(board_2d)
            for j,k in moves:
                new_board=deepcopy(board_2d)
                if(k=='ne'):
                    current_piece=board_2d[i[0]][i[1]]
                    new_board[i[0]][i[1]]= '.'
                    new_board[j[0]][j[1]]= current_piece
                elif(k=='bre'):
                    current_piece=board_2d[i[0]][i[1]]
                    new_board[i[0]][i[1]]= '.'
                    new_board[j[0]][j[1]]= current_piece
                    new_board[j[0]-1][j[1]-1]='.'
                elif(k=='tle'):
                    current_piece=board_2d[i[0]][i[1]]
                    new_board[i[0]][i[1]]= '.'
                    new_board[j[0]][j[1]]= current_piece
                    new_board[j[0]+1][j[1]+1]='.'
                elif(k=='tre'):
                    current_piece=board_2d[i[0]][i[1]]
                    new_board[i[0]][i[1]]= '.'
                    new_board[j[0]][j[1]]= current_piece
                    new_board[j[0]+1][j[1]-1]='.'
                elif(k=='ble'):
                    current_piece=board_2d[i[0]][i[1]]
                    new_board[i[0]][i[1]]= '.'
                    new_board[j[0]][j[1]]= current_piece
                    new_board[j[0]-1][j[1]+1]='.'
                elif(k=='fe'):
                    current_piece=board_2d[i[0]][i[1]]
                    new_board[i[0]][i[1]]= '.'
                    new_board[j[0]][j[1]]= current_piece
                    new_board[j[0]-1][j[1]]='.'
                elif(k=='be'):
                    current_piece=board_2d[i[0]][i[1]]
                    new_board[i[0]][i[1]]= '.'
                    new_board[j[0]][j[1]]= current_piece
                    new_board[j[0]+1][j[1]]='.'
                elif(k=='re'):
                    current_piece=board_2d[i[0]][i[1]]
                    new_board[i[0]][i[1]]= '.'
                    new_board[j[0]][j[1]]= current_piece
                    new_board[j[0]][j[1]-1]='.'
                elif(k=='le'):
                    current_piece=board_2d[i[0]][i[1]]
                    new_board[i[0]][i[1]]= '.'
                    new_board[j[0]][j[1]]= current_piece
                    new_board[j[0]][j[1]+1]='.'
                succ.append(new_board)
    #print(succ)

    return succ


def termin_criteria(board,player):
    if count_white(board)==0 and player=='b':
        return True
    if count_black(board)==0 and player=='w':
        return True
    return False


def minimax(board,depth,a,b,player,N):
    t1=convert_board(board,N)
    bestBoard=board
    if depth==0 or termin_criteria(board,player):
        return (board,evaluate(board,player))

    if player=='w':
        maxEval=-math.inf
        #a=-math.inf
        for i in successors(board,player,N):
            ev= minimax(convert_board_to_string(i),depth-1,a,b,'b',N)
            maxEval=max(maxEval,ev[1])
            temp=a
            a=max(a,ev[1])
            if(b<=a):
                break
            if(a!=temp):
                bestBoard=i
        return (bestBoard,maxEval)
    else:
        minEval= math.inf
        #b=math.inf
        for i in successors(board,player,N):
            ev=minimax(convert_board_to_string(i),depth-1,a,b,'w',N)
            minEval=min(minEval,ev[1])
            temp=b
            b=min(b,ev[1])
            if(b<=a):
                break
            if(b!=temp):
                bestBoard=i
            
        return (bestBoard,minEval)


def convert_board_to_string(board):
    result=''
    for i in board:
        for j in i:
            result=result+j
    return result

def find_best_move(board, N, player, timelimit):
    # This sample code just returns the same board over and over again (which
    # isn't a valid move anyway.) Replace this with your code!
    board_2d=convert_board(board,N)
    count=1
    oppPlayer='b'
    #temp=successors(board,player,N)
    #for i in temp:
    #    print("Successor "+str(count))
    #    print(np.asarray(i))
    #    print()
    #    count+=1
    t0=time.time()
    ev=minimax(board,4,-99999,99999,'w',N)
    t1=time.time()
    print(str(t1-t0)+" seconds")
    print(np.array(ev[0]))
    
    yield convert_board_to_string(ev[0])
        

        
            

    #print(pichusW)
    #print(pichusB)
    #pikachus=find_pikachus(board)
    #print(board_2d)



if __name__ == "__main__":
    if len(sys.argv) != 5:
      raise Exception("Usage: Raichu.py N player board timelimit")
        
    (_, N, player, board, timelimit) = sys.argv
    #N=8
    #player='w'
    #board='..........................................................@.$@@.'
    #board='........W.W.W.W........w.B...........w.bb.w...B..B..B.......@...'
    #board='...$..........W..WW.Wb....w......w.b....b........B..BB......@...'
    #board='....................$..b.........b.b.BWB......w.b.WwBW..........'
    #board='........W...W.W...W.....w...b.w....B....b...w.b..B...B.B........'
    #board='........W.W.W.W..w.w.w.w................b.b.b.b..B.B.B.B........'
    #board='........W.W.W.W..w.w.w.w................b.b.b.b..B.B.B.B........'
    #board='........W.W.W.W....w.w.ww............B..b.b.b.b..B.B...B........'
    #board='.................W.W.W.Wb.b.b.b..B.B.B.B........................'
    #board= '.........W.w.@.w.w.w.b.b.b.b....................................'
    timelimit=10
    N=int(N)
    timelimit=int(timelimit)
    if player not in "wb":
        raise Exception("Invalid player.")

    if len(board) != N*N or 0 in [c in "wb.WB@$" for c in board]:
        raise Exception("Bad board string.")

    print("Searching for best move for " + player + " from board state: \n" + board_to_string(board, N))
    print("Here's what I decided:")
    for new_board in find_best_move(board, N, player, timelimit):
        print(new_board)


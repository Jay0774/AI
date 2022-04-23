# importing important libraries
import tensorflow.compat.v1 as tf
tf.disable_v2_behavior()
import numpy as np
from copy import deepcopy
import random 
import math
import pandas as pd
import time
import matplotlib.pyplot as plt
import matplotlib
matplotlib.use('Agg')
# tkinter is used for displaying the output
from tkinter import *
from game import *

# initializing a new game peroid
# here n is number of rows and columns
def new_game_board(n):
    matrix = np.zeros([n,n])
    return matrix

# now adding 2 or 4 element in the matrix
def put_two_four(mat):
    empty_cells = []
    for i in range(len(mat)):
        for j in range(len(mat[0])):
            if(mat[i][j]==0):
                empty_cells.append((i,j))
    if(len(empty_cells)==0):
        return mat
    index_pair = empty_cells[random.randint(0,len(empty_cells)-1)]
    prob = random.random()
    if(prob>=0.9):
        mat[index_pair[0]][index_pair[1]]=4
    else:
        mat[index_pair[0]][index_pair[1]]=2
    return mat

# check the state of the game
def state_of_game(mat):
    #   if 2048 element present in mat:
    #    return 'win'
    
    for i in range(len(mat)-1): #intentionally reduced to check the row on the move_right and below
        for j in range(len(mat[0])-1): #more elegant to use exceptions but most likely this will be their solution
            if mat[i][j]==mat[i+1][j] or mat[i][j+1]==mat[i][j]:
                return 'not over'
            
    for i in range(len(mat)): #check for any zero entries
        for j in range(len(mat[0])):
            if mat[i][j]==0:
                return 'not over'
            
    for k in range(len(mat)-1): #to check the move_left/move_right entries on the last row
        if mat[len(mat)-1][k]==mat[len(mat)-1][k+1]:
            return 'not over'
        
    for j in range(len(mat)-1): #check move_up/move_down entries on last column
        if mat[j][len(mat)-1]==mat[j+1][len(mat)-1]:
            return 'not over'
        
    return 'lose'

# reversing the matrix
def reverse_matrix(mat):
    new=[]
    for i in range(len(mat)):
        new.append([])
        for j in range(len(mat[0])):
            new[i].append(mat[i][len(mat[0])-j-1])
    return new
# trasnsposing the matrix
def transpose_matrix(mat):
    new=[]
    for i in range(len(mat[0])):
        new.append([])
        for j in range(len(mat)):
            new[i].append(mat[j][i])
            
    return np.transpose(mat)

# cover move_up matrix
def new_cover(mat):
    new = [[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0]]
    done = False
    for i in range(4):
        count = 0
        for j in range(4):
            if mat[i][j]!=0:
                new[i][count] = mat[i][j]
                if j!=count:
                    done=True
                count+=1
    return (new,done)

# merge_matrix two matrices 
def merge_matrix(mat):
    done=False
    score = 0
    for i in range(4):
        for j in range(3):
            if mat[i][j]==mat[i][j+1] and mat[i][j]!=0:
                mat[i][j]*=2
                score += mat[i][j]   
                mat[i][j+1]=0
                done=True
    return (mat,done,score)

# game move_up move
def move_up(game):
        game = transpose_matrix(game)
        game,done = new_cover(game)
        temp = merge_matrix(game)
        game = temp[0]
        done = done or temp[1]
        game = new_cover(game)[0]
        game = transpose_matrix(game)
        return (game,done,temp[2])

# game move_down move
def move_down(game):
        game=reverse_matrix(transpose_matrix(game))
        game,done=new_cover(game)
        temp=merge_matrix(game)
        game=temp[0]
        done=done or temp[1]
        game=new_cover(game)[0]
        game=transpose_matrix(reverse_matrix(game))
        return (game,done,temp[2])

# game move_left move
def move_left(game):
        game,done=new_cover(game)
        temp=merge_matrix(game)
        game=temp[0]
        done=done or temp[1]
        game=new_cover(game)[0]
        return (game,done,temp[2])

#game move_right move
def move_right(game):
        game=reverse_matrix(game)
        game,done=new_cover(game)
        temp=merge_matrix(game)
        game=temp[0]
        done=done or temp[1]
        game=new_cover(game)[0]
        game=reverse_matrix(game)
        return (game,done,temp[2])

# defining the controls and their index values
controls = {0:move_up,1:move_left,2:move_right,3:move_down}

# converting the input game matrix into corresponding power of 2 matrix to get the reward.
def change_values_of_matrice(X):
    power_mat = np.zeros(shape=(1,4,4,16),dtype=np.float32)
    for i in range(4):
        for j in range(4):
            if(X[i][j]==0):
                power_mat[0][i][j][0] = 1.0
            else:
                power = int(math.log(X[i][j],2))
                power_mat[0][i][j][power] = 1.0
    return power_mat        

# finding the number of empty cells in the game matrix.
def find_empty_Cell(mat):
    count = 0
    for i in range(len(mat)):
        for j in range(len(mat)):
            if(mat[i][j]==0):
                count+=1
    return count

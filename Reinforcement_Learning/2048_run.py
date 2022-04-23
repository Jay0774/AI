# importing required libraries
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

# convolution layer1 depth
depth1 = 128

# convolution layer2 depth
depth2 = 128

# input depth
input_depth = 16

# fully conneted hidden layer
hidden_units = 256

# output layer
output_units = 4

# shape of weights
conv1_layer1_shape = [2,1,input_depth,depth1]
conv1_layer2_shape = [2,1,depth1,depth2]
conv2_layer1_shape = [1,2,input_depth,depth1]
conv2_layer2_shape = [1,2,depth1,depth2]

fc_layer1_w_shape = [3*4*depth1*2+ 4*2*depth2*2 + 3*3*depth2*2,hidden_units]
fc_layer1_b_shape = [hidden_units]
fc_layer2_w_shape = [hidden_units,output_units]
fc_layer2_b_shape = [output_units]

# loading the parameters trained before
parameters = {}
path = r'FinalWeights'
parameters['conv1_layer1'] = np.array(pd.read_csv(path + r'\conv1_layer1_weights.csv')['Weight']).reshape(conv1_layer1_shape)
parameters['conv1_layer2'] = np.array(pd.read_csv(path + r'\conv1_layer2_weights.csv')['Weight']).reshape(conv1_layer2_shape)
parameters['conv2_layer1'] = np.array(pd.read_csv(path + r'\conv2_layer1_weights.csv')['Weight']).reshape(conv2_layer1_shape)
parameters['conv2_layer2'] = np.array(pd.read_csv(path + r'\conv2_layer2_weights.csv')['Weight']).reshape(conv2_layer2_shape)
parameters['fc_layer1_w'] = np.array(pd.read_csv(path + r'\fc_layer1_weights.csv')['Weight']).reshape(fc_layer1_w_shape)
parameters['fc_layer1_b'] = np.array(pd.read_csv(path + r'\fc_layer1_biases.csv')['Weight']).reshape(fc_layer1_b_shape)
parameters['fc_layer2_w'] = np.array(pd.read_csv(path + r'\fc_layer2_weights.csv')['Weight']).reshape(fc_layer2_w_shape)
parameters['fc_layer2_b'] = np.array(pd.read_csv(path + r'\fc_layer2_biases.csv')['Weight']).reshape(fc_layer2_b_shape)

# learned graph using tensorflow
learned_graph = tf.Graph()

# creating the model for testing the output
with learned_graph.as_default():
    #input data
    single_dataset = tf.placeholder(tf.float32,shape=(1,4,4,16))

    #weights    
    #conv layer1 weights
    conv1_layer1_weights = tf.constant(parameters['conv1_layer1'],dtype=tf.float32)
    conv1_layer2_weights = tf.constant(parameters['conv1_layer2'],dtype=tf.float32)
    
    #conv layer2 weights
    conv2_layer1_weights = tf.constant(parameters['conv2_layer1'],dtype=tf.float32)
    conv2_layer2_weights = tf.constant(parameters['conv2_layer2'],dtype=tf.float32)
    
    #fully connected parameters
    fc_layer1_weights = tf.constant(parameters['fc_layer1_w'],dtype=tf.float32)
    fc_layer1_biases = tf.constant(parameters['fc_layer1_b'],dtype=tf.float32)
    fc_layer2_weights = tf.constant(parameters['fc_layer2_w'],dtype=tf.float32)
    fc_layer2_biases = tf.constant(parameters['fc_layer2_b'],dtype=tf.float32)
    
    
    # model defination
    def model(dataset):
        # layer1
        conv1 = tf.nn.conv2d(dataset,conv1_layer1_weights,[1,1,1,1],padding='VALID') 
        conv2 = tf.nn.conv2d(dataset,conv2_layer1_weights,[1,1,1,1],padding='VALID') 

        # layer1 relu activation
        relu1 = tf.nn.relu(conv1)
        relu2 = tf.nn.relu(conv2)

        # layer2
        conv11 = tf.nn.conv2d(relu1,conv1_layer2_weights,[1,1,1,1],padding='VALID') 
        conv12 = tf.nn.conv2d(relu1,conv2_layer2_weights,[1,1,1,1],padding='VALID') 

        conv21 = tf.nn.conv2d(relu2,conv1_layer2_weights,[1,1,1,1],padding='VALID') 
        conv22 = tf.nn.conv2d(relu2,conv2_layer2_weights,[1,1,1,1],padding='VALID') 

        # layer2 relu activation
        relu11 = tf.nn.relu(conv11)
        relu12 = tf.nn.relu(conv12)
        relu21 = tf.nn.relu(conv21)
        relu22 = tf.nn.relu(conv22)

        # get shapes of all activations
        shape1 = relu1.get_shape().as_list()
        shape2 = relu2.get_shape().as_list()

        shape11 = relu11.get_shape().as_list()
        shape12 = relu12.get_shape().as_list()
        shape21 = relu21.get_shape().as_list()
        shape22 = relu22.get_shape().as_list()

        # expansion of layers
        hidden1 = tf.reshape(relu1,[shape1[0],shape1[1]*shape1[2]*shape1[3]])
        hidden2 = tf.reshape(relu2,[shape2[0],shape2[1]*shape2[2]*shape2[3]])

        hidden11 = tf.reshape(relu11,[shape11[0],shape11[1]*shape11[2]*shape11[3]])
        hidden12 = tf.reshape(relu12,[shape12[0],shape12[1]*shape12[2]*shape12[3]])
        hidden21 = tf.reshape(relu21,[shape21[0],shape21[1]*shape21[2]*shape21[3]])
        hidden22 = tf.reshape(relu22,[shape22[0],shape22[1]*shape22[2]*shape22[3]])

        # concatenation of layers
        hidden = tf.concat([hidden1,hidden2,hidden11,hidden12,hidden21,hidden22],axis=1)

        # full connected layers
        hidden = tf.matmul(hidden,fc_layer1_weights) + fc_layer1_biases
        hidden = tf.nn.relu(hidden)

        # output layers
        output = tf.matmul(hidden,fc_layer2_weights) + fc_layer2_biases

        # returning the output
        return output

    # testing for single example
    single_output = model(single_dataset)


# defining the display parameters of the grid 
SIZE = 10000
GRID_LEN = 4
GRID_PADDING = 15

# setting the background color of the game screen
BACKGROUND_COLOR_GAME = "#0e1714"
# setting the color of the empty cell
BACKGROUND_COLOR_CELL_EMPTY = "#73714d"
# setting the colors of different numbers
BACKGROUND_COLOR_DICT = {   2:"#eee4da", 4:"#ede0c8", 8:"#f2b179", 16:"#f59563", \
                            32:"#f67c5f", 64:"#f65e3b", 128:"#edcf72", 256:"#edcc61", \
                            512:"#edc850", 1024:"#edc53f", 2048:"#edc22e" }
# setting the color of different color cells
CELL_COLOR_DICT = { 2:"#776e65", 4:"#776e65", 8:"#f9f6f2", 16:"#f9f6f2", \
                    32:"#f9f6f2", 64:"#f9f6f2", 128:"#f9f6f2", 256:"#f9f6f2", \
                    512:"#f9f6f2", 1024:"#f9f6f2", 2048:"#f9f6f2" }

# strating the session
learned_sess = tf.Session(graph=learned_graph)

# setting the font
FONT = ("Verdana", 40, "bold")

# making a class to display the gameplay grid
class GameGrid(Frame):
    # defning the constructor
    def __init__(self):
        # creating a tkinter frame oject
        Frame.__init__(self)
        # setting up the grid values
        self.grid()
        self.master.title('2048-Game-Play-After-Training')
        self.grid_cells = []
        self.init_grid()
        self.init_matrix()
        self.update_grid_cells()
        self.wait_visibility()
        self.after(10,self.make_move)
    
    # initializing the grid
    def init_grid(self):
        # creating a background
        background = Frame(self, bg=BACKGROUND_COLOR_GAME, width=SIZE, height=SIZE)
        # creating grid
        background.grid()
        for i in range(GRID_LEN):
            grid_row = []
            for j in range(GRID_LEN):
                # entering cells
                cell = Frame(background, bg=BACKGROUND_COLOR_CELL_EMPTY, width=SIZE/GRID_LEN, height=SIZE/GRID_LEN)
                cell.grid(row=i, column=j, padx=GRID_PADDING, pady=GRID_PADDING)
                # font = Font(size=FONT_SIZE, family=FONT_FAMILY, weight=FONT_WEIGHT)
                t = Label(master=cell, text="", bg=BACKGROUND_COLOR_CELL_EMPTY, justify=CENTER, font=FONT, width=4, height=2)
                t.grid()
                grid_row.append(t)
            self.grid_cells.append(grid_row)

    # generating a random element
    def gen(self):
        return randint(0, GRID_LEN - 1)
    # initializing the matix
    def init_matrix(self):
        self.matrix = new_game_board(4)
        self.matrix=put_two_four(self.matrix)
        self.matrix=put_two_four(self.matrix)
    # updating the cells
    def update_grid_cells(self):
        for i in range(GRID_LEN):
            for j in range(GRID_LEN):
                new_number = self.matrix[i][j]
                if new_number == 0:
                    self.grid_cells[i][j].configure(text="", bg=BACKGROUND_COLOR_CELL_EMPTY)
                else:
                    self.grid_cells[i][j].configure(text=str(new_number), bg=BACKGROUND_COLOR_DICT[new_number], fg=CELL_COLOR_DICT[new_number])
        self.update_idletasks()
    # making a move
    def make_move(self):
        output = learned_sess.run([single_output],feed_dict = {single_dataset:change_values_of_matrice(self.matrix)})
        move = np.argmax(output[0])
        self.matrix,done,tempo = controls[move](self.matrix)
        done=True
        # checking whether game is lost or win
        if state_of_game(self.matrix)=='lose':
            self.grid_cells[1][1].configure(text="You",bg=BACKGROUND_COLOR_CELL_EMPTY)
            self.grid_cells[1][2].configure(text="Lose!",bg=BACKGROUND_COLOR_CELL_EMPTY)
            done=False
        # setting the values
        self.matrix = put_two_four(self.matrix)
        self.update_grid_cells()
        if(done==True):
            self.after(7,self.make_move)
        else:
            time.sleep(1)
            self.init_matrix()
            self.update_grid_cells()
            self.after(7,self.make_move)
    # generating a next state
    def generate_next(self):
        empty_cells = []
        for i in range(len(mat)):
            for j in range(len(mat)):
                if(mat[i][j]==0):
                    empty_cells.append((i,j))
        if(len(empty_cells)==0):
            return 0,false
        index_pair = empty_cells[random.randint(0,len(empty_cells)-1)]
        index = index_pair
        self.matrix[index[0]][index[1]] = 2

# starting the game in a loop
root = Tk()
gamegrid = GameGrid()
root.mainloop()
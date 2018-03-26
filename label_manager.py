''' This class will keep track of the checkpoint and win labels for each car.
Created Fall 2014
label_manager.py
@author: Jonathan Manni (jdm42)
'''

from tkinter import *

class Labels:
    def __init__(self, map, car):
        self.canvas = map.canvas # set the canvas to use
        self.canvas_width = map.getWidth() # get the width of the canvas
        self.canvas_height = map.getHeight() # get the height of the canvas
        self.color = car.color # set a global color variable to the color of the car
        self.number = car.number # set a global number variable to the number of the car
        self.win_printed = False # set a variable that indicates if the win screen has been printed
        self.checkpoint_printed = False # set a variable that indicates if the checkpoint has been printed
        self.winTag = '' # set an empty tag for the win screen
        self.checkTag = '' # set an empty tag for the checkpoint display
        self.scale = map.scale # get the scale from the map and create a global scale variable
        self.font_size = int(self.scale / 3) # set the font size to a third of the scale
        
    def printWin(self):
        '''This function will print the win screen when a car wins.'''
        self.winTag = 'win_label' + str(self.number) # create the win tag
        text = 'Player ' + str(self.number) + ' Wins!!' # set the text for which play won
        # create a stippled background of dark green
        self.canvas.create_rectangle( (0, 0),
                                      (self.canvas_width, self.canvas_height),
                                      fill='#092129', outline='', stipple='gray75')
        # create the text that displays which player won
        self.canvas.create_text((self.canvas_width / 2, self.canvas_height / 2 - self.scale * 3),
                                text=text, font=("Arial", self.font_size * 2), fill='white', tags=self.winTag)
        
    def printCheckpoint(self):
        '''This function displays that a certain car has reached the checkpoint.'''
        self.checkTag = 'check_label' + str(self.number) # create a tag to use to delete the checkpoint label
        text = 'Player ' + str(self.number) + ' reached the checkpoint!!' # creat the text for which player hit the checkpoint

        if self.number == 1: # put the rectangle and text higher if player 1
            # create the background rectangle for the text
            self.canvas.create_rectangle( ((self.canvas_width / 2) - self.font_size * 11, (self.canvas_height / 2) - (self.scale / 2) - (self.scale / 2)),
                                          ((self.canvas_width / 2) + self.font_size * 11, (self.canvas_height / 2) + (self.scale / 2) - (self.scale / 2)),
                                          fill='#b3ecec', outline='', stipple='gray75', tags=self.checkTag)
            # create the text indicating who got the checkpoint
            self.canvas.create_text((self.canvas_width / 2, self.canvas_height / 2 - (self.scale / 2)),
                                    text=text, font=("Arial", self.font_size), fill=self.color, tags=self.checkTag)
        elif self.number == 2: # put the rectangle and text lower if player 2
            # create the background rectangle for the text
            self.canvas.create_rectangle( ((self.canvas_width / 2) - self.font_size * 11, (self.canvas_height / 2) - self.scale / 2 + (self.scale / 2)),
                                          ((self.canvas_width / 2) + self.font_size * 11, (self.canvas_height / 2) + self.scale / 2 + (self.scale / 2)),
                                          fill='#b3ecec', outline='', stipple='gray75', tags=self.checkTag)
            # create the text indicating who got the checkpoint
            self.canvas.create_text((self.canvas_width / 2, self.canvas_height / 2 + (self.scale / 2)),
                                    text=text, font=("Arial", self.font_size), fill=self.color, tags=self.checkTag)    
        self.checkpoint_printed = True # set the checkpoint_printed indicator to True
    
    def deleteCheckpoint(self):
        '''This function will delete the checkpoint banner when called (after the timer has been reached.)'''
        self.canvas.delete(self.checkTag) # delete the rectangle and text for the checkpoint banner  
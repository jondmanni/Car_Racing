''' This class will create the end high score prompts.
Created Fall 2014
saveScore.py
@author: Jonathan Manni (jdm42)
'''

from tkinter import *

class endScore:
    def __init__(self, map, time):
        self.name = StringVar() # initiate a name string variable
        self.time = time # store the win time in a global variable
        self.canvas = map.canvas # create a global canvas variable
        self.scale = int(map.scale) # create a global scale variable
        self.width = map.getWidth() # create a global width variable
        self.height = map.getHeight() # create a global height variable
        self.checkHighScoreBeat() # check if the user beat the high score
        
    def checkHighScoreBeat(self):
        '''This function checks if the current high score was beat, and displays the proper prompt.'''
        if self.getHighScore(self.time) < self.loadHighScore(): # if the user beat the high score
            # create text on the canvas that says "You beat the high score!"
            self.canvas.create_text((self.width / 2, self.height / 2 - self.scale * 2),
                            text='You beat the high score!', font=("Arial", int(self.scale / 3)), fill='white', tags='')
            # create text on the canvas that says "Enter your name below."
            self.canvas.create_text((self.width / 2, self.height / 2 - self.scale * 1.5),
                                text='Enter your name below.', font=("Arial", int(self.scale / 3)), fill='white', tags='save')
            
            entry = Entry(self.canvas, textvariable=self.name) # create an entry field
            submit = Button(self.canvas, text="Submit", command= self.saveScore) # create a submit button
            # put the entry field on the canvas
            self.canvas.create_window((self.width / 2, self.height / 2 - self.scale * 0.75), window=entry, tags='save')
            # put the button on the canvas
            self.canvas.create_window((self.width / 2, self.height / 2), window=submit, tags='save')
        else: # if the user didn't beat the high score
            # create text on the canvas that sayd "You didn't beat the high score."
            self.canvas.create_text((self.width / 2, self.height / 2 - self.scale * 2),
                            text='You didnt beat the high score.', font=("Arial", int(self.scale / 3)), fill='white', tags='')
    
    def loadHighScore(self):
        '''This function will load the high score from file.'''
        file = open('high_score.txt', 'r')
        line = file.readline()
        return self.getHighScore(line) # call the getHighScore function to parse the file
        
    def getHighScore(self, line):
        '''This function will analyze the string in the high_score.txt file and return the score.'''
        time = '' # set a time string to nothing
        for x in line: # go through each character in the line
            if x != ':': # if the character is not a semicolon
                time += x # add that character to the time string
            if x == ' ': # if the character is a space
                break # stop looking through the line
        score = 0 # set a local score variable to zero
        
        #set minute formatting
        if int(time[0]) == 0: # if minutes are less than or equal to 9
            score += int(time[1]) * 60 * 1000 # add only the second minute digit to the score (in milliseconds)
        elif int(time[0]) != 0: # if minutes are greater than 9
            score += int(time[0:2]) * 60 * 1000 # add both minute digits (in milliseconds)
        
        #set second formatting
        if int(time[2]) == 0: # if seconds are less than or equal to 9
            score += int(time[3]) * 1000 # add only the second seconds digit to the score (in ms)
        elif int(time[2]) != 0: # if seconds are greater than 9
            score += int(time[2:4]) * 1000 # add both seconds digits (in ms)
            
        #set millisecond formatting
        score += int(time[4:6]) * 10 #add the amount of milliseconds * 10 to the score
        return score # send the score
        
    def saveScore(self):
        '''This function will save the user's score to the high_score.txt file.'''
        write_text = self.time + ' ' + self.name.get() # create a variable with the text to write
        file = open("high_score.txt", 'w') # open the file
        file.write(write_text) # write the text
        file.close() # close the file
        self.canvas.delete('save')
            
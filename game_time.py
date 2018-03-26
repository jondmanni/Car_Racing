''' This class will keep track of the game time and run various time-related functions.
Created Fall 2014
game_time.py
@author: Jonathan Manni (jdm42)
'''

from tkinter import *
import math # import math to use for absolute value

class Time():
    def __init__(self, canvas, scale):
        self.canvas = canvas # instantiate what canvas to use
        
        self.time = StringVar() # instantiate a time StringVar
        self.time.set("00:00:00") # set the time to zero
        self.pos_x = scale / 3 # place the time in the top left
        self.pos_y = scale / 3 # place the time in the top left
        
        self.msec = 0 # create millisecond counter
        self.sec = 0 # create second counter
        self.min = 0 # create minute counter
        self.sec_disp = 0 # create second display counter
        
        self.time_car1 = 0 # set timer for checkpoint display (car1) to zero
        self.time_car2 = 0 # set timer for checkpoint display (car 2) to zero
        
        self.font_size = int(scale / 4) # set the font size to a quarter of the scale
        
    def getTime(self):
        return self.time.get()
    
    def timer(self, data):
        '''This function will start a timer for a checkpoint label when checkpoint is reached.'''
        if data == 'car1':
            self.time_car1 = self.sec_disp
        elif data == 'car2':
            self.time_car2 = self.sec_disp
            
    def checkDelete(self, time, label):
        '''This function will check when the timer is up for the checkpoint label to be deleted.
        If so, it will delete the appropriate label.'''
        if label.number == 1:
            if math.fabs((self.sec_disp - self.time_car1)) > time:
                label.deleteCheckpoint()
        elif label.number == 2:
            if math.fabs((self.sec_disp - self.time_car2)) > time:
                label.deleteCheckpoint()
    
    def displayTime(self):
        '''This function will format time correctly, and will display it on the canvas.'''
        self.sec = self.msec // 1000 # set seconds to the int divide of milliseconds
        self.min = self.sec // 60 # set minutes to the int divide of seconds
        
        # make milliseconds go to zero as seconds add up
        if self.msec >= 1000:
            msec_disp = self.msec - (self.sec * 1000)
        elif self.msec < 1000:
            msec_disp = self.msec
            
        # make seconds go to zero as minutes add up
        if self.min >= 1:
            self.sec_disp = self.sec - (self.min * 60)
        elif self.min < 1:
            self.sec_disp = self.sec
        
        #set minute formatting
        if self.min <= 9: # if minutes are 9 or smaller
            min_format = '0' + str(self.min) # add a zero before the minute
        elif self.min > 9: # otherwise, if minutes are greater than 9
            min_format = str(self.min) # send the minutes as they are
        
        #set second formatting
        if self.sec_disp > 9: # if seconds are greater than 9
            sec_format = str(self.sec_disp) # send seconds as they are
        elif self.sec_disp <= 9: # if seconds are 9 or smaller
            sec_format = '0' + str(self.sec_disp) # add a zero before the minute
            
        #set millisecond formatting
        if msec_disp >= 100: # if milliseconds are larger than 100
            msec_format = str(int(msec_disp / 10)) # divide the ms by 10 and send
        elif msec_disp < 100: # if milliseconds are less than 100
            msec_format = str(msec_disp) # send milliseconds as they are
    
        #send formatted digits to screen
        self.canvas.delete('time') # delete the current time on the screen
        self.time.set(min_format + ':' + sec_format + ':' + msec_format) # update the time
        # send the time to canvas
        self.canvas.create_text((self.pos_x, self.pos_y), font=("Verdana", self.font_size), text=self.time.get(), anchor=NW, tags='time')
        
    def changeTime(self, rate):
        self.msec += rate # add the rate to the current milliseconds
        self.displayTime() # run the display time function
        
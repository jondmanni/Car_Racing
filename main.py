''' This file contains the GUI class that will run the game, as well as other necessary game functions.

Controls:
**Make sure caps lock is off.**
Car 1 - up: o, down: l, left: k, right: ;
Car 2 - up: w, down: s, left: a, right: d

Created Fall 2014
main.py
@author: Jonathan Manni (jdm42)
'''

import tkinter
import os.path
from car import * # import class in car.py
from map import * # import class in map.py
from label_manager import * # import class in label_manager.py
from saveScore import * # import class in saveScore.py
from game_time import Time # import Time from game_time.py

class GUI:
    def __init__(self):
        self.pressed = {} # this dict keeps track of keys that have been pressed but not released
        self.is_won = False # set a variable saying that he game hasn't been won
        self.window = tkinter.Tk() # create a window
        self.window.title('Car Racing') # title the window
        self.window.geometry('+100+100') # set the window geometry

        try: # try to create the map
            map_loc = os.path.join('maps','hey_lava.txt') # reference the map file
            self.map = Map(map_loc) # call the Map constructor
            self.map.drawRoad() # ask the map to draw the road
        except Exception as err: # if an error is thrown, catch it
            print('Could not create game.', err) # print that an error was thrown

        # create the first car
        self.car1 = Car(self.map.canvas, self.map.scale, "orange", 1, self.map.start_pos_x, self.map.start_pos_y)
        # create the second car
        self.car2 = Car(self.map.canvas, self.map.scale, "purple", 2, self.map.start_pos_x, self.map.start_pos_y)

        self.time = Time(self.map.canvas, self.map.scale) # create a global Time objected
        self.win_check_dist = self.map.scale * 0.4 # create a variable keeping track of the radius around win square

        self.car1_labels = Labels(self.map, self.car1) # create a labels object for car 1
        self.car2_labels = Labels(self.map, self.car2) # create a labels object for car 2

        self._set_bindings() # see sources.txt line 1
        self.animate() # run the animation

        self.window.mainloop() # run the mainloop for the window

    def _set_bindings(self): # see sources.txt line 1
        '''This function binds the keys to actions.
        See sources.txt line 1.'''
        for char in ["w","s","o", "l", "a", "d", "k", ";"]:
            self.window.bind("<KeyPress-%s>" % char, self._pressed)
            self.window.bind("<KeyRelease-%s>" % char, self._released)
            self.pressed[char] = False

    def _pressed(self, event):
        '''This function will identify if a key is currently pressed.
        See sources.txt line 1.'''
        self.pressed[event.char] = True

    def _released(self, event):
        '''This function will identify if a key has been released.
        See sources.txt line 1.'''
        self.pressed[event.char] = False

    def key_check(self):
        '''This function checks for which keys are pressed, and does an appropriate action.
        See sources.txt line 1.'''
        if self.map.getMapFill(self.car1._x, self.car1._y) == "on_track": # if car 1 is on the track
            # check if the direction keys are pressed
            if self.pressed["o"] or self.pressed["l"] or self.pressed["k"] or self.pressed[';']:
                self.car1.slow = False # set the slow indicator to false
                self.car1.accel = True # set the acceleration indicator to true
                self.car1.slow_speed = self.car1.speed # reset the speed again
            else: # if the direction keys are not pressed
                self.car1.accel = False # set the acceleration indicator to false
                self.car1.fast_speed = self.car1.speed * 0.1 # reset the speed again
            if self.pressed["o"]: self.car1.move_up("fast") # if o is pressed, move up fast - see sources.txt line 1
            if self.pressed["l"]: self.car1.move_down("fast") # if l is pressed, move down fast - see sources.txt line 1
            if self.pressed["k"]: self.car1.move_left("fast") # if k is pressed, move left fast - see sources.txt line 1
            if self.pressed[";"]: self.car1.move_right("fast") # if ; is pressed, move right fast - see sources.txt line 1
        elif self.map.getMapFill(self.car1._x, self.car1._y) == "off_track": # if car 1 is off the track
            # check if direction keys are pressed
            if self.pressed["o"] or self.pressed["l"] or self.pressed["k"] or self.pressed[';']:
                self.car1.slow = True
                self.car1.accel = False
                self.car1.fast_speed = self.car1.speed * 0.1 # reset the speed again
            if self.pressed["o"]: self.car1.move_up("slow") # see sources.txt line 1
            if self.pressed["l"]: self.car1.move_down("slow") # see sources.txt line 1
            if self.pressed["k"]: self.car1.move_left("slow") # see sources.txt line 1
            if self.pressed[";"]: self.car1.move_right("slow") # see sources.txt line 1
        if self.map.getMapFill(self.car2._x, self.car2._y) == "on_track":
            if self.pressed["w"] or self.pressed["s"] or self.pressed["a"] or self.pressed['d']:
                self.car2.slow = False
                self.car2.accel = True
                self.car2.slow_speed = self.car2.speed # reset the speed again
            else:
                self.car2.accel = False
                self.car2.fast_speed = self.car1.speed * 0.1 # reset the speed again
            if self.pressed["w"]: self.car2.move_up("fast") # see sources.txt line 1
            if self.pressed["s"]: self.car2.move_down("fast") # see sources.txt line 1
            if self.pressed["a"]: self.car2.move_left("fast") # see sources.txt line 1
            if self.pressed["d"]: self.car2.move_right("fast") # see sources.txt line 1
        elif self.map.getMapFill(self.car2._x, self.car2._y) == "off_track":
            if self.pressed["w"] or self.pressed["s"] or self.pressed["a"] or self.pressed['d']:
                self.car2.slow = True
                self.car2.accel = False
                self.car2.fast_speed = self.car2.speed * 0.1 # reset the speed again
            if self.pressed["w"]: self.car2.move_up("slow") # see sources.txt line 1
            if self.pressed["s"]: self.car2.move_down("slow") # see sources.txt line 1
            if self.pressed["a"]: self.car2.move_left("slow") # see sources.txt line 1
            if self.pressed["d"]: self.car2.move_right("slow") # see sources.txt line 1

    def checkpoints(self):
            self.car1.check_Checkpoint(self.map.cp_pos_x, self.map.cp_pos_y)
            self.car2.check_Checkpoint(self.map.cp_pos_x, self.map.cp_pos_y)
            if (self.car1.got_checkpoint == True) and (self.car1_labels.checkpoint_printed == False):
                self.time.timer('car1')
                self.car1_labels.printCheckpoint()
            elif (self.car2.got_checkpoint == True) and (self.car2_labels.checkpoint_printed == False):
                self.time.timer('car2')
                self.car2_labels.printCheckpoint()

            if self.car1_labels.checkpoint_printed == True: # if the car1 checkpoint label printed
                self.time.checkDelete(2, self.car1_labels) # set the timer for 2 seconds before delete
            if self.car2_labels.checkpoint_printed == True: # if the car2 checkpoint label printed
                self.time.checkDelete(2, self.car2_labels) # set the timer foar 2 seconds before delete


    def check_win(self):
        '''This function will check if the cars have won the game,
        provided they have reached the checkpoint.'''
        if (self.car1.got_checkpoint == True) or (self.car2.got_checkpoint == True): # if either car hit a checkpoint
            if self.is_won == False: # if the game hasn't been, check each car's status
                # check if car 1 won the game
                if (-self.win_check_dist <= (self.map.win_pos_x - self.car1.get_x()) <= self.win_check_dist) and \
                (-self.win_check_dist <= (self.map.win_pos_y - self.car1.get_y()) <= self.win_check_dist):
                    self.car1_labels.deleteCheckpoint()
                    self.car1_labels.printWin()
                    endScore(self.map, self.time.getTime())
                    self.is_won = True
                # check if car 2 won the game
                elif (-self.win_check_dist <= (self.map.win_pos_x - self.car2.get_x()) <= self.win_check_dist) and \
                (-self.win_check_dist <= (self.map.win_pos_y - self.car2.get_y()) <= self.win_check_dist):
                    self.car2_labels.deleteCheckpoint()
                    self.car2_labels.printWin()
                    endScore(self.map, self.time.getTime())
                    self.is_won = True

    def animate(self):
        while True:
            self.key_check() # check which buttons are currently pressed
            self.check_win() # check if a car has one
            self.checkpoints() # check if the cars have reached the checkpoints
            self.car1.draw(self.is_won) # draw car 1
            self.car2.draw(self.is_won) # draw car 2
            self.car1.physics() # run car1 physics
            self.car2.physics() # run car2 physics
            if self.is_won == False: #check if the game has been won
                self.time.changeTime(60) # update game_time by frame rate
            self.map.canvas.after(60)
            self.map.canvas.update()


game = GUI()

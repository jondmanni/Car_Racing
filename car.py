''' This class will manage a car and it's movement, as well as other indicating variables.
Created Fall 2014
car.py
@author: Jonathan Manni (jdm42)
'''

class Car:
    def __init__(self, canvas, scale, color, number, start_x, start_y):
        self.canvas = canvas # set a global canvas variable to the canvas that was sent
        self._x = start_x # set the cars current x location to the starting x location
        self._y = start_y # set the cars current y location to the starting y location
        self.got_checkpoint = False # set an indicator saying the car has reached the checkpoint to False
        self.scale = scale # set a global scale variable to the scale that was sent
        self.color = color # set the color of the car to the color that was sent
        self.number = number # set the number of the car to the number that was sent
        self.slow = False # set an indicator showing if the car is going slow to False
        self.accel = False # set an indicator showing if the car is accelerating to False
        
        self.tag = 'car' + str(number) # create a tag for the car to delete it when needed
        
        self.speed = self.scale * 0.2 # set the speed of the car to (2/10) of the current scale
        self.slow_speed = self.speed # set the slow speed to start at the speed of the car
        self.fast_speed = self.speed * 0.1 # set the fast speed to start at (1/10) of the initial speed
        
        # create an oval representing the car to begin with
        self.car = self.canvas.create_oval(self._x - (self.scale/4), self._y - (self.scale/4), self._x + (self.scale/4),
                                           self._y + (self.scale/4), fill = self.color, tags=self.tag)
    
    def draw(self, is_won):
        '''This function will delete the car where it is and draw it where it has moved,
        if the game hasn't been won.'''    
        self.canvas.delete(self.tag) # delete the current car
        if not is_won: # if the game is still in process
            # create an image of the car again in it's new location
            self.canvas.create_oval(self._x - (self.scale/4), self._y - (self.scale/4), self._x + (self.scale/4),
                                               self._y + (self.scale/4), fill = self.color, tags=self.tag)
        
    def get_x(self):
        return self._x
    
    def get_y(self):
        return self._y
    
    def check_Checkpoint(self, x, y):
        '''This function will check if the car is on the checkpoint or not.'''
        if (-(self.scale / 2) <= (x - self._x) <= (self.scale / 2)) and \
            (-(self.scale / 2) <= (y - self._y) <= (self.scale /2)): # if the car is in the vicinity
                self.got_checkpoint = True # change the checkpoint indicator to True
    
    def move_up(self, speed):
        '''This function will move the car up at a certain speed.'''
        if speed == "fast": # if the speed of the car is fast
            self._y -= self.fast_speed # move the car up fast
        elif speed == "slow": # if the speed of the car is slowly
            self._y -= self.slow_speed # move the car up slowly
    
    def move_down(self, speed):
        '''This function will move the car down at a certain speed.'''
        if speed == "fast": # if the speed of the car is fast
            self._y += self.fast_speed # move the car down fast
        elif speed == "slow":  # if the speed of the car is slow
            self._y += self.slow_speed # move the car down slowly
    
    def move_left(self, speed):
        '''This function will move the car left at a certain speed.'''
        if speed == "fast": # if the speed of the car is fast
            self._x -= self.fast_speed # move the car left fast
        elif speed == "slow": # if the speed of the car is slow
            self._x -= self.slow_speed # move the car left slowly
    
    def move_right(self, speed):
        if speed == "fast": # if the speed of the car is fast
            self._x += self.fast_speed # move the car right fast
        elif speed == "slow": # if the speed of the car is slow
            self._x += self.slow_speed # move the car right slowly
            
    def physics(self):
        '''This function will manage the acceleration and deceleration of the car.'''
        if self.accel == True: # if the car is accelerating
            if self.fast_speed < self.speed: # while the fast_speed of the car is lower than max speed
                self.fast_speed *= 1.1 # increase the fast_speed by a multiple of 1.1
        if self.slow == True: # when car leaves the track, slow it down incrementally
            if self.slow_speed > (self.speed * 0.1): #if the slow speed is greater than the min speed
                self.slow_speed *= 0.6 * 0.6 # slow the speed down by the square of 0.6
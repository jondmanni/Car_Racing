''' This class will render a canvas containing the map, and store other important map variables.
Created Fall 2014
map.py
@author: Jonathan Manni (jdm42)
'''

import tkinter

class Map:
    def __init__(self, filename):
        self.root = tkinter.Tk() # create Tkinter object to determine screen size
        self.file = filename
        # self.scale = int(root.winfo_screenwidth()/len(self # set the size of each "pixel" of the map
        self.rows = [] # create an empty global "rows" list 
        self.win_pos_x = 0 # x location of the win block initialized to 0
        self.win_pos_y = 0 # y location of the win block initialized to 0
        self.start_pos_x = 0 # x location of the start block initialized to 0
        self.start_pos_y = 0 # y location of the start block initialized to 0
        self.cp_pos_x = 0 # x location of the checkpoint initialized to 0
        self.cp_pos_y = 0 # y location of the checkpoint initialized to 0
        
        self.getMapData() # read the map data in from file

        self.scale = int(self.root.winfo_screenwidth()/len(self.rows[0])) # set the size of each "pixel" of the map

        self.rows_count = 0 # set the current row to 0
        self.cols_count = 0 # set the current column to 0
        self.x0 = self.cols_count * self.scale # set the current x location on the canvas to 0
        self.y0 = self.rows_count * self.scale # set the current y location on the canvas to 0
        # create the canvas as wide and high as the scale multiplied by the width and height of map data
        self.canvas = tkinter.Canvas(width = self.scale * len(self.rows[0]), 
                                     height = self.scale * len(self.rows))
        self.canvas.pack() # pack the canvas onto the window
        
    def getWidth(self):
        '''This function will provide the width of the map canvas to anything that asks for it.'''
        return len(self.rows[0]) * self.scale
        
    def getHeight(self):
        '''This function will provide the height of the map canvas to anything that asks for it.'''
        return len(self.rows) * self.scale
    
    def getMapData(self):
        '''This function loads in the map data from file.'''
        file = open(self.file)
        lines = file.readlines()
        for line in lines:
            self.rows.append(line.split()) # split lines based on spaces to get color codes
            
    def findStartSpace(self):
        '''This function will find the location of the red starting space.'''
        left = self.getPixel((self.cols_count - 1), self.rows_count) # gets the pixel to the left
        right = self.getPixel((self.cols_count + 1), self.rows_count) # gets the pixel to the right
        up = self.getPixel(self.cols_count, (self.rows_count - 1)) # gets the pixel above
        down = self.getPixel(self.cols_count, (self.rows_count + 1))  # gets the pixel below
        #if red win space is in horizontal with road
        if (left == '#000000') and (right == '#000000') and (up != '#000000') and (down != '#000000'):
            # if winspace is on right top of screen
            if ((self.cols_count / len(self.rows[0])) > 0.5) and ((self.rows_count / len(self.rows)) < 0.5):
                self.start_pos_x = (self.cols_count - 1) * self.scale + self.scale/2 # set start position to left
                self.start_pos_y = self.rows_count * self.scale + self.scale/2 
            # if winspace is on left top of screen
            elif ((self.cols_count / len(self.rows[0])) < 0.5) and ((self.rows_count / len(self.rows)) < 0.5):
                self.start_pos_x = (self.cols_count - 1) * self.scale + self.scale/2 # set start position to left
                self.start_pos_y = self.rows_count * self.scale + self.scale/2
            # if winspace is on left bottom of screen
            elif ((self.cols_count / len(self.rows[0])) < 0.5) and ((self.rows_count / len(self.rows)) > 0.5):
                self.start_pos_x = (self.cols_count + 1) * self.scale + self.scale/2 # set start position to right
                self.start_pos_y = self.rows_count * self.scale + self.scale/2
            # if winspace is on right bottom of screen
            elif ((self.cols_count / len(self.rows[0])) > 0.5) and ((self.rows_count / len(self.rows)) < 0.5):
                self.start_pos_x = (self.cols_count + 1) * self.scale + self.scale/2 # set start position to right
                self.start_pos_y = self.rows_count * self.scale + self.scale/2
                
        #if red win space is in vertical with road 
        elif (left != '#000000') and (right != '#000000') and (up == '#000000') and (down == '#000000'):
            # if winspace is on right top of screen
            if ((self.cols_count / len(self.rows[0])) > 0.5) and ((self.rows_count / len(self.rows)) < 0.5):
                self.start_pos_x = self.cols_count * self.scale + self.scale/2
                self.start_pos_y = (self.rows_count - 1) * self.scale + self.scale/2 # set start position above
            # if winspace is on left top of screen
            elif ((self.cols_count / len(self.rows[0])) < 0.5) and ((self.rows_count / len(self.rows)) < 0.5):
                self.start_pos_x = self.cols_count * self.scale + self.scale/2
                self.start_pos_y = (self.rows_count + 1) * self.scale + self.scale/2 # set start position below
            # if winspace is on left bottom of screen
            elif ((self.cols_count / len(self.rows[0])) < 0.5) and ((self.rows_count / len(self.rows)) > 0.5):
                self.start_pos_x = self.cols_count * self.scale + self.scale/2
                self.start_pos_y = (self.rows_count + 1) * self.scale + self.scale/2 # set start position below
            # if winspace is on right bottom of screen
            elif ((self.cols_count / len(self.rows[0])) > 0.5) and ((self.rows_count / len(self.rows)) < 0.5):
                self.start_pos_x = self.cols_count * self.scale + self.scale/2
                self.start_pos_y = (self.rows_count - 1) * self.scale + self.scale/2 # set start position above
    
    def getMapFill(self, x, y):
        '''int, int -> str
        This function will return if a car is on the road or not.'''
        flat_x = int(x // self.scale) # set a variable to x int-divided by the scale
        flat_y = int(y // self.scale) # set a variable to y int-divided by the scale
        color = self.getPixel(flat_x, flat_y) # get the color at that location 
        if color == '#000000': # if the color is black
            return 'on_track' # return that the car is on the track
        else: # otherwise
            return 'off_track' # return that the car is not on the track
        
    def getPixel(self, x, y):
        '''int, int -> str
        This function will return the color of a particular pixel.'''
        return self.rows[y][x]
    
    def blackPixel(self):
        '''This function will take any black pixels from the loaded map and
        apply curves around the corners.'''
        # order of pixel location in the if statement is as follows:
        # left, up, down, right
        
        # if black pixel is horizontal
        if self.getPixel((self.cols_count - 1), self.rows_count) == '#000000' and \
           self.getPixel(self.cols_count, (self.rows_count - 1)) != '#000000' and \
           self.getPixel(self.cols_count, (self.rows_count + 1)) != '#000000' and \
           self.getPixel((self.cols_count + 1), self.rows_count) == '#000000':
            self.canvas.create_rectangle(self.x0, self.y0, #create background rectangle
                                 (self.x0 + self.scale), (self.y0 + self.scale), 
                                 fill='black', outline='black') # fill with black
        # if black pixel is horizontal with red win space to right
        elif self.getPixel((self.cols_count - 1), self.rows_count) == '#000000' and \
           self.getPixel(self.cols_count, (self.rows_count - 1)) != '#000000' and \
           self.getPixel(self.cols_count, (self.rows_count + 1)) != '#000000' and \
           self.getPixel((self.cols_count + 1), self.rows_count) == '#ff0000':
            self.canvas.create_rectangle(self.x0, self.y0, #create background rectangle
                                 (self.x0 + self.scale), (self.y0 + self.scale), 
                                 fill='black', outline='black') # fill with black
        # if black pixel is horizontal with red win space to left
        elif self.getPixel((self.cols_count - 1), self.rows_count) == '#ff0000' and \
           self.getPixel(self.cols_count, (self.rows_count - 1)) != '#000000' and \
           self.getPixel(self.cols_count, (self.rows_count + 1)) != '#000000' and \
           self.getPixel((self.cols_count + 1), self.rows_count) == '#000000':
            self.canvas.create_rectangle(self.x0, self.y0, #create background rectangle
                                 (self.x0 + self.scale), (self.y0 + self.scale), 
                                 fill='black', outline='black') # fill with black
        # if black pixel is vertical
        elif self.getPixel((self.cols_count - 1), self.rows_count) != '#000000' and \
           self.getPixel(self.cols_count, (self.rows_count - 1)) == '#000000' and \
           self.getPixel(self.cols_count, (self.rows_count + 1)) == '#000000' and \
           self.getPixel((self.cols_count + 1), self.rows_count) != '#000000':
            self.canvas.create_rectangle(self.x0, self.y0, #create background rectangle
                                 (self.x0 + self.scale), (self.y0 + self.scale), 
                                 fill='black', outline='black') # fill with black
        # if black pixel is vertical with red win space above
        elif self.getPixel((self.cols_count - 1), self.rows_count) != '#000000' and \
           self.getPixel(self.cols_count, (self.rows_count - 1)) == '#ff0000' and \
           self.getPixel(self.cols_count, (self.rows_count + 1)) == '#000000' and \
           self.getPixel((self.cols_count + 1), self.rows_count) != '#000000':
            self.canvas.create_rectangle(self.x0, self.y0, #create background rectangle
                                 (self.x0 + self.scale), (self.y0 + self.scale), 
                                 fill='black', outline='black') # fill with black
        # if black pixel is vertical with red win space below
        elif self.getPixel((self.cols_count - 1), self.rows_count) != '#000000' and \
           self.getPixel(self.cols_count, (self.rows_count - 1)) == '#000000' and \
           self.getPixel(self.cols_count, (self.rows_count + 1)) == '#ff0000' and \
           self.getPixel((self.cols_count + 1), self.rows_count) != '#000000':
            self.canvas.create_rectangle(self.x0, self.y0, #create background rectangle
                                 (self.x0 + self.scale), (self.y0 + self.scale), 
                                 fill='black', outline='black') # fill with black
        # if black pixel is a top left corner, create curved edge
        elif self.getPixel((self.cols_count - 1), self.rows_count) != '#000000' and \
           self.getPixel(self.cols_count, (self.rows_count - 1)) != '#000000':
            self.canvas.create_rectangle(self.x0, self.y0, #create background rectangle
                                 (self.x0 + self.scale), (self.y0 + self.scale), 
                                 fill=self.getPixel((self.cols_count - 1), self.rows_count), 
                                 outline=self.getPixel((self.cols_count - 1), self.rows_count))
            #create an arc in top left
            self.canvas.create_arc(self.x0, self.y0,
                                   (self.x0 + self.scale), (self.y0+ self.scale),
                                   start = 90, extent = 90, fill = 'black')
            # create a polygon to cover what the arc didn't cover
            self.canvas.create_polygon((self.x0 + (self.scale / 2)), self.y0, 
                                       self.x0, (self.y0 + (self.scale / 2)),
                                       self.x0, (self.y0 + self.scale),
                                       (self.x0 + self.scale), (self.y0 + self.scale),
                                       (self.x0 + self.scale), self.y0,
                                        fill = 'black') 
        # if black pixel is a bottom left corner, create curved edge
        elif self.getPixel((self.cols_count - 1), self.rows_count) != '#000000' and \
           self.getPixel(self.cols_count, (self.rows_count + 1)) != '#000000':
            self.x0 = self.cols_count * self.scale
            self.y0 = self.rows_count * self.scale
            self.canvas.create_rectangle(self.x0, self.y0, #create background rectangle
                                 (self.x0 + self.scale), (self.y0 + self.scale), 
                                 fill=self.getPixel((self.cols_count - 1), self.rows_count), 
                                 outline=self.getPixel((self.cols_count - 1), self.rows_count))
            # create an arc in bottom left
            self.canvas.create_arc(self.x0, self.y0,
                                   (self.x0 + self.scale), (self.y0 + self.scale),
                                   start = 180, extent = 90, fill = 'black')
            # create a polygon to cover what the arc didn't cover
            self.canvas.create_polygon(self.x0, (self.y0 + (self.scale / 2)), 
                                       (self.x0 + (self.scale / 2)), (self.y0 + self.scale),
                                       (self.x0 + self.scale), (self.y0 + self.scale),
                                       (self.x0 + self.scale), self.y0,
                                       self.x0, self.y0,
                                        fill = 'black') 
        # if black pixel is a bottom right corner, create curved edge
        elif self.getPixel(self.cols_count, (self.rows_count + 1)) != '#000000' and \
           self.getPixel((self.cols_count + 1), self.rows_count) != '#000000':
            self.x0 = self.cols_count * self.scale
            self.y0 = self.rows_count * self.scale
            self.canvas.create_rectangle(self.x0, self.y0, #create background rectangle
                                 (self.x0 + self.scale), (self.y0 + self.scale), 
                                 fill=self.getPixel(self.cols_count, (self.rows_count + 1)), 
                                 outline=self.getPixel(self.cols_count, (self.rows_count + 1)))
            # create arc in bottom right
            self.canvas.create_arc(self.x0, self.y0,
                                   (self.x0 + self.scale), (self.y0 + self.scale),
                                   start = 270, extent = 90, fill = 'black')
            # create a polygon to cover what the arc didn't cover
            self.canvas.create_polygon((self.x0 + self.scale), (self.y0 + (self.scale / 2)), 
                                       (self.x0 + (self.scale / 2)), (self.y0 + self.scale),
                                       (self.x0), (self.y0 + self.scale),
                                       (self.x0), self.y0,
                                       (self.x0 + self.scale), self.y0,
                                        fill = 'black')    
        # if black pixel is a top right corner, create curved edge
        elif self.getPixel(self.cols_count, (self.rows_count - 1)) != '#000000' and \
           self.getPixel((self.cols_count + 1), self.rows_count) != '#000000':
            self.x0 = self.cols_count * self.scale
            self.y0 = self.rows_count * self.scale
            self.canvas.create_rectangle(self.x0, self.y0, #create background rectangle
                                 (self.x0 + self.scale), (self.y0 + self.scale), 
                                 fill=self.getPixel((self.cols_count + 1), (self.rows_count)), 
                                 outline=self.getPixel((self.cols_count + 1), (self.rows_count)))
            # create arc in top right
            self.canvas.create_arc(self.x0, self.y0,
                                   (self.x0 + self.scale), (self.y0 + self.scale),
                                   start = 0, extent = 90, fill = 'black')
            # create a polygon to cover what the arc didn't cover
            self.canvas.create_polygon((self.x0 + (self.scale / 2)), (self.y0), 
                                       (self.x0 + self.scale), (self.y0 + (self.scale / 2)),
                                       (self.x0 + self.scale), (self.y0 + self.scale),
                                       (self.x0), (self.y0 + self.scale),
                                       (self.x0), self.y0,
                                        fill = 'black')  
            
    def drawRoad(self):
        '''This function will draw the entire map, including the road.'''
        # first, find the location of the checkpoint and change it's color data to black
        for row in self.rows: # go through each row
            for color in row: # go through each color in the row
                if color == "#0000ff": # if the color is pure blue 
                    self.cp_pos_x = self.cols_count * self.scale + (self.scale/2) # set the checkpoint position x
                    self.cp_pos_y = self.rows_count * self.scale + (self.scale/2) # set the checkpoint position y
                    self.rows[self.rows_count][self.cols_count] = "#000000" #update the color to be black
                self.cols_count += 1 # add 1 to the column count
            self.rows_count += 1 # add 1 to the row count
            self.cols_count = 0 # reset the column count
        
        self.rows_count = 0 # reset row count for map-making
        self.cols_count = 0 # reset column count for map-making

        for row in self.rows: # go through each row
            for color in row: # go through each color in the row
                if color == "#ff0000": # store the location of the win space if pure red
                    self.win_pos_x = self.cols_count * self.scale + (self.scale/2) # store pos x
                    self.win_pos_y = self.rows_count * self.scale + (self.scale/2) # store pos y
                    self.findStartSpace() # run the start space function to find where to start cars
                    # create the red rectangle as the win space
                    self.canvas.create_rectangle(self.cols_count * self.scale, self.rows_count * self.scale, 
                                                 ((self.cols_count * self.scale) + self.scale), 
                                                 ((self.rows_count * self.scale)+ self.scale), 
                                                 fill=color, outline=color)    
                elif color == "#000000": # otherwise, if the color is black
                    self.blackPixel() # run the blackPixel function to determine curves and horiz/vertical
                else: # otherwise create a rectangle with the color listed (for everything that isn't black or red)
                    # create a rectangle with the current color
                    self.canvas.create_rectangle(self.cols_count * self.scale, self.rows_count * self.scale, 
                                                 ((self.cols_count * self.scale) + self.scale), 
                                                 ((self.rows_count * self.scale)+ self.scale), 
                                                 fill=color, outline=color)    
                self.cols_count += 1 # add one to the column count
                self.x0 = self.cols_count * self.scale # set x position to the column count * scale
                self.y0 = self.rows_count * self.scale # set y position to the row count * scale
            self.rows_count += 1 # add one to the row count
            self.cols_count = 0 # reset the column count
            self.x0 = self.cols_count * self.scale # set x position to the column count * scale
            self.y0 = self.rows_count * self.scale # set y position to the row count * scale
                
# Car Racing
A multiplayer racing game I made for a final project for an intro computer science course back in 2014.
## Quick Start Guide
To start racing, download or clone the repository on your own machine. Run 'main.py' with Python 3 and start racing!

Keyboard Controls:
* O, K, L, ; - Player 1: Up, Left, Down, Right 
* W, A, S, D - Player 2: Up, Left, Down, Right 

## Custom Map Making
In addition to multiplayer racing fun, the game supports custom maps. Four maps are included as examples, but use the following steps to get started creating custom maps.
1. Using your favorite image editing software to draw a map, noting that individual pixels represent items on screen (i.e. a 25x25 pixel image would represent a 25x25 block map).
2. Include the following items:
* Road (this must be one continuous loop and must be pure black in color, #000000)
* A checkpoint square (this must be pure blue in color, #0000ff)
* A "finish" square (this cannot be adjacent a turn/corner, and must be pure red in color, #ff0000)
* All other pixels can be any color besides pure black, pure blue, or pure red and will show up as the color provided
3. Save the image somewhere in the main directory (inside the 'maps' folder is great).
4. Run 'analyze_map.py' and enter the location and filename of image as follows:
```
maps/your_map_here.png
```
5. Then, enter the location of where you'd like to save the map with a '.txt' filename as follows:
```
maps/your_map_here.txt
```
6. Next, edit line 30 of 'main.py' with the name of your newly-created map file (note: you may need to change the directory depending on where you saved the file):
```
map_loc = os.path.join('maps','your_map_here.txt')
```
7. You're all set to play on your new map. Run 'main.py' to see your new map.

## High Score
Race against your best times with the built-in high score feature.
If you'd ever like to reset the high score, follow these steps:
1. Open up 'high_score.txt' and fill in the time with a time you can beat.
```
01:59:59 Slowpoke
```
2. Save the file and get back to racing.

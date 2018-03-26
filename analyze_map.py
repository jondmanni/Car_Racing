import os.path
from PIL import Image

while True:
    try:
        img = Image.open(input('Enter map image file location and name: '))
        print("Awesome.")
        out = input('Enter the output file location and name (as a .txt file): ')
        break
    except Exception as err:
        print("Couldn't open file, try again:", err)

def getFill(pix):
    im = img.convert('RGB') # change img mode to RGB, in case it isn't
    color_inst = '#%02x%02x%02x' % im.getpixel(pix)  # convert color to hex
    return color_inst  # send hex color

img_size_x = img.size[1]
img_size_y = img.size[0]
print('Image size is:', img_size_y, 'x', img_size_x)
print('Image type is:', img.format)

cols = []
rows = []

count_x = 0
count_y = 0

pixel = (count_x, count_y)

while count_y < img_size_x:
    while count_x < img_size_y:
        cols.append(getFill(pixel))
        count_x += 1
        pixel = (count_x, count_y)
    rows.append(cols)
    cols = []
    count_x = 0
    count_y += 1
    pixel = (count_x, count_y)
    
# write the map data to file
#write_loc = os.path.join('maps','hey_lavaadsfadf.txt')
file = open(out, 'w')
for row in rows:
    for item in row:
        file.write(item)
        file.write(' ')
    file.write('\n')    
file.close()
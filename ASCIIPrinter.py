#I am very lazy so I found a package that does it instead of doing it manually
#Code is a modified version of code from this link: https://stackoverflow.com/questions/9632995/how-to-easily-print-ascii-art-text

from PIL import Image, ImageFont, ImageDraw

ShowText = 'Torstein'

font = ImageFont.truetype('arialbd.ttf', 15) #load the font
size = font.getsize(ShowText)  #calc the size of text in pixels
image = Image.new('1', size, 1)  #create a b/w image
draw = ImageDraw.Draw(image)
draw.text((0, 0), ShowText, font=font) #render the text to the bitmap
for rownum in range(size[1]): 
#scan the bitmap:
# print ' ' for black pixel and 
# print '#' for white one
    line = []
    for colnum in range(size[0]):
        if image.getpixel((colnum, rownum)): line.append(' '),
        else: line.append('*'),
    print(''.join(line))

ShowText = 'Hatlebakk'

font = ImageFont.truetype('arialbd.ttf', 15) #load the font
size = font.getsize(ShowText)  #calc the size of text in pixels
image = Image.new('1', size, 1)  #create a b/w image
draw = ImageDraw.Draw(image)
draw.text((0, 0), ShowText, font=font) #render the text to the bitmap
for rownum in range(size[1]): 
#scan the bitmap:
# print ' ' for black pixel and 
# print '#' for white one
    line = []
    for colnum in range(size[0]):
        if image.getpixel((colnum, rownum)): line.append(' '),
        else: line.append('*'),
    print(''.join(line))

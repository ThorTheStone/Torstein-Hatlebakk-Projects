import cv2
import numpy as np
import os


from PIL import Image, ImageDraw, ImageFilter, ImageFile



files = [f for f in os.listdir('.') if os.path.isfile(f)]

for file in files:

    if file.endswith('.JPG'):

        print(file)
        im_rgb = Image.open(file)



#print(img)


cwd = os.getcwd()

print(cwd + '\\' + 'Img.JPG')

im_rgba = im_rgb.copy()

width, height = im_rgba.size



region = im_rgba.crop((1433, 811, 1891, 1523))

new_img = Image.new('RGB', (width, height), (255, 255, 255))

new_img.paste(region, (1433, 811, 1891, 1523))
#im_rgba.paste(region, (1433, 811, 1891, 1523))

new_img.save(cwd + '\\' + 'Cropped_Ace of Clubs.jpg')









show = False

if show == True:
    imS = cv2.resize(img, (816, 612))                   
    cv2.imshow("output", imS)                           
    cv2.waitKey(0)

#Takes background removed images and adds them to backgrounds to generate random image data form machine learning datasets

import Augmentor
import time
import os
import numpy as np
import imageio
import cv2
import random
import os.path
from os import path
import pathlib
from PIL import Image, ImageDraw
import glob
import imagecorruptions

import imgaug as ia
import imgaug.augmenters as iaa
from imgaug.augmentables.bbs import BoundingBox, BoundingBoxesOnImage

from pathlib import Path

from xml.etree import cElementTree as ET

import matplotlib.pyplot as plt
import matplotlib.patches as patches



#Make multi bounding box detector and supporter



#Add out of bounds support
#Make varied auto-augmentor
#Make PB labelmap and model filler automater
#Make start training automatic as well



def getFiles():
#Get's all JPG and xml files in the script's directory

    cwd = os.getcwd()

    images = {}
    labels = []

    #files = [f for f in os.listdir('.') if os.path.isfile(f)]

    dirName = cwd + '\\' + 'Auto_Labeled_Masked_Images'
    
    for root, dirs, files in os.walk(dirName):
        for file in files:
            
            if file.endswith('.png'):
                
                #Load image from folder
                im = imageio.imread(dirName + '\\' + file)
                #Add Image to Dictionary
                images[file] = im

            if file.endswith('.xml'):
                
                #Add Label to List
                labels.append(file)

        return images, labels, dirName






def findXMLforImage(imageName, labelFiles):

    image = imageName.replace(".png", "")

    for x in labelFiles:
        label = x.replace(".xml", "")

        if label == image:

            return x, image
            

def getBndboxAmount(xmlLabel, dirName):

    root = ET.parse(dirName + '\\' + xmlLabel).getroot()

    objectCount = 0

    for x in list(root):

        if x.tag == 'object':
            objectCount = objectCount + 1

            #for z in x:

                #if z.tag == 'name':

                    #if z.text != 'Overlap':
                    
                        #objectCount = objectCount + 1

    return objectCount



def getBndboxCoordinates(bndboxAmount, xmlLabel, dirName):
    
    root = ET.parse(dirName + '\\' + xmlLabel).getroot()

    bndboxCoordinates = {}
    overlapCoordinates = {}
    objectNames = {}
    coordinateList = []
    overlapCoordinateList = []

    objectCount = 0

    bndboxVar = '''bbs = BoundingBoxesOnImage([
    LINE
], shape=image.shape)'''


    for x in list(root):

        if x.tag == 'object':
            objectCount = objectCount + 1

            for y in x:

                if y.text == 'Overlap':

                    for z in x:
                        if z.tag == 'bndbox':
                            for c in z:
                                overlapData = int(c.text)
                                overlapCoordinateList.append(overlapData)
                                

                if y.tag == 'name' and y.text != 'Overlap':
                    cardName = y.text + str(objectCount)
                    objectNames[cardName] = objectCount

                    for y in x:
                        if y.tag == 'bndbox':

                            for z in y:

                                if z.tag == 'xmin':
                                    xmin = z.text
                                    xmin = int(xmin)
                                    coordinateList.append(xmin)                 

                                elif z.tag == 'ymin':
                                    ymin = z.text
                                    ymin = int(ymin)
                                    coordinateList.append(ymin)

                                elif z.tag == 'xmax':
                                    xmax = z.text
                                    xmax = int(xmax)
                                    coordinateList.append(xmax)

                                elif z.tag == 'ymax':
                                    ymax = z.text
                                    ymax = int(ymax)
                                    coordinateList.append(ymax)

                    singleBoxVar = '''BoundingBox(x1=''' + str(xmin) + ''', y1=''' + str(ymin) + ''', x2=''' + str(xmax) + ''', y2=''' + str(ymax) + ''')NEXT
    LINE'''

                    bndboxVar = bndboxVar.replace("NEXT", ',')
                    bndboxVar = bndboxVar.replace("LINE", singleBoxVar)

                if 0 < len(coordinateList):
                    bndboxCoordinates[cardName] = coordinateList
                    coordinateList = []

                if 0 < len(overlapCoordinateList):
                    overlapCoordinates[cardName] = overlapCoordinateList
                    overlapCoordinateList = []



    #Add overlap coordinates to the bbs draw
    for x in overlapCoordinates:
        listCoord = overlapCoordinates[x]

        singleBoxVar = '''BoundingBox(x1=''' + str(listCoord[0]) + ''', y1=''' + str(listCoord[1]) + ''', x2=''' + str(listCoord[2]) + ''', y2=''' + str(listCoord[3]) + ''')NEXT
    LINE'''        

        bndboxVar = bndboxVar.replace("NEXT", ',')
        bndboxVar = bndboxVar.replace("LINE", singleBoxVar)


    #Remove Extra NEXT and LINE
    bndboxVar = bndboxVar.replace("NEXT", '')
    bndboxVar = bndboxVar.replace("LINE", '')

    return bndboxVar, bndboxCoordinates, objectNames, overlapCoordinates



def getBndbox(bndboxAmount, dirName, bndboxCoordinates, objectNames):


    bndboxAfterCoordinates = {}

    bndboxVar = '''bbs = BoundingBoxesOnImage([
    LINE
], shape=image.shape)'''

    for x in bndboxCoordinates:
            
            coordinateList = []

            coordinateList.append(bndboxCoordinates[x][0])
            coordinateList.append(bndboxCoordinates[x][1])
            coordinateList.append(bndboxCoordinates[x][2])
            coordinateList.append(bndboxCoordinates[x][3])


            singleBoxVar = '''BoundingBox(x1=''' + str(bndboxCoordinates[x][0]) + ''', y1=''' + str(bndboxCoordinates[x][1]) + ''', x2=''' + str(bndboxCoordinates[x][2]) + ''', y2=''' + str(bndboxCoordinates[x][3]) + ''')NEXT
    LINE'''
            
            bndboxVar = bndboxVar.replace("NEXT", ',')
            bndboxVar = bndboxVar.replace("LINE", singleBoxVar)

            bndboxAfterCoordinates[x] = coordinateList

    bndboxVar = bndboxVar.replace("NEXT", '')
    bndboxVar = bndboxVar.replace("LINE", '')


    return bndboxVar, bndboxAfterCoordinates, objectNames


def randomNegate(coord):

    ran = random.randrange(0,2)

    if ran == 1:
        return coord
    else:
        return -coord


def multiRandomNegate(coord_1, coord_2):

    ran = random.randrange(0,2)

    if ran == 1:
        return coord_1, coord_2
    else:
        return -coord_1, -coord_2


def duoPreRandomNegate():

    ran = random.randrange(0,5)

    if ran == 1:
        return '-', '-'
    elif ran == 2:
        return '+', '+'
    elif ran == 3:
        return '-', '+'
    else:
        return '+', '-'
    

def setTestAugmentation(imagesB, labelsB, dirNameB, backgroundImgB, bbsB, imageB, bndboxDrawB, bndboxCoordinatesB, objectNamesB, bndboxAmountB, labelB, nameImageB, overlapCoordinatesB, seqAugB):

    images = imagesB.copy()
    labels = labelsB
    dirName = dirNameB
    backgroundImg = backgroundImgB
    bbs = bbsB
    image = imageB
    bndboxDraw = bndboxDrawB
    bndboxCoordinates = bndboxCoordinatesB
    objectNames = objectNamesB
    bndboxAmount = bndboxAmountB
    label = labelB
    nameImage = nameImageB
    overlapCoordinates = overlapCoordinatesB
    seqAug = seqAugB

    print(bndboxCoordinates)

    

    backgroundImg = backgroundImg.resize((3264, 2448))
    width, height = backgroundImg.size



    ia.seed(1)

    #Randomly Generate Location
    x1 = float(random.randrange(0,100)) * 0.01
    x2 = float(random.randrange(0,100)) * 0.01
    y1 = float(random.randrange(0,100)) * 0.01
    y2 = float(random.randrange(0,100)) * 0.01

    '''
    #Randomly Negate Coordinates
    x1 = randomNegate(x1)
    x2 = randomNegate(x2)
    y1 = randomNegate(y1)
    y2 = randomNegate(y2)
    '''
    
    x1, x2 = multiRandomNegate(x1, x2)
    y1, y2 = multiRandomNegate(y1, y2)
    
    #Round Coordinates
    x1 = round(x1, 3)
    x2 = round(x2, 3)
    y1 = round(y1, 3)
    y2 = round(y2, 3)

    #Add centralization offset
    centCoords = []
    centOffsets = []
    

    for x in bndboxCoordinates:

        val = x
        coords = bndboxCoordinates[x]
        
        medX = (coords[0] + coords[2])/2
        centX = (width/2) - medX
        print(centX)
        centOffsets.append(centX)

        medY = (coords[1] + coords[3])/2
        centY = (height/2) - medY
        print(centY)
        centOffsets.append(centY)
        

        centCoords.append(round(coords[0] + centX))
        centCoords.append(round(coords[1] + centY))
        centCoords.append(round(coords[2] + centX))
        centCoords.append(round(coords[3] + centY))



    #img_1.paste(img_2, (148, 315), mask=img_2)

    collection = [x1, y1, x2, y2]

    '''
    size = float(random.uniform(0.5, 1.25))
    #rot = float(random.randrange(-90, 90))
    rot = float(0)

    
    #Augment Picture
    seq = iaa.Sequential([

        #translate by 40/60px on x/y axis, and scale to 50-70%, affects BBs
        iaa.Affine(
            translate_percent={"x": (x1, x2), "y": (y1, y2)},
            scale=(size),
            rotate=(rot)
            )
    ])
    '''

    centCoordsB = centCoords
    bndboxCoordinatesB = bndboxCoordinates.copy()
    
#ffffffffffffffffffffffffffffffffffffffffffff
    stop = False
    lastOutR = 0
    lastOutS = 0

    for c in np.arange(0.5, 1.5, 0.25):
        print(c)
        
        if stop == True:
            break

        for i in np.arange(0.20, 1, 0.005):
            bndboxCoordinates = bndboxCoordinatesB.copy()
            bbs = bbsB
            centCoords = centCoordsB
            
            i = round(i, 5)

            if stop == True:
                break

            for j in range(-90, 91):
                j = j*-1
                stop = False
                lastOutS = 0
                lastOutr = 0
                
                #print('\r' + str(j) + ' ', end='')

    
                #Augment Picture
                seq = iaa.Sequential([
                    iaa.Affine(
                        translate_percent={"x": (0, 0), "y": (i, i)},
                        scale=(c),
                        rotate=(j)
                        )
                ])

                '''
                bbs = str(bbs)

                for x in bndboxCoordinates:
                    coords = bndboxCoordinates[x]

                    for y in coords:
                        bbs = bbs.replace(str(y), str(centCoords[coords.index(y)]))


                bbs = bbsMaker(bbs, None)
                bndboxCoordinates[val] = centCoords
                '''
                
                augmentedImage, bndboxCoordinatesAfter, overlapCoordinatesAfter = augmentImage(bbs, image, seq, bndboxCoordinates, overlapCoordinates)
                
                #print(bndboxCoordinatesAfter)
                
                imgT = Image.fromarray(augmentedImage, 'RGBA')
            
                augmentedImage = maskAugment(imgT, bImg)

                #Get Output Directory
                outputName = 'Ace of Clubs'
                outputDir = findOutputDirectory(outputName)





                if(checkOutBounds(augmentedImage, bndboxCoordinatesAfter)):
                    print('Out of Bounds T:' + str(i) + ' S: ' + str(c) + ' R: ' + str(j))
                    #imageActName = saveAugmentedImage(augmentedImage, nameImage, outputDir)

                    print(str(lastOutS) + str(c) + str(lastOutR) + str(j))

                    if lastOutS == c and lastOutR == j:
                        print('Found End')
                        stop = True
                        break
                    
                    lastOutS = c
                    lastOutR = j
                    break

                else:
                    lastOutR = 0
                    lastOutS = 0
                    pass
                    #print('In Bounds ' + str(i) + ' ' + str(c))
                    #Save Image
                    #if j == 90:
                        #imageActName = saveAugmentedImage(augmentedImage, nameImage, outputDir)

#ffffffffffffffffffffffffffffffffffffffffffff




def noOverlapCoord(xDirB, yDirB, usedCoordsB):
    xDir = xDirB
    yDir = yDirB
    usedCoords = usedCoordsB
    
    threshold = 0.2

    if len(usedCoords) == 0:
        x1 = random.uniform( 0, xDir)
        x2 = random.uniform( 0, xDir)

        y1 = random.uniform( 0, yDir)
        y2 = random.uniform( 0, yDir)

        return x1, x2, y1, y2
    else:

        x1 = random.uniform( 0, xDir)
        x2 = random.uniform( 0, xDir)

        y1 = random.uniform( 0, yDir)
        y2 = random.uniform( 0, yDir)


        for x in usedCoords:

            if threshold < abs(usedCoords[x][0]-x1): #and threshold < abs(usedCoords[x][1]-y1):
                pass
            else:
                print(str(abs(usedCoords[x][0]-x1))+' - '+str(abs(usedCoords[x][1]-y1)))
                #print()
                return noOverlapCoord(xDirB, yDirB, usedCoordsB) 

            return x1,x2,y1,y2
                

                    

                
    


def setMaskAugmentation(backgroundImage, usedCoords):

    if len(usedCoords) == 0:
        pass
              

    backgroundImage = backgroundImage.resize((3264, 2448))

    width, height = backgroundImage.size

    size = float(random.uniform(0.5, 1.25))

    #print(size)

    xDirV, yDirV = duoPreRandomNegate()

    #print(xDir)
    #print(yDir)


    if xDirV == '+':
        xDir = (-size-19)/-37.5
    else:
        xDir = (-size+7.69)/-14.99       



    if yDirV == '+':
        yDir = (-size-5.39)/-10.71
    else:
        yDir = (-size+3.125)/-6.25


    #print('x ' + str(xDir))
    #print('y ' + str(yDir))

    
    x1 = random.uniform( 0, xDir)
    x2 = random.uniform( 0, xDir)

    y1 = random.uniform( 0, yDir)
    y2 = random.uniform( 0, yDir)


    #Minimize Overlap
    #x1, x2, y1, y2 = noOverlapCoord(xDir, yDir, usedCoords)


    #Decided Rot Randomly
    if xDirV == '+':
        if x1 > 0.47:
            rot = float(random.randrange(-90, 83))
        else:
            rot = float(random.randrange(-90, 90))

    else:
        if x1 < -0.33:
            rot = float(random.randrange(-46, 90))
        else:
            rot = float(random.randrange(-90, 90))

            

    if yDirV == '+':
        if x1 > 0.405:
            rot = float(-89)
        else:
            rot = float(random.randrange(-90, 90))

    else:
        if x1 < -0.27:
            rot = float(random.randrange(-90, 37))
        else:
            rot = float(random.randrange(-90, 90))
        
    
    '''
    #Randomly Generate Location
    x1 = float(random.randrange(0,48)) * 0.01
    x2 = float(random.randrange(0,48)) * 0.01
    y1 = float(random.randrange(0,48)) * 0.01
    y2 = float(random.randrange(0,48)) * 0.01
    '''



    '''
    x1, x2 = multiRandomNegate(x1, x2)
    y1, y2 = multiRandomNegate(y1, y2)
    '''
    
    '''
    #Randomly Negate Coordinates
    x1 = randomNegate(x1)
    x2 = randomNegate(x2)
    y1 = randomNegate(y1)
    y2 = randomNegate(y2)


    #Round Coordinates
    x1 = round(x1, 3)
    x2 = round(x2, 3)
    y1 = round(y1, 3)
    y2 = round(y2, 3)
    '''
    
    

    #print(x1)
    #print(y1)
    
    #print(x2)
    #print(y2)


    ia.seed(1)
    
    #Augment Picture
    seq = iaa.Sequential([

        #translate by 40/60px on x/y axis, and scale to 50-70%, affects BBs
        iaa.Affine(
            translate_percent={"x": (x1, x2), "y": (y1, y2)},
            scale=(size),
            rotate=(rot)
            )

        #,

        #iaa.Affine(rotate=(rot))
    ])


    return seq, x1, y1


def setAfterAugmentation(seqAug):

    ia.seed(1)

    '''
    #Augment Picture
    seq = iaa.Sequential([

        #change brightness, doesn't affect BBs
        iaa.Multiply((1.2, 1.5))

    ])
    '''

    seq = seqAug

    return seq


def augmentImage(bbs, image, seq, boxCoordinates, overlapCoordinates, after):

    boxCoordinatesAfter = {}
    overlapCoordinatesAfter = {}

    
    # Augment BBs and images.
    image_aug, bbs_aug = seq(image=image, bounding_boxes=bbs)

    if after == False:
        # print coordinates before/after augmentation (see below)
        # use .x1_int, .y_int, ... to get integer coordinates
        for i in range(len(bbs.bounding_boxes)):
            before = bbs.bounding_boxes[i]
            after = bbs_aug.bounding_boxes[i]

            '''
            print("BB %d: (%.4f, %.4f, %.4f, %.4f) -> (%.4f, %.4f, %.4f, %.4f)" % (
                i,
                before.x1, before.y1, before.x2, before.y2,
                after.x1, after.y1, after.x2, after.y2)
            )
            '''

            

            oldCoord = [before.x1, before.y1, before.x2, before.y2]
            newCoord = [after.x1, after.y1, after.x2, after.y2]


            '''
            newOldCoords = []
            for x in oldCoord:
                newOldCoords.append(int(x))

            oldCoord = newOldCoords

            newNewCoords = []
            for x in newCoord:
                newNewCoords.append(int(x))

            newCoord = newNewCoords
            '''

            if i == 0:
                for x in boxCoordinates:

                    #if str(boxCoordinates[x]) == str(oldCoord):
                        
                    boxCoordinatesAfter[x] = newCoord

            if i == 1:
                for x in overlapCoordinates:

                    #if str(overlapCoordinates[x]) == str(oldCoord):
                        
                    overlapCoordinatesAfter[x] = newCoord
    else:
        boxCoordinatesAfter = boxCoordinates.copy()
        overlapCoordinatesAfter = overlapCoordinates.copy()
                
    return image_aug, boxCoordinatesAfter, overlapCoordinatesAfter


def findOutputDirectory(directoryName):

    #cwd = os.getcwd()

    cwd = 'D:\\MachineLearningDataset'
    
    if os.path.exists(cwd + '\\' + directoryName):
        output = cwd + '\\' + directoryName
        return output
    else:
        output = os.makedirs(cwd + '\\' + directoryName)
        output = cwd + '\\' + directoryName
        return output
    

def checkName(name, output):
#Checks for names of files in output directory until it finds one that is available

    sameNr = 0

    foundName = 1

    while foundName == 1:

        saveName = output + "\\" + name + str(sameNr) + '.JPG'

        if os.path.isfile(saveName):
            sameNr = sameNr + 1
        else:
            return sameNr


def saveAugmentedImage(image, imageName, output):

    #image_save = Image.fromarray(image)
    image_save = image

    useNr = checkName(imageName, output)

    image_save.save(output + "\\" + imageName + str(useNr) + '.JPG')
    
    imageActName = imageName + str(useNr) + '.JPG'

    return imageActName


def makeAugmentedLabel(output, imageFileName, bndboxCoordinates, objectNames):

    
    template =  """
<annotation>
    <folder>FOLDERNAME</folder>
    <filename>FILENAME</filename>
    <path>PATH</path>
    <source>
            <database>Unknown</database>
    </source>
    <size>
            <width>3264</width>
            <height>2448</height>
            <depth>3</depth>
    </size>
    <segmented>0</segmented>
    BOX
</annotation>"""

    
    folder = os.path.basename(output)
    fileName = imageFileName
    path = output + "\\" + imageFileName

    #width
    #height
    
    template = template.replace("FILENAME", fileName)
    template = template.replace("PATH", path)
    template = template.replace("FOLDERNAME", folder)
    
    cardName = imageFileName.replace(".JPG", "")

    for x in bndboxCoordinates:

        xmin = bndboxCoordinates[x][0]
        ymin = bndboxCoordinates[x][1]
        xmax = bndboxCoordinates[x][2]
        ymax = bndboxCoordinates[x][3]


        bndboxTemplateOriginal = """
    <object>
        <name>CARDNAME</name>
        <pose>Unspecified</pose>
        <truncated>0</truncated>
        <difficult>0</difficult>
        <bndbox>
                <xmin>XMIN</xmin>
                <ymin>YMIN</ymin>
                <xmax>XMAX</xmax>
                <ymax>YMAX</ymax>
        </bndbox>
    </object>
    BOX"""

        
        bndboxTemplate = bndboxTemplateOriginal
        '''
        #Fix and update this here by using the "make objectNames useful" function made earlier
        print(objectNames)
        for x in objectNames:
             val = objectNames[x]             
             newName = x.replace(str(val), '')
             del objectNames[x]
             objectNames[newName] = val
        print(objectNames)
             
        objectName = x.replace(str(objectNames[x]), '')
        '''
        objectName = x

        bndboxTemplate = bndboxTemplate.replace("CARDNAME", objectName)
        
        bndboxTemplate = bndboxTemplate.replace("XMIN", str(xmin))
        bndboxTemplate = bndboxTemplate.replace("YMIN", str(ymin))
        bndboxTemplate = bndboxTemplate.replace("XMAX", str(xmax))
        bndboxTemplate = bndboxTemplate.replace("YMAX", str(ymax))



        template = template.replace("BOX", bndboxTemplate)

    template = template.replace("BOX", '')

    with open(output + "\\" + imageFileName.replace(".JPG", "") + ".txt", "w") as textFile:
        textFile.write(template)

    p = Path(output + "\\" + imageFileName.replace(".JPG", "") + ".txt")
    p.rename(p.with_suffix('.xml'))


def bbsMaker(bndboxDraw, image):


    start = "bbs = "
    bndboxDraw = bndboxDraw.replace(start, '')

    exec('bbs = ' + bndboxDraw, locals(), globals())

    return bbs



def checkOutBounds(augmentedImage, bndboxCoordinatesAfter):

    width, height = augmentedImage.size
    
    bndOut = False

    for x in bndboxCoordinatesAfter:
        box = bndboxCoordinatesAfter[x]
        
        
        for y in box:

            #print(y)
            
            #print(box.index(y))

            if box.index(y) == 0 or box.index(y) == 2:
                #print('X')

                if y < 0 or y > width:
                    bndOut = True


            if box.index(y) == 1 or box.index(y) == 3:
                #print('Y')
            
                if y < 0 or y > height:
                    bndOut = True


    if bndOut:
        #print('Out')
        return True


    return False





def augmentInBounds(imagesB, labelsB, dirNameB, backgroundImgB, bbsB, imageB, bndboxDrawB, bndboxCoordinatesB, objectNamesB, bndboxAmountB, labelB, nameImageB, overlapCoordinatesB, seqAugB):

    images = imagesB.copy()
    labels = labelsB
    dirName = dirNameB
    backgroundImg = backgroundImgB
    bbs = bbsB
    image = imageB
    bndboxDraw = bndboxDrawB
    bndboxCoordinates = bndboxCoordinatesB
    objectNames = objectNamesB
    bndboxAmount = bndboxAmountB
    label = labelB
    nameImage = nameImageB
    overlapCoordinates = overlapCoordinatesB
    seqAug = seqAugB



    #setTestAugmentation(imagesB, labelsB, dirNameB, backgroundImgB, bbsB, imageB, bndboxDrawB, bndboxCoordinatesB, objectNamesB, bndboxAmountB, labelB, nameImageB, overlapCoordinatesB, seqAugB)

    #f
    

    #Get Augmentation Spesifications
    modifications, xCoord1, yCoord1 = setMaskAugmentation(backgroundImg, {})
    
    #Augment Image
    augmentedImage, bndboxCoordinatesAfter, overlapCoordinatesAfter = augmentImage(bbs, image, modifications, bndboxCoordinates, overlapCoordinates, False)


    #Convert and mask paste mask and background together
    imgT = Image.fromarray(augmentedImage, 'RGBA')
    maskedImage = maskAugment(imgT, bImg)

    #maskedImage.show()

    
    
    #Get Output Directory
    #outputDir = findOutputDirectory('BackgroundMaskedImages')
    
    #Save Image
    #imageActName = saveAugmentedImage(maskedImage, nameImage, outputDir)

    #Make Label for Augmented Image
    #makeAugmentedLabel(outputDir, imageActName, bndboxCoordinatesAfter, objectNames)



    #Generate new bounding box coordinate object with the augmented mask image boundingbox data
    bndboxDraw, bndboxCoordinates, objectNames = getBndbox(bndboxAmount, dirName, bndboxCoordinatesAfter, objectNames)

    maskedImage = np.asarray(maskedImage)

    #Make new bounding box object
    bbs = bbsMaker(bndboxDraw, maskedImage)


    modifications = setAfterAugmentation(seqAug)
    
    augmentedImage, bndboxCoordinatesAfter, overlapCoordinatesAfter = augmentImage(bbs, maskedImage, modifications, bndboxCoordinates,overlapCoordinates, True)

    augmentedImage = Image.fromarray(augmentedImage)


    #print(checkOutBounds(augmentedImage, bndboxCoordinatesAfter))


    if checkOutBounds(augmentedImage, bndboxCoordinatesAfter):
        return augmentInBounds(imagesB, labelsB, dirNameB, backgroundImgB, bbsB, imageB, bndboxDrawB, bndboxCoordinatesB, objectNamesB, bndboxAmountB, labelB, nameImageB, overlapCoordinatesB, seqAugB)
    else:
        #print('Found One')
        return augmentedImage, bndboxCoordinatesAfter, objectNames


def checkOverlap(multiCoord, multiOverlap):
    
    overlap = False

    firstCoords = []
    secondCoords = []
    for x in multiCoord:

        for y in multiOverlap:

            if x != y:

                #print(x + ' ' + y)

                secondCoords = multiCoord[x]
                firstCoords = multiOverlap[y]
                
                #print(firstCoords)
                #print(secondCoords)


                if (((secondCoords[0] > firstCoords[0]) and (secondCoords[0] < firstCoords[2])) or ((secondCoords[2] < firstCoords[2]) and (secondCoords[2] > firstCoords[0]))) and (((secondCoords[1] > firstCoords[1]) and (secondCoords[1] < firstCoords[3])) or ((secondCoords[3] < firstCoords[3]) and (secondCoords[3] > firstCoords[1]))):
                    overlap = True
                    #print('Overlap')


    return overlap





    
    '''
    #If x1 on second bndbox is greater than the x1 of the first while also smaller than x2 of the first, then x values are overlapping
    #If x2 on second bndbox is smaller than the x2 of the first while also greater than x1 of the first, then x values are overlapping
    if (((secondCoords[0] > firstCoords[0]) and (secondCoords[0] < firstCoords[2])) or ((secondCoords[2] < firstCoords[2]) and (secondCoords[2] > firstCoords[0]))) and (((secondCoords[1] > firstCoords[1]) and (secondCoords[1] < firstCoords[3])) or ((secondCoords[3] < firstCoords[3]) and (secondCoords[3] > firstCoords[1]))):
        print('Overlap')
        return True
    else:
        print('No Overlap')
        return False
    '''



def multiMask(imagesB, labelsB, nameImageB, maskedImageB, bndboxCoordinatesB, bbsB, bndboxCoordinatesAfterB, newCard, card, objectNamesB, multiNr, imagesTemp, multiCoordinates, firstTime, nameCard, multiOverlapCoordinates, overlapCoordinatesB, overlapCoordinatesAfterB, usedMultiCoordinatesB):

    images = imagesB
    labels = labelsB
    bbs = bbsB
    maskedImage = maskedImageB
    bndboxCoordinates = bndboxCoordinatesB
    nameImage = nameImageB
    bndboxCoordinatesAfter = bndboxCoordinatesAfterB
    objectNamesOrg = objectNamesB
    overlapCoordinatesAfter = overlapCoordinatesAfterB
    overlapCoordinates = overlapCoordinatesB
    usedMultiCoordinates = usedMultiCoordinatesB

    
    #print(multiOverlapCoordinates)

    #Hugely akward function made with no sleep
    if firstTime:
        objectNames = objectNamesOrg.copy()
        
        usedMultiCoordinates = {}
        imagesTemp = images.copy()
            
        name = nameImage + '.png'
        del imagesTemp[name]

        #Make objectNames useable
        for x in objectNames:
             val = objectNames[x]             
             newName = x.replace(str(val), '')
             del objectNames[x]
             objectNames[newName] = val

        #Make list of objectNames
        nameObjects = []
        for x in objectNames:
            val = objectNames[x]
            objectName = x + str(val)
            nameObjects.append(objectName)
            
        #Carry existing card over to multi Coordinates Variable
        for x in bndboxCoordinatesAfter:
            if x in nameObjects:
                 val = bndboxCoordinatesAfter[x]
                 newNameVal = objectNamesOrg[x]

                 multiCoordinates[newName] = val

        #Do the same for overlap coordinates
        for x in overlapCoordinatesAfter:
            if x in nameObjects:
                 val = overlapCoordinatesAfter[x]

                 multiOverlapCoordinates[newName] = val

     


    #Get random card's image
    if newCard:     

        #Pick random card image from list not containing previously used cards
        cardsInImage = []
        cardsInImage.append(nameImage)
        
        cardAmount = len(imagesTemp)

        cardNr = random.randrange(0, cardAmount)
        cards = []
        
        for key in imagesTemp.keys():
            cards.append(key)


        cardName = cards[cardNr]
        nameCard = cardName.replace('.png', '')
        nameCardObject = nameCard + '1'
        card = imagesTemp[cardName]

        del imagesTemp[cardName]

    
    #Get Augmentation Spesifications
    modifications, xCoord1, yCoord1 = setMaskAugmentation(maskedImage, usedMultiCoordinates)
    #print(xCoord1)
    #print(yCoord1)



    #Augment Image and Convert and mask paste mask and background together
    augmentedImage, bndboxCoordinatesAfter, overlapCoordinatesAfter = augmentImage(bbs, card, modifications, bndboxCoordinates, overlapCoordinates, False)
    augmentedImage = Image.fromarray(augmentedImage, 'RGBA')
    maskedImage = maskAugment(augmentedImage, maskedImage)

    #print(bndboxCoordinatesAfterB)
    #print(bndboxCoordinatesAfter)

    #Get coords of newly augmented image
    for key in bndboxCoordinatesAfter.keys():
        val = bndboxCoordinatesAfter[key]

    multiCoordinates[nameCard] = val

    for key in overlapCoordinatesAfter.keys():
        val = overlapCoordinatesAfter[key]

    multiOverlapCoordinates[nameCard] = val

    #print(bndboxCoordinates)
    #print(bndboxCoordinatesAfter)
    #print(bndboxCoordinatesAfterB)


    if checkOutBounds(maskedImage, bndboxCoordinatesAfter) or checkOverlap(multiCoordinates, multiOverlapCoordinates):
        return multiMask(imagesB, labelsB, nameImageB, maskedImageB, bndboxCoordinatesB, bbsB, bndboxCoordinatesAfterB, False, card, objectNamesB, multiNr, imagesTemp, multiCoordinates, False, nameCard, multiOverlapCoordinates, overlapCoordinatesB, overlapCoordinatesAfterB, usedMultiCoordinates)
    else:
        #print(xCoord1)
        #print(yCoord1)
        #print('Success ' + str(multiNr) + ' Cards Left')
        usedMultiCoordinates[len(usedMultiCoordinates)] = [xCoord1, yCoord1]
        #print(usedMultiCoordinates)
        multiNr = multiNr -1
        if multiNr == 0:
            #print('Done')
            #print()
            '''
            #maskedImage.show()
            testImage = maskedImage.copy()

            draw = ImageDraw.Draw(testImage)

            for x in multiOverlapCoordinates:
                listTemp = multiOverlapCoordinates[x]

                draw.rectangle((listTemp[0], listTemp[1], listTemp[2],listTemp[3]), fill=(0, 0, 155), outline=(255, 255, 255))

            for x in multiCoordinates:
                listTemp = multiCoordinates[x]

                draw.rectangle((listTemp[0], listTemp[1], listTemp[2],listTemp[3]), fill=(50, 50, 50), outline=(255, 255, 255))
                
                
            #testImage.show()
            '''

            return maskedImage, multiCoordinates, multiOverlapCoordinates
        else:
            #If desired number of cards not reached, run function again with previous image image until desired number is reached
            return multiMask(imagesB, labelsB, nameCard, maskedImage, bndboxCoordinatesB, bbsB, bndboxCoordinatesAfterB, True, card, objectNamesB, multiNr, imagesTemp, multiCoordinates, False, nameCard, multiOverlapCoordinates, overlapCoordinatesB, overlapCoordinatesAfterB, usedMultiCoordinates)
        
    

#Check that the cards don't overlap eachother


def multiAugmentInBounds(imagesB, labelsB, dirNameB, backgroundImgB, bbsB, imageB, bndboxDrawB, bndboxCoordinatesB, objectNamesB, bndboxAmountB, labelB, nameImageB, overlapCoordinatesB, seqAugB, multiNrB):

    images = imagesB
    labels = labelsB
    dirName = dirNameB
    backgroundImg = backgroundImgB
    bbs = bbsB
    image = imageB
    bndboxDraw = bndboxDrawB
    bndboxCoordinates = bndboxCoordinatesB
    objectNames = objectNamesB
    bndboxAmount = bndboxAmountB
    label = labelB
    nameImage = nameImageB
    overlapCoordinates = overlapCoordinatesB
    multiNr = multiNrB
    seqAug = seqAugB
    
    

    #Get Augmentation Spesifications
    modifications, xCoord1, yCoord1 = setMaskAugmentation(backgroundImg, {})

    #Augment Image
    augmentedImage, bndboxCoordinatesAfter, overlapCoordinatesAfter = augmentImage(bbs, image, modifications, bndboxCoordinates, overlapCoordinates, False)


    #Convert and mask paste mask and background together
    imgT = Image.fromarray(augmentedImage, 'RGBA')
    
    maskedImage = maskAugment(imgT, bImg)

    #maskedImage.show()
    #maskedImage = np.asarray(maskedImage)


    if checkOutBounds(maskedImage, bndboxCoordinatesAfter):
        return multiAugmentInBounds(imagesB, labelsB, dirNameB, backgroundImgB, bbsB, imageB, bndboxDrawB, bndboxCoordinatesB, objectNamesB, bndboxAmountB, labelB, nameImageB, overlapCoordinates, seqAugB, multiNrB)
    else:
        

        #maskedImage.show()


        #Add other images to already single masked image 1 initial + multiNr extra        
        multiMaskedImage, multiCoordinates, multiOverlapCoordinates = multiMask(images, labels, nameImage, maskedImage, bndboxCoordinates, bbs, bndboxCoordinatesAfter, True, None, objectNames, multiNr, [], {}, True, '', {}, overlapCoordinates, overlapCoordinatesAfter, {})
            
        #Problem is something here where all cards are unified

        maskedImage = multiMaskedImage.copy()

        #maskedImage.show()
        maskedImage = np.asarray(maskedImage)

        #Generate new bounding box coordinate object with the augmented mask image boundingbox data
        bndboxDraw, bndboxCoordinates, objectNames = getBndbox(bndboxAmount, dirName, multiCoordinates, objectNames)
        #bndboxDraw, bndboxCoordinates, objectNames = getBndbox(bndboxAmount, dirName, bndboxCoordinatesAfter, objectNames)


        #Make new bounding box object
        bbs = bbsMaker(bndboxDraw, maskedImage)


        modifications = setAfterAugmentation(seqAug)

        
        augmentedImage, bndboxCoordinatesAfter, overlapCoordinatesAfter = augmentImage(bbs, maskedImage, modifications, bndboxCoordinates, overlapCoordinates, True)

        augmentedImage = Image.fromarray(augmentedImage)



        return augmentedImage, bndboxCoordinatesAfter, objectNames




    
def augment(firstImage, images, labels, dirName, backgroundImg, seqAug, multiNr):

    #Find xml file beloning to first image, Input Image Name and Label List, returns xml Label File


    #Find XML file belonging to Image
    label, nameImage = findXMLforImage(firstImage, labels)

    
    #Change this

    #Get amount of boundingboxes on image according to xml, Input xml Label File, Returns int of Amount of Bndboxes
    bndboxAmount = getBndboxAmount(label, dirName)
    
    #Get boundingbox coordinates and save them for augmentation, Input int of Amount of Bndboxes and xml Label File, Returns String Draw Bndboxes on Image Function with Coordinates
    bndboxDraw, bndboxCoordinates, objectNames, overlapCoordinates = getBndboxCoordinates(bndboxAmount, label, dirName)


    #Fix missing bounding box data on end picture
    #Add folder for each card and switch effect and background

    #Set Image and Draw Bndboxes on it
    image = images[firstImage]
    
    bbs = bbsMaker(bndboxDraw, image)


    if multiNr == 0:
        multiAug = False
    else:
        multiAug = True

    #Either multi or single augment image
    if multiAug:
        augmentedImage, bndboxCoordinatesAfter, objectNames = multiAugmentInBounds(images, labels, dirName, backgroundImg, bbs, image, bndboxDraw, bndboxCoordinates, objectNames, bndboxAmount, label, nameImage, overlapCoordinates, seqAug, multiNr)
    else:    
        augmentedImage, bndboxCoordinatesAfter, objectNames = augmentInBounds(images, labels, dirName, backgroundImg, bbs, image, bndboxDraw, bndboxCoordinates, objectNames, bndboxAmount, label, nameImage, overlapCoordinates, seqAug)

    #Get Output Directory
    outputName = firstImage.replace('.png', '')
    outputDir = findOutputDirectory(outputName)

    #print(bndboxCoordinatesAfter)

    #Save Image
    imageActName = saveAugmentedImage(augmentedImage, nameImage, outputDir)

    #Make Label for Augmented Image
    makeAugmentedLabel(outputDir, imageActName, bndboxCoordinatesAfter, objectNames)  



def getBackground():

    cwd = os.getcwd()

    objC = 0

    for root, dirs, files in os.walk(cwd + '\\' + 'BackgroundImages'):
        for file in files:

            if file.endswith('.jpg'):
                fileStr = file.replace('.jpg', '')
                endStr = fileStr[-5:]
                dirName = fileStr.replace(endStr, '')
                
                if objC == 0:
                    objC = objC + 1;

                    img_1 = Image.open(cwd + '\\' + 'BackgroundImages' + '\\' + dirName + '\\' + file)

                    return img_1


def getBackgrounds():

    cwd = os.getcwd()
    path = cwd + '\\' + 'BackgroundImages'

    backgroundDir = {}
    backgroundImages = []

    first = True


    for root, dirs, files in os.walk(path):
        for dire in dirs:
            
            if first:
                currentDire = dire
                first = False

            if dire == currentDire:

                dirPath = path + '\\' + dire
                
                for root, dirs, files in os.walk(path + '\\' + dire):
                    for file in files:
                        print(file)

                        #print('BackgroundImages' + '\\' + dire + '\\' + file)

                        backgroundImages.append('BackgroundImages' + '\\' + dire + '\\' + file)

                    
            else:
                backgroundDir[currentDire] = backgroundImages
                backgroundImages = []

                currentDire = dire

                for root, dirs, files in os.walk(path + '\\' + dire):
                    for file in files:

                        #print('BackgroundImages' + '\\' + dire + '\\' + file)

                        backgroundImages.append('BackgroundImages' + '\\' + dire + '\\' + file)
               
    return backgroundDir

            


def maskAugment(firstImage, backgroundImg):

    img_2 = firstImage
    img_1 = backgroundImg
    
    img_1 = img_1.resize((3264, 2448))

    #img_1.paste(img_2, (148, 315), mask=img_2)
    img_1.paste(img_2, (0, 0), mask=img_2)
    return img_1



















#For each card, do on each background with each 1-12 extra cards and with each different effect

#Find all Images and Labels, Returns Dict of Image Name and Image Array, and List of Labels
images, labels, dirName = getFiles()

cwd = os.getcwd()

backgroundImages = getBackgrounds()

print(backgroundImages)


#List of Effects
def randomizeAugmentationValues():
    seqAugments = []

    val = random.randrange(1, 6)
    if val == 5:
        #Darken and Brighten
        val = random.uniform(0.5, 2)
        effect = 'iaa.Multiply(('+str(val)+'))'
        seqAugments.append(effect)
        
    '''
    val = random.randrange(1, 6)
    if val == 5:
        #Add MotionBlur
        val1 = random.randrange(-45, 45)
        val2 = random.randrange(10, 30)
        effect = 'iaa.MotionBlur(k='+str(val2)+', angle=['+str(val1)+'])'
        seqAugments.append(effect)
    '''

    val = random.randrange(1, 6)
    if val == 5:
        #Add DefocusBlur
        val = random.randrange(1, 4)
        effect = 'iaa.imgcorruptlike.DefocusBlur(severity='+str(val)+')'
        seqAugments.append(effect)    

    val = random.randrange(1, 6)
    if val == 5:
        #Change Colour Temperature    
        val = random.randrange(1000,15000)
        effect = 'iaa.ChangeColorTemperature('+str(val)+')'
        seqAugments.append(effect)

    val = random.randrange(1, 6)
    if val == 5:
        #Change Contrast
        val = random.uniform(1.0, 3.0)
        effect = 'iaa.LinearContrast(('+str(val)+'))'
        seqAugments.append(effect)

    
    return seqAugments


print(cwd)

amount = 0

#Get Image
for y in range(0, 2):
    for x in images:

        print('\nNew Primary Card\n')
        firstImage = x
#Get Image
    

#Get Background
        for y in backgroundImages:

            for z in backgroundImages[y]:

                print('\nNew Background\n')
                bImg = Image.open(cwd + '\\' + z)            
#Get Background


#Set Amount of Cards Per Card Per Background Per Effect to make
                
                card_Amount = 13

                for i in range(0, card_Amount):
                    #print(i)
                    #multiNr = 0
                    multiNr = i

                    #Make After Augment Effect
                    seqAugments = randomizeAugmentationValues()

                    seqAugVar ='''
seqAug = iaa.Sequential([

    LINE

])
''' 
                    for a in seqAugments:
                        seqAugVar = seqAugVar.replace('NEXT', ',')
                        seqAugVar = seqAugVar.replace('LINE',a + 'NEXT' + '\n'.ljust(5) + 'LINE')


                    seqAugVar = seqAugVar.replace('NEXT', '')
                    seqAugVar = seqAugVar.replace('LINE', '')

                    exec(seqAugVar)
                    #Make After Augment Effect                  

                    augment(firstImage, images, labels, dirName, bImg, seqAug, multiNr)

                    amount = amount + 1
                    print(str(amount) + ' Cards')


#Set Amount of Cards Per Card Per Background Per Effect to make
            




            

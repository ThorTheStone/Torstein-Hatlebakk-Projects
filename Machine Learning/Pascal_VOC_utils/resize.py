from PIL import Image
import os
import os.path
import re

import xml.etree.ElementTree



#Find center of image
def crop_center(pil_img, crop_width, crop_height):
    img_width, img_height = pil_img.size
    return pil_img.crop(((img_width - crop_width) // 2,
                         (img_height - crop_height) // 2,
                         (img_width + crop_width) // 2,
                         (img_height + crop_height) // 2))

#Crop a square
def crop_max_square(pil_img):

    return crop_center(pil_img, min(pil_img.size), min(pil_img.size))



cwd = os.getcwd()

amount = 0

files = [f for f in os.listdir('.') if os.path.isfile(f)]

for root, dirs, files in os.walk(cwd):
    
    for file in files:

        fileName = file


        if 'JPG' in fileName:

            #print(fileName)
        
            image = Image.open(fileName)

            scale = 416
            last_scale = 640

            im = crop_max_square(image)

            im = im.resize((scale, scale))
            
            #print(im.size)

            #im.show()

            #fileName = fileName.replace('JPG', 'jpg')
                        
            im.save(fileName)




        if 'xml' in fileName:

            xml = fileName
            
            inFile = open(xml, 'r')
            data = inFile.readlines()
            inFile.close()

            newData = []

            for line in data:

                #Change Size ########################################################
                if '<width>' in line:

                    line = line.replace('<width>', '')                
                    line = line.replace('</width>', '')

                    fold = line

                    folde = []
                    noWhite = True
                    
                    for char in fold:

                        if noWhite == True:

                            if char == ' ':
                                pass
                            else:
                                folde.append(char)
                                noWhite = False
                        else:
                            folde.append(char)

                    fold = ''.join(folde)

                    #print(scale)
                    #print(fold)
                    #x_scale = round(float(scale)/float(fold))
                    x_scale = scale/last_scale
                    
                    line = line.replace(fold,'<width>'+str(scale)+'</width>'+'\n')

                if '<height>' in line:

                    line = line.replace('<height>', '')                
                    line = line.replace('</height>', '')

                    fold = line

                    folde = []
                    noWhite = True
                    
                    for char in fold:

                        if noWhite == True:

                            if char == ' ':
                                pass
                            else:
                                folde.append(char)
                                noWhite = False
                        else:
                            folde.append(char)

                    fold = ''.join(folde)

                    #print(scale)
                    #print(fold)
                    #y_scale = round(float(scale)/float(fold))
                    y_scale = scale/last_scale
                    
                    line = line.replace(fold,'<height>'+str(scale)+'</height>'+'\n')
                    ####################################################################



                offsetVal = 0
                
                #Stats
                tag = 'xmin'
                if '<'+tag+'>' in line:

                    line = line.replace('<'+tag+'>', '')                
                    line = line.replace('</'+tag+'>', '')

                    fold = line

                    folde = []
                    noWhite = True
                    
                    for char in fold:

                        if noWhite == True:

                            if char == ' ':
                                pass
                            else:
                                folde.append(char)
                                noWhite = False
                        else:
                            folde.append(char)

                    fold = ''.join(folde)
                    #print(fold)

                    newVal = int(float(fold)*x_scale)

                    #percent = float(((newVal-0)*100)/(640-0))

                    #print('Percent ' + str(percent))

                    #offset = (offsetVal * percent)/100

                    #newVal = newVal - offset
                    #newVal = newVal - 108

                    line = line.replace(fold,'<'+tag+'>'+str(newVal)+'</'+tag+'>'+'\n')


                tag = 'ymin'
                if '<'+tag+'>' in line:

                    line = line.replace('<'+tag+'>', '')                
                    line = line.replace('</'+tag+'>', '')

                    fold = line

                    folde = []
                    noWhite = True
                    
                    for char in fold:

                        if noWhite == True:

                            if char == ' ':
                                pass
                            else:
                                folde.append(char)
                                noWhite = False
                        else:
                            folde.append(char)

                    fold = ''.join(folde)

                    newVal = int(float(fold)*y_scale)
                    
                    line = line.replace(fold,'<'+tag+'>'+str(newVal)+'</'+tag+'>'+'\n')
                    








                tag = 'xmax'
                if '<'+tag+'>' in line:

                    line = line.replace('<'+tag+'>', '')                
                    line = line.replace('</'+tag+'>', '')

                    fold = line

                    folde = []
                    noWhite = True
                    
                    for char in fold:

                        if noWhite == True:

                            if char == ' ':
                                pass
                            else:
                                folde.append(char)
                                noWhite = False
                        else:
                            folde.append(char)

                    fold = ''.join(folde)
                    
                    newVal = int(float(fold)*x_scale)
                    
                    #percent = float(((newVal-0)*100)/(640-0))

                    #offset = (offsetVal * percent)/100

                    #newVal = newVal - offset
                    #newVal = newVal - 108


                    
                    line = line.replace(fold,'<'+tag+'>'+str(newVal)+'</'+tag+'>'+'\n')


                tag = 'ymax'
                if '<'+tag+'>' in line:

                    line = line.replace('<'+tag+'>', '')                
                    line = line.replace('</'+tag+'>', '')

                    fold = line

                    folde = []
                    noWhite = True
                    
                    for char in fold:

                        if noWhite == True:

                            if char == ' ':
                                pass
                            else:
                                folde.append(char)
                                noWhite = False
                        else:
                            folde.append(char)

                    fold = ''.join(folde)
                    
                    newVal = int(float(fold)*y_scale)

                    line = line.replace(fold,'<'+tag+'>'+str(newVal)+'</'+tag+'>'+'\n')
                    



                #End

                

                newData.append(line)
            
            nextLine = ''
            obj = True
            skipNext = False
            out = False
            finalData = []
            for line in newData:
                #print(line)

                if skipNext == True:
                    skipNext = False
                    continue

                if 0 == newData.index(line) and '<annotation>' not in line:
                    continue

                if '</segmented>' in line:
                    skipNext = True

                if '</object>' in line:
                    checkLine = newData.index(line)
                    nextLine = newData[checkLine+1]

                    

                if obj:
                    if '<object>' in line:
                        objectData = []
                        objectData.append(line)
                        obj = False
                    else:
                        finalData.append(line)
                else:
                    if line == nextLine:

                        pass
                    else:
                    
                        objectData.append(line)

                        if '<xmin>' in line:
                            
                            line = line.replace('<xmin>', '')                
                            line = line.replace('</xmin>', '')

                            fold = line

                            folde = []
                            noWhite = True
                            
                            for char in fold:

                                if noWhite == True:

                                    if char == ' ':
                                        pass
                                    else:
                                        folde.append(char)
                                        noWhite = False
                                else:
                                    folde.append(char)

                            fold = ''.join(folde)

                            if int(fold) > scale or int(fold) < 0:
                                out = True
                                

                        if '<xmax>' in line:
                            
                            line = line.replace('<xmax>', '')                
                            line = line.replace('</xmax>', '')

                            fold = line

                            folde = []
                            noWhite = True
                            
                            for char in fold:

                                if noWhite == True:

                                    if char == ' ':
                                        pass
                                    else:
                                        folde.append(char)
                                        noWhite = False
                                else:
                                    folde.append(char)

                            fold = ''.join(folde)

                            if int(fold) > scale or int(fold) < 0:
                                out = True

                        if '</object>' in line:

                            if out == True:
                                objectData = []
                                out = False
                                obj = True
                            else:
                                for i in objectData:
                                    finalData.append(i)
                                objectData = []

                            
            annote = True
            for line in finalData:
                if '</annotation>' in line:
                    annote = False

            if annote:
                finalData.append('</annotation>')


            os.remove(xml)
                        
            outFile = open(xml, 'w')
            outFile.writelines(finalData)
            outFile.close()

        if '.py' not in file:
            amount = amount + 1
            print(amount)













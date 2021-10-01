import os
import os.path
from PIL import Image


cwd = os.getcwd()
count = 0
bigList = []

thresh = 70

files = [f for f in os.listdir('.') if os.path.isfile(f)]

for root, dirs, files in os.walk(cwd):

    for file in files:



        if '.JPG' in file:
            image = Image.open(file)

            width, height = image.size

            print(width, height)

            if width != 416:
                #print('Wrong Width')
                bigList.append(file)
            
            if height != 416:
                #print('Wrong Height')
                bigList.append(file)                
        
        if '.xml' in file:
            #print(file)


            inFile = open(file, 'r')
            data = inFile.readlines()
            inFile.close()

            for line in data:
                #print(line)


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

                    xmin = fold
                    #print(fold)


                #Stats
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

                    xmax = fold
                    #print(fold)
                    
                    difference = abs(int(float(xmax.replace('\n', ''))) - int(float(xmin.replace('\n', ''))))
                    if difference > thresh:
                        print('Big X', difference, file)
                        bigList.append(file)

                #Stats
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

                    ymin = fold
                    #print(fold)


                #Stats
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

                    ymax = fold
                    #print(fold)
                    
                    difference = abs(int(float(xmax.replace('\n', ''))) - int(float(xmin.replace('\n', ''))))
                    if difference > thresh:
                        print('Big Y', difference, file)
                        bigList.append(file)

            count = count +1
            print(count)

print('All\n')
for i in bigList:
    print(i)

                    

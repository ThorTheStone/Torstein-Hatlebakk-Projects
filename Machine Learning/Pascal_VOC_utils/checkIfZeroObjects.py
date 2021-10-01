import os
import os.path


count = 0

zeroList = []
zeroNameList = []

cwd = os.getcwd()

files = [f for f in os.listdir('.') if os.path.isfile(f)]

for root, dirs, files in os.walk(cwd):

    for file in files:
        
        
        if 'xml' in file:

            #print(file)



            inFile = open(file, 'r')
            data = inFile.readlines()
            inFile.close()

            amount = 0

            for line in data:

                if '<object>' in line:
                    amount = amount + 1

            if amount == 0:
                print(file)
                zeroList.append(file)
                zeroNameList.append(file.replace('.xml', ''))

            count = count +1
            print(count)
                    
print(zeroList)


for root, dirs, files in os.walk(cwd):

    for file in files:
        
        
        if '.JPG' in file:
            print(file)

            if file.replace('.JPG', '') in zeroNameList:
                    zeroList.append(file)
            



for file in zeroList:
    os.remove(file)

























        

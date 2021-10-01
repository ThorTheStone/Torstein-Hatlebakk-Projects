import os
import os.path

import xml.etree.ElementTree




cwd = os.getcwd()


print(cwd)
print(os.path.basename(cwd))
amount = 0

files = [f for f in os.listdir('.') if os.path.isfile(f)]

for root, dirs, files in os.walk(cwd):
    for file in files:

        fileName = file


            

        if 'xml' in fileName:

            xml = fileName

            inFile = open(xml, 'r')
            data = inFile.readlines()
            inFile.close()

            newData = []

            for line in data:

                if '<folder>' in line:

                    line = line.replace('<folder>', '')                
                    line = line.replace('</folder>', '')

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

                    line = line.replace(fold,'<folder>'+os.path.basename(cwd)+'</folder>'+'\n')
        
                    

                if '<path>' in line:

                    line = line.replace('<path>', '')                
                    line = line.replace('</path>', '')

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

                    xmlName = xml.replace('.xml', '.JPG')

                    line = line.replace(fold,'<path>'+cwd+'\\'+xmlName+'</path>'+'\n')
                    

                    
                newData.append(line)

            # some manipulation on `data`

            os.remove(xml)
                        
            outFile = open(xml, 'w')
            outFile.writelines(newData)
            outFile.close()

        if '.py' not in file:
            amount = amount + 1
            print(amount)
            

                    
            



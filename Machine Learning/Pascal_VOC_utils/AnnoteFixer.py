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

                if '</annotation></annotation>' in line:

                    line = line.replace('</annotation></annotation>', '</annotation>')                

                    
                newData.append(line)

            # some manipulation on `data`

            os.remove(xml)
                        
            outFile = open(xml, 'w')
            outFile.writelines(newData)
            outFile.close()

        if '.py' not in file:
            amount = amount + 1
            print(amount)
            

                    
            



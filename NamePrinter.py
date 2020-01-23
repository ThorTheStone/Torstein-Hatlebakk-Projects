import random
import string

def deList(string): 
  
    stringName = "" 
    for i in string: 
        stringName += i   
    return stringName 

#Print my first name and last name with a normal for loop and predefined string values
for i in range(2):
    if i == 0:
        print("Torstein")
    elif i == 1:
        print("Hatlebakk")

#Over convelutedly make a string of the alphabet and get numerical values of the letters -1 of my name and last name and then convert the list to a string, because why not
alpha = list(string.ascii_lowercase)
print("")

name = []

name.append(alpha[20-1])
name.append(alpha[15-1])
name.append(alpha[18-1])
name.append(alpha[19-1])
name.append(alpha[20-1])
name.append(alpha[5-1])
name.append(alpha[9-1])
name.append(alpha[14-1])

print(deList(name).capitalize())

name = []

name.append(alpha[8-1])
name.append(alpha[1-1])
name.append(alpha[20-1])
name.append(alpha[12-1])
name.append(alpha[5-1])
name.append(alpha[2-1])
name.append(alpha[1-1])
name.append(alpha[11-1])
name.append(alpha[11-1])

print(deList(name).capitalize())

print("")
input("Press Enter to start random name generation...")


#An an extra for fun where it generates a random 8 letter string word where each try has a 1 to 298 827 0064 576 chance of finding my name and will never finish in a practical timeframe
name = []
while i == 1:

    number = random.randrange(1, 26)-1
    letter = alpha[number]

    if len(name) == 8:
        if deList(name) == "torstein":
            print(deList(name).capitalize())
            i == 2
            print("Huh, it somehow worked")
        else:
            print(deList(name).capitalize())
            name = []
    elif letter not in name:
        name.append(letter)

#Same for last name and with 9 letters
name = []
while i == 1:

    number = random.randrange(1, 26)-1
    letter = alpha[number]

    if len(name) == 9:
        if deList(name) == "hatlebakk":
            print(deList(name).capitalize())
            i == 2
            print("Huh, it somehow worked as well")
        else:
            print(deList(name).capitalize())
            name = []
    elif letter not in name:
        name.append(letter)

























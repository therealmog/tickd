from string import ascii_letters
from random import choice
lettersAndNums = ascii_letters + "0123456789"

def create():
    listID = ""
    for each in range(6):
        listID += choice(lettersAndNums)

    print(f'"listID":"{listID}",')

for i in range(5):
    create()
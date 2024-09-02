from random import choice
from string import ascii_letters,ascii_lowercase,ascii_uppercase

def createTaskDict(title,date=None,attributes:dict=None):
    chars = ascii_letters+ascii_uppercase+ascii_lowercase
    taskID = ""
    for each in range(6):
        char = choice(chars)
        taskID+=char

    taskDict = {"title":title,
                "date":"",
                "taskID":taskID,
                "completed":"False"}

    if date is not None:
        taskDict["date"] = date
    if attributes is not None:
        for each in attributes:
            item = attributes[each]
            taskDict[each] = item
    
    return taskDict
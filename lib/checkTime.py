
def checkTime(self,userInput):
    if len(userInput) == 5:
        timeSections = userInput.split(userInput[2])
    elif len(userInput) == 4:
        hour = userInput[0:2]
        minute = userInput[2:]
    else:
        message = "Invalid time entered."
        return False

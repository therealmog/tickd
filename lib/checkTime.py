
def checkTime(userInput):
    if len(userInput) == 5:
        timeSections = userInput.split(userInput[2])
        if len(timeSections) !=2:
            message = "Invalid time entered"
            return False,message
        else:
            hour = timeSections[0]
            minute = timeSections[1]
            time = f"{hour}:{minute}"
            return time,None
        
    elif len(userInput) == 4:
        hour = userInput[0:2]
        minute = userInput[2:]
        time = f"{hour}:{minute}"
        return time,None
    else:
        message = "Invalid time entered."
        return False,message

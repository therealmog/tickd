def checkInt(val):
    try:
        val = int(val)
        return True
    except ValueError:
        return False

def checkTime(userInput):
    # Get input from entry box and remove any whitespace.
    userInput = userInput.strip()

    # Correct format: HH:MM, which is 5 characters
    if len(userInput) == 5:
        # Splits input using third character
        # Allows for use of any delimiter (separating hour and minute)
        timeSections = userInput.split(userInput[2])

        # If there isn't a clear hour and minute
        if len(timeSections) !=2:
            message = "Invalid time entered"

            # Returns error message
            return False,message
        else:
            # Separates hour and minute
            hour = timeSections[0]
            minute = timeSections[1]


    # H:MM (user hasn't inputted a leading zero)
    elif len(userInput) == 4 and userInput[0] != "0" and not checkInt(userInput[1]):
        userInput = "0" + userInput
        print(userInput)

        timeSections = userInput.split(userInput[2])

        # If there isn't a clear hour and minute
        if len(timeSections) !=2:
            message = "Invalid time entered"

            # Returns error message
            return False,message
        else:
            # Separates hour and minute
            hour = timeSections[0]
            minute = timeSections[1]
    
    # Alternative format: HHMM (still valid)
    elif len(userInput) == 4:
        hour = userInput[0:2]
        minute = userInput[2:]

    else:
        message = "Invalid time entered."
        return False,message

    # Program will only reach here if format is valid
    # Otherwise the return will cause a break in the code.

    try:
        if int(hour) > 23:
            message = "Invalid time"
            return False,message
        elif int(minute) > 59:
            message = "Invalid time"
            return False, message
        else:
            time = f"{hour}:{minute}"
        return time,None
    except:
        message = "Invalid time"
        return False,message

    

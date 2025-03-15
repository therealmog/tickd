
import datetime

def checkDate(userInput):
        userInput = userInput.strip()
        userInput = userInput.lower()
        print(userInput)

        # Creates the datetime object to represent today's date.
        today = datetime.date.today()


        if userInput == "today":
            # The date is set to today's object
            # strftime used to generate a string representation of the date.
            date = today.strftime("%d/%m/%Y")
            return date,None # None is for message
        
        elif userInput == "tomorrow":
            # timedelta is used to add an extra day to the object representing today's date.
            tomorrow = today + datetime.timedelta(days=1)

            # Again, strftime used to generate a string representation.
            date = tomorrow.strftime("%d/%m/%Y")
            return date,None # None is for message
        else:
            try:
                # List created by splitting date input string by "/" -> creates [day,month,year]
                dateSections = userInput.split("/")
            except:
                # If the list cannot be split, then an error message is returned.
                message = "Invalid date entered"
                return False,message
            
            try:
                day = dateSections[0]
                month = dateSections[1]
                year = dateSections[2]
            except:
                message = "Invalid date"
                return False,message

            # Checking to see that all sections are integers
            integers = True
            for each in dateSections:
                try:
                    each = int(each)
                except ValueError:
                    integers = False
            
            if not integers:
                # Error message returned.
                message = "Date must be all integers"
                return False,message
            else:
                # Checking year
                if len(year)<=2: # Short year entered (e.g. 11/12/'24')
                    if int(year)<24:
                        message = "Your date cannot be in the past."
                        return False,message
                    else:
                        year = str(2000+int(year))
                elif len(year)==3:
                    message = "Invalid year."
                    return False,message
                else:
                    if int(year)<2024:
                        message = "Your date cannot be in the past."
                        return False,message
                
                # Checking day #
                if int(day)>31:
                    message = "Invalid day entered"
                    return False,message
                elif int(day)>28 and int(month) == 2 and int(year)%4 != 0: 
                    # i.e. day cannot be greater than 28 if month is February and not a leap year
                    message = "Invalid day"
                    return False,message
                else:
                    day = int(day)
                    day = str(day) # Removes any preceding zeros e.g. 05/12/24 -> 5/12/24
                
                # Checking month #
                if int(month)> 12 or int(month)<1:
                    message = "Invalid month"
                    return False,message
                else:
                    month = int(month)
                    month = str(month) #same as with day, to remove preceding zero
                
                try:
                    if datetime.date(int(year),int(month),int(day)) < today:
                        message = "Your due date cannot be in the past."
                        return False,message
                    else:
                        date = f"{day}/{month}/{year}"
                        return date,None # None is for message
                except ValueError:
                    message = "Invalid date entered."
                    return False,message        
                    
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

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
                        year = "20"+year
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
                elif int(day)>28 and int(month) != 2 and int(year)%4 != 0: 
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
                
                if datetime.date(int(year),int(month),int(day)) < today:
                    message = "Your due date cannot be in the past."
                    return False,message
                else:
                    date = f"{day}/{month}/{year}"
                    return date,None # None is for message               
                    
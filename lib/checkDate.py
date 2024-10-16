
import datetime

def checkDate(userInput):
        userInput = userInput.strip()
        userInput = userInput.lower()
        print(userInput)
        today = datetime.date.today()


        if userInput == "today":
            date = today.strftime("%d/%m/%Y")
            return date,None # None is for message
        elif userInput == "tomorrow":
            tomorrow = today + datetime.timedelta(days=1)
            date = tomorrow.strftime("%d/%m/%Y")
            return date,None # None is for message
        else:
            try:
                dateSections = userInput.split("/")
            except:
                message = "Invalid date entered"
                return False,message
            
            try:
                day = dateSections[0]
                month = dateSections[1]
                year = dateSections[2]
            except:
                message = "Invalid date"
                return False,message

            #Checking all to see if they are integers
            integers = True
            for each in dateSections:
                try:
                    each = int(each)
                except ValueError:
                    integers = False,message
            
            if not integers:
                message = "Date must be all integers"
                return False,message
            else:
                # Checking year #
                if len(year)<=2:
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
                elif int(day)>28 and int(month) != 2: #i.e. day cannot be greater than 28 if month is February
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
                    date = f"{day}/{month}/{year}"
                    return date,None # None is for message
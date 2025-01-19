from glob import glob

def checkListName(listName,userPath):
    # First checks if entered list name is prohibited (i.e. default list name) 
    notAccepted = ["inbox","starred","today"]
    for each in notAccepted:
        # Makes direct comparison between list name and disallowed value.
        # However, the input is converted to lower and stripped of whitespace first. 
        if listName.lower().strip() == each:
            message = "Your list name contains a prohibited value in it, please enter another name."
            return False, message
    
    if listName.strip() == "":
        message = "Your list name cannot be empty, please try again."
        return False,message
    
    # Checking new list name is not already present.
    # Uses glob module to find file names with given pattern
    listNames = glob(f"{userPath}//*.json")
    print(listNames)

    for each in listNames:
        each = each.replace(f"{userPath}\\","")
        each = each.replace(".json","")
        if listName.lower() == each.lower():
            message = "This list name has already been used. Please enter a different name."
            return False,message

    # If the program exits out of the for loop, it is assumed that the name is valid.
    return listName,None # no message



from glob import glob

def checkListName(listName,userPath):
    notAccepted = ["inbox","starred","today"]
    for each in notAccepted:
        if listName.lower().strip() == each:
            message = "Your list name contains a prohibited value in it, please enter another name."
            return False, message
    
    if listName.strip() == "":
        message = "Your list name cannot be empty, please try again."
        return False,message
    
    # Checking new list name is not already present.
    listNames = glob(f"{userPath}//*.json")
    print(listNames)

    for each in listNames:
        each = each.replace(f"{userPath}\\","")
        each = each.replace(".json","")
        if listName.lower() == each.lower():
            message = "This list name has already been used. Please enter a different name."
            return False,message


    return listName,None # no message
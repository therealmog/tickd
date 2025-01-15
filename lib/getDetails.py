import json

def getAllDetails():
    with open("authDetails.json","r") as f:
        detailsDict = json.load(f)
        details = detailsDict["details"]
        rememberMeIndex = detailsDict["rememberMe"]

    return details,rememberMeIndex

def getDetailsIndividual(email):
    # Retrieves all details from JSON file.
    details,_ = getAllDetails()

    found = False
    userDetails = []
    i = 0 
    max = len(details)-1
    while not found and max >= i:
        # Each set of details is a list -> [userEmail,userPasswordHashed,userName]
        detailsSet = details[i]

        # detailsSet[0] is the user's email.
        if detailsSet[0] == email:
            userDetails = detailsSet
            found = True
            userIndex = i
        i += 1

    if found:
        # userIndex returned to use with "remember me" function.
        return userDetails,userIndex
    else:
        return False,False
    
def writeToAuthDetails(authDetailsDict:dict):
    """Remember that this will overwrite the details in authDetails.json with whatever you pass in."""
    with open("authDetails.json","w") as f:
        f.write(json.dumps(authDetailsDict))
    

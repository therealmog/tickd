import json

def getAllDetails():
    with open("authDetails.json","r") as f:
        detailsDict = json.load(f)
        details = detailsDict["details"]
        rememberMeIndex = detailsDict["rememberMe"]

    return details,rememberMeIndex

def getDetailsIndividual(email):
    details,_ = getAllDetails()

    found = False
    userDetails = []
    i = 0 
    max = len(details)-1
    while not found and max >= i:
        set = details[i]
        if set[0] == email:
            userDetails = set
            found = True
            userIndex = i
        i += 1

    if found:
        return userDetails,userIndex
    else:
        return False,False
    
def writeToAuthDetails(authDetailsDict:dict):
    """Remember that this will overwrite the details in authDetails.json with whatever you pass in."""
    with open("authDetails.json","w") as f:
        f.write(json.dumps(authDetailsDict))
    

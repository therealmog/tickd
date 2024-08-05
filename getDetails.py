import json

def getDetails():
    with open("authDetails.json","r") as f:
        detailsDict = json.load(f)
        details = detailsDict["details"]
        rememberMeIndex = detailsDict["rememberMe"]

    return details,rememberMeIndex

def getDetailsIndividual(email):
    details,_ = getDetails()

    found = False
    userDetails = []
    i = 0 
    max = len(details)-1
    while not found and max >= i:
        set = details[i]
        if set[0] == email:
            userDetails = set
            found = True
        i += 1
    
    if found:
        return userDetails
    else:
        return False
    

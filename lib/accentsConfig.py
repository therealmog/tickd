import json

def getAccent(email):
    with open("preferences.json","r") as f:
        details = json.load(f)
    
    try:
        user = details[email]
        accent = user["accent"]
        return accent
    
    except KeyError:
        return False
    
def setAccent(email,newColour):
    with open("preferences.json","r") as f:
        details = json.load(f)

    try:
        user = details[email]
        user["accent"] = str(newColour)
    
    except KeyError:
        raise KeyError("User not found in preferences file.")
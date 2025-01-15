import json

def getAccent(email):
    with open("preferences.json","r") as f:
        # Loads all details from preferences file
        details = json.load(f)
    
    try:
        user = details[email]
        accent = user["accent"]
        return accent
    
    except KeyError:
        # Creates new sub dictionary for user's preferences if not found.
        print("User not found, creating new preferences for them.")
        details["email"] = {"accent":"dodgerblue2"}

        with open("preferences.json","w") as f:
            json.dump(details,f,indent=4)
        
        # Default accent colour is "dodgerblue2"
        return "dodgerblue2"
        
            
    
def setAccent(email,newColour):
    with open("preferences.json","r") as f:
        details = json.load(f)

    try:
        user = details[email]
        user["accent"] = str(newColour)

        with open("preferences.json","w") as f:
            json.dump(details,f,indent=4)

        
    
    except KeyError:
        raise KeyError("User not found in preferences file.")

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
        
            
    
def setAccent(email,newColour="dodgerblue2"):
    # Loads in details from preferences file
    with open("preferences.json","r") as f:
        details = json.load(f)

    # Details is indexed by the user's email (email is the key for each dict item.)
        user = details[email]
        user["accent"] = str(newColour)

        # Overwrites file with the updated details.
        with open("preferences.json","w") as f:
            json.dump(details,f,indent=4)


def getFont(email):
    with open("preferences.json","r") as f:
        # Loads all details from preferences file
        details = json.load(f)
    
    try:
        user = details[email]
        font = user["font"]
        return font
    
    except KeyError:       
        # Default font is Bahnschrift
        return "Bahnschrift"


def setFont(email,newFont="Bahnschrift"):
    # Loads in details from preferences file
    with open("preferences.json","r") as f:
        details = json.load(f)

    # Details is indexed by the user's email (email is the key for each dict item.)
        user = details[email]
        user["font"] = str(newFont)

        # Overwrites file with the updated details.
        with open("preferences.json","w") as f:
            json.dump(details,f,indent=4)

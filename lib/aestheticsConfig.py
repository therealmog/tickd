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

def getWallpapersNum(email):
    with open("preferences.json","r") as f:
        # Loads all details from preferences file
        details = json.load(f)

    # Dictionary keys for the program to iterate over.
    wallpaperKeys = ["lightBG","darkBG"]

    # Contains found wallpaper names under keys "lightBG" and "darkBG"
    foundWallpapers = {}

    user = details[email]
    for key in wallpaperKeys:
        try:
            wall = user[key]
            foundWallpapers[key] = wall
        
        except KeyError:       
            # Defaults to none if key not found.
            foundWallpapers[key] = "none"
    
    # Returns lightBG,darkBG
    return foundWallpapers["lightBG"],foundWallpapers["darkBG"]

def setWallpapers(email,light=None,dark=None):
    # Validation to make sure that at least one wallpaper has been passed in to be changed.
    if light == None and dark == None:
        raise Exception("You have not entered any parameters, please try again.")

    wallpapersToSet = {"lightBG":light,"darkBG":dark}

    # Removes unset wallpapers
    for each in wallpapersToSet.copy():
        if wallpapersToSet[each] == None:
            wallpapersToSet.pop(each)
    
    with open("preferences.json","r") as f:
        # Loads all details from preferences file
        details = json.load(f)

    user = details[email]
    for each in wallpapersToSet:
        # Dictionary keys in wallpapersToSet match keys in preferences dict.
        user[each] = wallpapersToSet[each]
    
    # Overwrites file with the updated details.
    with open("preferences.json","w") as f:
        json.dump(details,f,indent=4)
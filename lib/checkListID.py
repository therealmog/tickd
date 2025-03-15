import json
from glob import glob


def checkListID(userEmail,listID):
    path = f"users//{userEmail}//*.json"

    # Gets all of the lists in the sharing user's account.
    userLists = glob(path)
    for each in userLists.copy():
        if "inbox" in each or "shared" in each:
            # Removes inbox and shared file.
            userLists.remove(each)
    
    # Checks each list, compares listID to provided one
    for each in userLists:
        with open(each,"r") as f:
            theList = json.load(f)
            foundListID = theList["listID"]

        if foundListID == listID:
            print("Found list")
            # Takes path from the glob procedure, removes unnecessary details
            # Leaves with actual list name.
            listNameSplit = each.split("\\")
            listName = listNameSplit[1]
            listName = listName.replace(".json","")
            
            return listName
import json

newPrefs = {}

with open("authDetails.json","r") as f:
    allDetails = json.load(f)

allDetails = allDetails["details"]

for each in allDetails:
    newPrefs[each[0]] = {"accent":"dodgerblue2"}

with open("preferences.json","w") as f:
    json.dump(newPrefs,f,indent=4)
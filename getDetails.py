import json

def getDetails(self):
        with open("authDetails.json","r") as f:
            detailsDict = json.load(f)
            details = detailsDict["details"]
            rememberMeIndex = detailsDict["rememberMe"]

        return details,rememberMeIndex
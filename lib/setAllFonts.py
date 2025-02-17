from lib.aestheticsConfig import setFont
import json

userEmails = []

with open("authDetails.json","r") as f:
    details = json.load(f)

for each in details["details"]:
    email = each[0]
    setFont(email)





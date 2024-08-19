import json
import os

def createUserFolder(userPath):
    newListPath = f"{userPath}//inbox.json"

    os.makedirs(userPath)
    with open(newListPath,"a") as f:
        json.dump({"shared":"no",},f) # First set attribute
        
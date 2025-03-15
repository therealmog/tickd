import json
import os

def createUserFolder(userPath):
    newListPath = f"{userPath}//inbox.json"

    os.makedirs(userPath)
    with open(newListPath,"a") as f:
        # Does not have a listID or shared attribute
        json.dump({"tasks":{}},f,indent=4)
    
    # Creates shared file
    with open(f"{userPath}//shared.json","a") as f:
        json.dump({"requests":{}},f,indent=4)       

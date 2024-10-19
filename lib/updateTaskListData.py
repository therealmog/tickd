# Updates a list's JSON file
import json

def updateTaskListData(updatedList,userPath,listName):
    listPath = f"{userPath}//{listName}.json"
    
    with open(listPath,"w") as f:
        json.dump(updatedList,f)
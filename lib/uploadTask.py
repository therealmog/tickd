import json

def uploadTask(userPath,taskDict,listName):
        listPath = f"{userPath}//{listName}.json"

        with open(listPath,"r") as f:
            listDict = json.load(f)

        try:
            tasks = listDict["tasks"]
        except KeyError:
            listDict["tasks"] = {}
        
        taskID = taskDict["taskID"]
        listDict["tasks"][taskID] = taskDict

        with open(listPath,"w") as f:
            json.dump(listDict,f)
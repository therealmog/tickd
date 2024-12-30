import json

def uploadTask(userPath,taskDict,listName):
        # Create file path for list.
        listPath = f"{userPath}//{listName}.json"

        # Extract previous list.
        with open(listPath,"r") as f:
            listDict = json.load(f)

        # Extract the existing tasks part out of the list dictionary.
        try:
            tasks = listDict["tasks"]
        except KeyError: # tasks part does not already exist.
            listDict["tasks"] = {}

        # TaskID is retrieved from new task.
        # Then, new task is stored under that taskID.
        taskID = taskDict["taskID"]
        listDict["tasks"][taskID] = taskDict

        # Altered list is then rewritten to the file.
        with open(listPath,"w") as f:
            json.dump(listDict,f,indent=4)


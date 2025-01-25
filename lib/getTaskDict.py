# Gets a task dictionary given specific taskID, userPath and listName
import json

def getTaskDict(taskID,userPath,listName):
    listPath = f"{userPath}//{listName}.json"

    with open(listPath,"r") as f:
        allData = json.load(f)

    tasksData = allData["tasks"]

    try:
        taskDict = tasksData[taskID]
        return taskDict
    except KeyError:
        print(f"Task not found with task ID {taskID}")
        return False
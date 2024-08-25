import json
from task import Task

def getTasks(master,userPath,listName):
        path = f"{userPath}//{listName}.json"
        
        with open(path,"r") as f:
            theList = json.load(f)
        
        try:
            taskDict = theList["tasks"] # First attribute is always "shared", then comes the tasklist

            taskList = []

            # Returning a list of task objects
            for each in taskDict:
                taskObj = Task(master,attributes=taskDict[each])
                taskList.append(taskObj)
            return taskList

        except:
            print("No tasks found.")
            return False
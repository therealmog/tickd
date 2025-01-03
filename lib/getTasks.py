import json
from lib.task import Task

def getTasks(master,userPath,listName,accent,command,fontName="Bahnschrift"):
        path = f"{userPath}//{listName}.json"
        
        try:
            with open(path,"r") as f:
                theList = json.load(f)
        except FileNotFoundError:
            print(f"List {listName} doesn't exist, creating it now.")
            with open(path,"w") as f:
                newDict = {"shared":"no",
                           "tasks":{},
                           }
                json.dump(newDict,f,indent=4)
            with open(path,"r") as f:
                theList = json.load(f)
            
        
        try:
            taskDict = theList["tasks"] # First attribute is always "shared", then comes the tasklist

            taskList = []

            # Returning a list of task objects
            for each in taskDict:
                if taskDict[each]["completed"] == "False":
                    taskObj = Task(master,accent=accent,attributes=taskDict[each],font=fontName,command=command)
                    taskList.append(taskObj)
            

            if len(taskList) == 0:
                print("No tasks found.")
                return False
            else:
                return taskList
        
        except:
            print("No tasks found.")
            return False
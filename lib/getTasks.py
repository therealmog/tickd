import json
from lib.task import Task
from glob import glob

def getTasks(master,userPath,listName,accent,command,fontName="Bahnschrift",displayListName=False,path=None):
        # Creates path for list
        if path == None:
            path = f"{userPath}//{listName}.json"
        else:
            path = path
        
        try:
            with open(path,"r") as f:
                # Uses json.load to retrieve a JSON object of the list dictionary.
                theList = json.load(f)
        except FileNotFoundError:
        # If the list cannot be found under the path, a new list is created.
        # This is used when creating a new list.
        
            print(f"List {listName} doesn't exist, creating it now.")
            with open(path,"w") as f:
                # Creates the structure of the new list.
                newDict = {"shared":"no",
                           "tasks":{},
                           }
                # Dumps to the new list path.
                json.dump(newDict,f,indent=4)

            # Tries again to retrieve the list from the specified path.    
            with open(path,"r") as f:
                theList = json.load(f)
            
        
        try:
            taskDict = theList["tasks"] # First attribute is always "shared", then comes the tasklist

            taskList = []

            # Returning a list of task objects
            for each in taskDict:
                if taskDict[each]["completed"] == "False":
                    # A Task object is created for each item in the task list.    
                    taskObj = Task(master,accent=accent,attributes=taskDict[each],font=fontName,command=command,displayListName=displayListName)
                    taskList.append(taskObj)
            

            if len(taskList) == 0:
                print("No tasks found.")
                return False
            else:
                return taskList
        
        except:
            print("No tasks found.")
            return False

def getTasksAllLists(master,userPath,accent,command,fontName="Bahnschrift",displayListName=False):
    # Find all lists from user directory.
    userLists = glob(f"{userPath}//*.json")
    allTasksList = []
    for each in userLists:
        if "inbox.json" in each:
            userLists.remove(each)
        else:
            taskList = getTasks(master,userPath,None,accent,command,fontName,displayListName,path=each)
            for each in taskList:
                allTasksList.append(taskList)

    if len(allTasksList) == 0:
        print("No tasks found.")
        return False
    else:
        return allTasksList      
    


    

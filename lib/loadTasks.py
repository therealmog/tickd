import json


def loadTasks(self,userPath,listName):
        listPath = f"{userPath}//{listName}.json"

        try:
            with open(listPath,"r") as f:
                requestedList = json.load(f)
            print(requestedList)
            return requestedList
                
        except FileNotFoundError:
            print("List does not exist!")
            return False
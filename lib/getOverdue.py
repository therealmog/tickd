from datetime import date


def getOverdue(taskList:dict):
    """Takes in a dictionary taskList and sorts which tasks are overdue, returning a dictionary of overdue tasks with the same keys"""

    todayObj = date.today()
    overdueList = {}


    for each in taskList:
        try:
            dateStr = each.attributes["date"]
            dateSplit = dateStr.split("/")
            taskDateObj = date(int(dateSplit[-1]),int(dateSplit[1]),int(dateSplit[0]))

            if taskDateObj < todayObj:
                print(f"Task '{each.attributes["title"]}' is overdue")
                overdueList[each.attributes["taskID"]] = each
        
        except:
            print(f"Date does not exist for {each.attributes["title"]}")
    
    return overdueList
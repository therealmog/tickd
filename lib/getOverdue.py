from datetime import date


def getOverdue(taskList:dict):
    """Takes in a dictionary taskList and sorts which tasks are overdue,\
        returning a dictionary of overdue tasks with the same keys"""

    # Gets today's date as a datetime object.
    todayObj = date.today()
    overdueList = {}


    for each in taskList:
        try:
            # Date is stored in task dict as a string.
            # It is split up by "/" and a datetime object is created using the 3 parts.
            dateStr = each.attributes["date"]
            dateSplit = dateStr.split("/")
            taskDateObj = date(int(dateSplit[-1]),int(dateSplit[1]),int(dateSplit[0]))

            # Compares today's date to the due date of the task.
            if taskDateObj < todayObj:
                #print(f"Task '{each.attributes["title"]}' is overdue")
                overdueList[each.attributes["taskID"]] = each
        
        except:
            # Program will throw an exception when trying to create a datetime object and there
            # are not 3 parts to the split string list.
            # This would mean that there is no date for this task.
            print(f"Date does not exist for {each.attributes["title"]}")
    
    return overdueList


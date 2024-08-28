from datetime import date, timedelta


def checkIfOverdue(taskDict):
    today = date.today()
    dueDateList = taskDict["date"].split("/")
    dueDate = date(int(dueDateList[2]), int(
        dueDateList[1]), int(dueDateList[0]))

    if today > dueDate:
        return True  # overdue
    else:
        return False  # not overdue

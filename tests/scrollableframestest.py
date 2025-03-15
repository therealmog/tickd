# testing scrollable frames

from customtkinter import *
from lib.task import Task

class TaskFrame(CTkScrollableFrame):
    def __init__(self,master):
        super().__init__(master=master,width=400,height=600)

        
        self.taskList = []
        self.createTasks()

    def createTasks(self):
        myTasks = {"yhYQmZ": {
            "title": "Do maths revision",
            "date": "12/11/2024",
            "taskID": "yhYQmZ",
            "completed": "False",
            "time": "",
            "priority": "",
            "description": "",
            "listName": "inbox"
        },
        "zMItjS": {
            "title": "do the deeds",
            "date": "13/11/2024",
            "taskID": "zMItjS",
            "completed": "False",
            "time": "",
            "priority": "",
            "description": "",
            "listName": "inbox"
        },
        "CAWmuG": {
            "title": "Go to school",
            "date": "14/11/2024",
            "taskID": "CAWmuG",
            "completed": "False",
            "time": "",
            "priority": "",
            "description": "",
            "listName": "inbox"
        },
        "yPEDLE": {
            "title": "Eat breakfast",
            "date": "13/11/2024",
            "taskID": "yPEDLE",
            "completed": "False",
            "time": "",
            "priority": "",
            "description": "",
            "listName": "inbox"
        },
        "mhAinz": {
            "title": "Respond to email",
            "date": "12/11/2024",
            "taskID": "mhAinz",
            "completed": "False",
            "time": "19:00",
            "priority": "P1",
            "description": "",
            "listName": "inbox"
        },
        "Ynngst": {
            "title": "Bish",
            "date": "",
            "taskID": "Ynngst",
            "completed": "False",
            "time": "",
            "priority": "",
            "description": "",
            "listName": "inbox"
        },
        "NbKzLa": {
            "title": "Bash",
            "date": "",
            "taskID": "NbKzLa",
            "completed": "False",
            "time": "",
            "priority": "",
            "description": "",
            "listName": "inbox"
        },
        "NoETOd": {
            "title": "Bosh",
            "date": "",
            "taskID": "NoETOd",
            "completed": "False",
            "time": "",
            "priority": "",
            "description": "",
            "listName": "inbox"
        },
        "TnegLq": {
            "title": "Yes now boiz we done",
            "date": "13/11/2024",
            "taskID": "TnegLq",
            "completed": "False",
            "time": "",
            "priority": "",
            "description": "",
            "listName": "inbox"
        },
        "XukBFJ": {
            "title": "Just one more now for luck ",
            "date": "12/11/2024",
            "taskID": "XukBFJ",
            "completed": "False",
            "time": "",
            "priority": "",
            "description": "",
            "listName": "inbox"
        }}

        for each in myTasks:
            taskObj = Task(self,attributes=myTasks[each],size=25)
            self.taskList.append(taskObj)
        
        self.placeTasks()

    
    def placeTasks(self):
        for i in range(0,len(self.taskList)):
            self.taskList[i].grid(row=i,column=0,pady=5)
        
        """self.taskList[0].place(x=0,y=0)
        self.taskList[0].lift()"""

        """for i in range(1,len(self.taskList)):
            self.taskList[i].place(in_=self.taskList[i-1],y=50)"""
    

root = CTk()
root.geometry("600x800")
    
myTaskFrame = TaskFrame(root)
myTaskFrame.place(x=50,y=75)

root.mainloop()
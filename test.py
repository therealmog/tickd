from customtkinter import *
from lib.checkbox_customTk import Checkbox
from lib.task import Task
from random import choice,randint
from string import ascii_letters, ascii_lowercase, ascii_uppercase

root = CTk()

#myTask = Task(root,"Make a sandwich","asjoda","","Bahnschrift")
#myTask.place(x=0,y=0)

def getTasks():
    tasks = {}
    chars = ascii_letters+ascii_uppercase+ascii_lowercase

    for each in range(3):
        taskID = ""
        for each in range(6):
            char = choice(chars)
            taskID+=char
        tasks[taskID] = {"title":"asodadsjasjd",
                         "date":f"{randint(1,31)}/08/24"}
    
    print(tasks)

root.mainloop()
getTasks()




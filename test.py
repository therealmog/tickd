from customtkinter import *
from lib.checkbox_customTk import Checkbox
from task import Task

root = CTk()

myTask = Task(root,"Make a sandwich","asjoda","","Bahnschrift")
myTask.place(x=0,y=0)

root.mainloop()




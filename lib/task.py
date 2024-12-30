# Task frame
from customtkinter import *
from lib.checkbox_customTk import Checkbox
from datetime import date,timedelta


class Task(CTkFrame):

    def __init__(self,master,attributes:dict,accent="dodgerblue2",font="Bahnschrift",size=30,command=None):
        super().__init__(master=master,width=400,height=50,fg_color=("white","gray13"),border_color="gray15",\
                         border_width=3,cursor="hand2")

        self.font = font
        self.size = size
        self.accent = accent
        self.attributes = attributes
        self.command = command

        self.getAttributes()
        self.widgets()
        self.placeWidgets()

        self.bind("<Enter>",lambda event:self.onmouseEnter())
        self.bind("<Leave>",lambda event:self.onmouseLeave())
        self.lblTitle.bind("<Enter>",lambda event:self.onmouseEnter())
        self.lblTitle.bind("<Leave>",lambda event:self.onmouseLeave())
        self.lblDate.bind("<Enter>",lambda event:self.onmouseEnter())
        self.lblDate.bind("<Leave>",lambda event:self.onmouseLeave())

    def widgets(self):
        self.lblTitle = CTkLabel(self,text=self.title,font=(self.font,self.size*0.80),cursor="hand2")
        self.lblTitle.bind("<Button-1>",lambda event: self.lblTitle.focus())
        self.taskDate = self.getDate()
        self.lblDate = CTkLabel(self,text=self.taskDate,font=(self.font,17*0.95))

        if self.taskDateObj != None:
            if self.taskDateObj < date.today():
                self.lblDate.configure(text_color="red")
        
            self.differenceStr = self.getTimeDifference()
            print(self.differenceStr)


        self.checkbox = Checkbox(self,x=-40,y=5,size=(self.size,self.size),relWidget=self.lblTitle,command=self.command,commandArgs={"taskID":self.attributes["taskID"]})

    def placeWidgets(self):
        self.lblTitle.place(x=45,y=5)#This should stay as it is, since it is the frame that will be placed inside the actual app.
        self.checkbox.placeWidget()
        if self.lblDate != "":
            self.configure(height=65)
            self.lblDate.place(in_=self.lblTitle,x=0,y=30)

    def onmouseEnter(self):
        self.lblTitle.configure(text_color=self.accent)

        self.lblDate.configure(text=self.differenceStr)
        

    def onmouseLeave(self):
        self.lblTitle.configure(text_color=("black","white"))
        if self.taskDateObj != None:
            self.lblDate.configure(text=self.taskDate)

    def getAttributes(self):
        attributes = self.attributes

        self.title = attributes["title"]
        if self.title == "":
            self.title = "(no title)"
        
        #---- Possible attributes ----#
        self.date = ""
        self.time = ""
        self.priority = ""
        self.description = ""

        possibleAttributes = {"date":self.date,
                              "time":self.time,
                              "priority":self.priority,
                              "description":self.description}
        for each in attributes:
            try:
                possibleAttributes[each] = attributes[each]
            except:
                pass
    
    def getDate(self):
        #try:
        taskDateStr = self.attributes["date"]
        dateList = taskDateStr.split("/")

        if len(dateList) >1:
            self.taskDateObj = date(int(dateList[-1]),int(dateList[1]),int(dateList[0]))
            today = date.today()
            tomorrow = date.today() + timedelta(days=1)

            if self.taskDateObj == today:
                taskDate = "today"
            elif self.taskDateObj == tomorrow:
                taskDate = "tomorrow"
            else:
                taskDate = self.taskDateObj.strftime("%d/%m/%Y")
        else:
            self.taskDateObj = None
            taskDate = "(no date)"
            
        """except:
            self.taskDateObj = None
            taskDate = taskDateStr"""
                    
        return taskDate
    
    def getTimeDifference(self):
        late = False
        if self.taskDateObj >= date.today():
            difference = self.taskDateObj - date.today()
        else:
            difference = date.today() - self.taskDateObj
            late = True
        
        days = difference.days
        if late:
            differenceStr = f"{days} days ago"
        else:
            differenceStr = f"{days} days left"
        
        return differenceStr

    
    


    

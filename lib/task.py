# Task frame
from customtkinter import *
from lib.checkbox_customTk import Checkbox
from datetime import date,timedelta
from lib.getListImgs import getListImgs

class Task(CTkFrame):

    def __init__(self,master,attributes:dict,accent="dodgerblue2",font="Bahnschrift",size=30,command=None,displayListName=False):
        super().__init__(master=master,width=400,height=67,fg_color=("white","gray13"),border_color="gray15",\
                         border_width=3,cursor="hand2")

        self.font = font
        self.size = size
        self.accent = accent
        self.attributes = attributes
        self.command = command

        # Task becomes bigger and displays list name underneath title
        self.displayListName = displayListName

        self.widgets()
        self.placeWidgets()

        self.bind("<Enter>",lambda event:self.onmouseEnter())
        self.bind("<Leave>",lambda event:self.onmouseLeave())
        self.lblTitle.bind("<Enter>",lambda event:self.onmouseEnter())
        self.lblTitle.bind("<Leave>",lambda event:self.onmouseLeave())
        self.lblDate.bind("<Enter>",lambda event:self.onmouseEnter())
        self.lblDate.bind("<Leave>",lambda event:self.onmouseLeave())

    def widgets(self):
        # Defining the title and date label widgets.
        self.lblTitle = CTkLabel(self,text=self.attributes["title"],font=(self.font,self.size*0.80),cursor="question_arrow")
        self.lblTitle.bind("<Button-1>",lambda event: self.lblTitle.focus())
        self.taskDate = self.getDate()
        self.lblDate = CTkLabel(self,text=self.taskDate,font=(self.font,17*0.95))

        # Checking if the date is overdue, to set a red label.
        if self.taskDateObj != None:
            if self.taskDateObj < date.today():
                self.lblDate.configure(text_color="red")

            # Calculates the string to show if hovering over date (e.g. "2 days ago", "in 4 days", etc.)
            self.differenceStr = self.getTimeDifference()
            #print(self.differenceStr)   

        # Creating the checkbox for the task.
        # Passing in the command which is taken in from the main app (i.e. in the constructor.)
        self.checkbox = Checkbox(self,x=-40,y=5,size=(self.size,self.size),relWidget=self.lblTitle,\
                                 command=self.command,commandArgs={"taskID":self.attributes["taskID"]})
        
        # Adds the time to the date label if applicable.
        if self.attributes["time"] != "":
            self.lblDate.configure(text=f"{self.taskDate}, {self.attributes["time"]}")

        # Assigns the priority colour, if applicable.
        if self.attributes["priority"] != "":
            priority = self.attributes["priority"]
            if  priority == "P1":
                self.configure(border_color="red")
            elif priority == "P2":
                self.configure(border_color="#db9d09")
            else:
                self.configure(border_color="limegreen")
        
        if self.displayListName:
            listImgs = getListImgs((20,20))
            try:
                listName = self.attributes["listName"]

                iconFound = False
                for each in listImgs:
                    if listName.capitalize() == each:
                        iconFound = True
                        break
                
                if iconFound:
                    self.lblListName = CTkLabel(self,text=f" {listName.capitalize()}",font=(self.font,self.size*0.6),image=listImgs[listName.capitalize()],compound="left")
                else:
                    self.lblListName = CTkLabel(self,text=listName.capitalize(),font=(self.font,self.size*0.6))

            except KeyError:
                print("List name not found.")
                self.displayListName = False


    def placeWidgets(self):
        self.lblTitle.place(x=45,y=5)#This should stay as it is, since it is the frame that will be placed inside the actual app.
        self.checkbox.placeWidget()

        self.lblDate.place(in_=self.lblTitle,x=0,y=30)

        if self.displayListName:
            # Increases height of task.
            self.configure(height=95)
            self.lblListName.place(in_=self.lblTitle,x=0,y=32)
            self.lblDate.place(in_=self.lblListName,y=25)



        

    def onmouseEnter(self):
        self.lblTitle.configure(text_color=self.accent)
        
        try:
            self.lblDate.configure(text=self.differenceStr)
        except:
            pass
        

    def onmouseLeave(self):
        self.lblTitle.configure(text_color=("black","white"))
        if self.taskDateObj != None:
            if self.attributes["time"] != "":
                self.lblDate.configure(text=f"{self.taskDate}, {self.attributes["time"]}")
            else:
                self.lblDate.configure(text=self.taskDate)

    def refreshData(self):
        # Makes sure that labels and messages are up to date with details, etc.

        self.lblTitle.configure(text=self.attributes["title"])
        self.taskDate = self.getDate()
        self.differenceStr = self.getTimeDifference()
        
        

        # Adds the time to the date label if applicable.
        if self.attributes["time"] != "":
            self.lblDate.configure(text=f"{self.taskDate}, {self.attributes["time"]}")
        else:
            self.lblDate.configure(text=self.taskDate)

        # Assigns the priority colour, if applicable.
        if self.attributes["priority"] != "":
            priority = self.attributes["priority"]
            if  priority == "P1":
                self.configure(border_color="red")
            elif priority == "P2":
                self.configure(border_color="#db9d09")
            else:
                self.configure(border_color="limegreen")
        
        if self.displayListName:
            listImgs = getListImgs((20,20))
            try:
                listName = self.attributes["listName"]

                iconFound = False
                for each in listImgs:
                    if listName.capitalize() == each:
                        iconFound = True
                        break
                
                if iconFound:
                    self.lblListName = CTkLabel(self,text=f" {listName.capitalize()}",font=(self.font,self.size*0.6),image=listImgs[listName.capitalize()],compound="left")
                else:
                    self.lblListName = CTkLabel(self,text=listName.capitalize(),font=(self.font,self.size*0.6))

            except KeyError:
                print("List name not found.")
                self.displayListName = False
        

    
    def getDate(self):
        # Gets the date stored in the task dictionary (or attributes dict in this object.)
        taskDateStr = self.attributes["date"]
        dateList = taskDateStr.split("/")

        # If the date is valid (it will create a list with more than 1 part)
        if len(dateList) >1:
            # Creates a datetime object for the task date - saved as an attribute.
            self.taskDateObj = date(int(dateList[-1]),int(dateList[1]),int(dateList[0]))

            # Creates datetime objects for today and tomorrow.
            today = date.today()
            tomorrow = date.today() + timedelta(days=1)

            # The task date can be displayed as "today" or "tomorrow" if applicable.
            if self.taskDateObj == today:
                taskDate = "today"
            elif self.taskDateObj == tomorrow:
                taskDate = "tomorrow"
            else:
                # Date is simply displayed as the regular short date.
                # Derived from taskDateObj using the strftime method.
                taskDate = self.taskDateObj.strftime("%d/%m/%Y")
        else:
            # No date saved - this is displayed clearly for the user.
            self.taskDateObj = None
            taskDate = "(no date)"
                                
        return taskDate
    
    def setTitleColour(self):
        """Sets colour of title to accent colour to display that it is being viewed (display panel)"""

        if self.lblTitle._text_color == self.accent:
            self.lblTitle.configure(text_colour=("black","white"))
        else:
            self.lblTitle.configure(text_colour=self.accent)
    
    
    def getTimeDifference(self):
        late = False
        if self.taskDateObj >= date.today():
            # The "-" operator creates a timedelta object using
            # the datetime module.
            difference = self.taskDateObj - date.today()
        else:
            difference = date.today() - self.taskDateObj
            late = True

        # The timedelta object has different parts
        # We only need the days part, so this is selected.
        days = difference.days
        if late:
            differenceStr = f"{days} days ago"
        else:
            differenceStr = f"{days} days left"
        
        return differenceStr

    
    


    

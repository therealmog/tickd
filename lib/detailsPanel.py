# Details panel for tasks
from customtkinter import *


class DetailsPanel(CTkFrame):
    def __init__(self,master,taskAttributes,taskButton,fontName="Bahnschrift"):
        super().__init__(master,width=500,height=350,border_width=3,border_color="white")
        self.option_add("*CTkLabel*text_color","green")

        self.taskAttributes = taskAttributes
        self.taskName = taskAttributes["title"]
        self.taskDate = taskAttributes["date"]
        self.taskTime = taskAttributes["time"]
        self.taskPriority = taskAttributes["priority"]
        self.taskID = taskAttributes["taskID"]
        self.fontName = fontName

        try:
            self.taskDescription = taskAttributes["description"]
        except:
            self.taskDescription = ""

        self.widgets()
        self.placeWidgets()


    def widgets(self):
        globalFontName = self.fontName
        self.lblTaskName = CTkLabel(self,text=self.taskName,font=(globalFontName,30))
        
        self.checkTitleLength()
        
        self.lblDate = CTkLabel(self,text=self.taskDate,font=(globalFontName,20))
        self.lblTime = CTkLabel(self,text=self.taskTime,font=(globalFontName,20))
        self.lblDescription = CTkLabel(self,text="description:",font=(globalFontName,20))
        self.entryDescription = CTkTextbox(self,width=450,height=180,font=(globalFontName,20),wrap=WORD,activate_scrollbars=True)
        self.entryDescription.insert("1.0",self.taskDescription)

        self.checkAttributes()

    def placeWidgets(self):
        self.lblTaskName.place(x=75,y=20)
        self.lblDate.place(in_=self.lblTaskName,y=35)
        self.lblTime.place(in_=self.lblDate,x=12*(len(self.lblDate.cget("text"))))
        self.lblDescription.place(x=25,y=100)
        self.entryDescription.place(in_=self.lblDescription,y=30)
        
    def checkAttributes(self):
        if self.taskDate == "":
            self.lblDate.configure(text="no date")
        
        if self.taskTime == "":
            self.lblTime.configure(text="no time")
    
    
    def checkTitleLength(self):
        # Reduces title font size if the title is greater than a certain length

        length = len(self.taskName)
        self.titleFontSize = 30
        if length > 30:
            if length > 30 and length < 40:
                self.titleFontSize = 25
            elif length > 40 and length <=45:
                self.titleFontSize = 20
            else:
                self.titleFontSize = 18
            self.lblTaskName.configure(font=(self.fontName,self.titleFontSize,"underline"))
        
            
        
    
root = CTk()
root.geometry("1920x1080")

myPanel = DetailsPanel(root,{"title":"Revise","date":"16/10/2024","description":"You have to finish all of your homework first","time":"","priority":"","taskID":"2ks90a"},"hello")
myPanel.pack()

root.mainloop()
        



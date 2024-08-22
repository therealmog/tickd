# Task frame
from customtkinter import *
from lib.checkbox_customTk import Checkbox


class Task(CTkFrame):

    def __init__(self,master,attributes:dict,font="Bahnschrift",size=25):
        super().__init__(master=master,width=1300,height=50,fg_color=("white","gray13"),border_color="gray15",border_width=5)

        self.font = font
        self.size = size
        self.attributes = attributes

        self.getAttributes()
        self.widgets()
        self.placeWidgets()
        

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

    def widgets(self):
        self.lblTitle = CTkLabel(self,text=self.title,font=(self.font,self.size*0.95))
        self.lblTitle.bind("<Button-1>",lambda event: self.lblTitle.focus())

        self.checkbox = Checkbox(self,x=-35,y=5,size=(self.size,self.size),relWidget=self.lblTitle)

    def placeWidgets(self):
        self.lblTitle.place(x=40,y=5)#This should stay as it is, since it is the frame that will be placed inside the actual app.
        self.checkbox.placeWidget()


    

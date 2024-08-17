# Task frame
from customtkinter import *
from lib.checkbox_customTk import Checkbox


class Task(CTkFrame):

    def __init__(self,master,attributes:dict,font="Bahnschrift",size=25):
        super().__init__(master=master,width=300,height=50)

        self.font = font


        self.widgets()
        self.placeWidgets()

    def getAttributes(self):
        attributes = self.attributes

        self.title = attributes["title"]
        self.description = attributes["description"]
        self.date = attributes["date"]


    def widgets(self):
        self.lblTitle = CTkLabel(self,text=self.title,font=(self.font,20))
        self.checkbox = Checkbox(self,x=-35,y=0,size=(25,25),relWidget=self.lblTitle)

    def placeWidgets(self):
        self.lblTitle.place(x=35)
        self.checkbox.placeWidget()


    

# Small window which opens when an attribute is being edited.
from customtkinter import *
import textwrap

class EditingWin(CTkToplevel):
    def __init__(self,attributeName,taskAttributes,userPath,listName,fontName="Bahnschrift"):
        super().__init__()
        
        self.geometry("500x150")

        self.attributeName = attributeName
        self.taskAttributes = taskAttributes
        self.userPath = userPath
        self.listName = listName
        self.fontName = fontName

        self.title(f"Change {self.attributeName} - Tickd")

        self.widgets()
        self.placeWidgets()
    
    def widgets(self):
        globalFontName = self.fontName
        titleText = textwrap.fill(f"Change the {self.attributeName} for '{self.taskAttributes["title"]}'")
        print(titleText)
        self.lblTitle = CTkLabel(self,text=titleText,font=(globalFontName,20))
        self.entryAttribute = CTkEntry(self,font=(globalFontName,20),placeholder_text=f"{self.attributeName}")
    
    def placeWidgets(self):
        self.lblTitle.place(x=15,y=25)
        self.entryAttribute.place(in_=self.lblTitle,y=30)
    

root = CTk()
myWin = EditingWin("date",{"title":"Do your A Level Maths revision"},"","")
myWin.grab_set()
#myWin.grab_release()
root.mainloop()
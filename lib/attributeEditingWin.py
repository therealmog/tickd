# Small window which opens when an attribute is being edited.
from customtkinter import *
import textwrap

class EditingWin(CTkToplevel):
    def __init__(self,attributeName,taskAttributes,userPath,listName,fontName="Bahnschrift",maxChars=None,customTitle=None):
        super().__init__()
        
        self.geometry("500x150")

        self.attributeName = attributeName
        self.taskAttributes = taskAttributes
        self.userPath = userPath
        self.listName = listName
        self.fontName = fontName
        self.maxChars = maxChars
        self.customTitle = customTitle

        if customTitle == None:
            self.title(f"Change {self.attributeName} - Tickd")
        else:
            self.title(f"{customTitle} - Tickd")

        self.widgets()
        self.placeWidgets()

        self.entryAttribute.bind("<FocusIn>",lambda event: self.enter())
        self.entryAttribute.bind("<FocusOut>",lambda event: self.leave())
    
    def widgets(self):
        globalFontName = self.fontName
        if self.customTitle == None:
            self.titleText = textwrap.fill(f"Change the {self.attributeName} for '{self.taskAttributes["title"]}'",50)
        else:
            self.titleText = textwrap.fill(f"{self.customTitle}",50)
        print(self.titleText)
        self.lblTitle = CTkLabel(self,text=self.titleText,font=(globalFontName,20),anchor=W)

        if self.maxChars != None:
            width = self.maxChars * 20
        else:
            width=140
        self.entryAttribute = CTkEntry(self,font=(globalFontName,20),placeholder_text=f"{self.attributeName}",width=width)
        self.entryText = ""

    def placeWidgets(self):
        self.lblTitle.place(x=15,y=25)
        
        if len(self.titleText) > 50:
            entryAttrY = 60
        else:
            entryAttrY = 30

        self.entryAttribute.place(in_=self.lblTitle,y=entryAttrY)

    def limitChars(self):
        print("Hello")
        if self.maxChars == None:
            pass
        else:
            if len(self.entryAttribute.get()) >= self.maxChars-1:
                accepted = self.entryAttribute.get()[0:self.maxChars-1]
                self.entryAttribute.delete(0,END)
                self.entryAttribute.insert(0,accepted)
            else:
                self.entryText = self.entryAttribute.get()
            """if self.entryChars < self.maxChars:
                self.entryChars = len(self.entryAttribute.get())
                newStr = self.entryAttribute.get()[0:-1]
                self.entryAttribute.delete(0,END)
                self.entryAttribute.insert(0,newStr)"""

    def enter(self):
        self.entryAttribute.bind("<Key>",lambda event: self.limitChars())
    def leave(self):
        self.entryAttribute.unbind("<Key>")
    

root = CTk()
myWin = EditingWin("date",{"title":"Do your revision"},"","",maxChars=5)
myWin.grab_set()
root.after(1000,lambda: myWin.grab_release())
root.mainloop()

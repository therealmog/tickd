# Small window which opens when an attribute is being edited.
from customtkinter import *
import textwrap
from submitBtn import SubmitButton

class EditingWin(CTkToplevel):
    def __init__(self,attributeName,valueToSave,userPath,listName=None,taskAttributes=None,validationFunc=None,fontName="Bahnschrift",maxChars=None,customTitle=None,accent="dodgerblue2"):
        """You can also include f-strings into the custom title and they will be formatted.
        Just make sure that they take into account what the actual variable name will be (e.g. attributeName -> self.attributeName)
        
        NOTE: The 'valueToSave' must be an attribute of the main window."""
        super().__init__()
        
        self.geometry("500x150")

        self.attributeName = attributeName
        if taskAttributes != None:
            self.taskAttributes = taskAttributes
        self.userPath = userPath
        if listName != None:
            self.listName = listName
        self.fontName = fontName
        self.maxChars = maxChars
        self.customTitle = customTitle
        self.accent = accent
        self.valueToSave = valueToSave

        if validationFunc != None:
            self.validationFunc = validationFunc
        else:
            self.validationFunc = None

        if customTitle == None:
            self.title(f"Change {self.attributeName} - Tickd")
        else:
            self.title(f"{customTitle} - Tickd")

        self.widgets()
        self.placeWidgets()

        """self.entryAttribute.bind("<FocusIn>",lambda event: self.enter())
        self.entryAttribute.bind("<FocusOut>",lambda event: self.leave())"""

        # Limits the amount of characters that can be entered.
        validateCharsCmd = (self.register(self.checkChars),"%P")
        self.entryAttribute.configure(validate="key",validatecommand=validateCharsCmd)
    
    def widgets(self):
        globalFontName = self.fontName
        if self.customTitle == None:
            self.titleText = textwrap.fill(f"Change the {self.attributeName} for '{self.taskAttributes["title"]}'",50)
        else:
            self.titleText = textwrap.fill(f"{self.customTitle}",50)
        print(self.titleText)
        self.lblTitle = CTkLabel(self,text=self.titleText,font=(globalFontName,20),anchor=W)

        if self.maxChars != None:
            self.entrywidth = self.maxChars * 15
        else:
            self.entrywidth=140
        self.entryAttribute = CTkEntry(self,font=(globalFontName,22),placeholder_text=f"{self.attributeName}",width=self.entrywidth)
        self.entryText = ""

        self.btnSubmit = SubmitButton(self,command=self.submit,colour=self.accent,buttonSize=(30,30))

    def placeWidgets(self):
        self.lblTitle.place(x=15,y=25)
        
        if len(self.titleText) > 50:
            entryAttrY = 60
        else:
            entryAttrY = 30

        self.entryAttribute.place(in_=self.lblTitle,y=entryAttrY)
        self.btnSubmit.place(in_=self.entryAttribute,y=5+self.entrywidth)

    
    
    def checkChars(self,entryTxt):
        if len(entryTxt) > self.maxChars:
            return False
        else:
            return True

    def enter(self):
        self.entryAttribute.bind("<Key>",lambda event: self.limitChars())
    def leave(self):
        self.entryAttribute.unbind("<Key>")
    

    def submit(self):
        self.valueToSave = self.entryAttribute.get()

        self.destroy()
    

root = CTk()
myWin = EditingWin("date","print",{"title":"Do your revision"},"","",maxChars=8)
myWin.grab_set()
root.after(1000,lambda: myWin.grab_release())
root.mainloop()

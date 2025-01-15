# Small window which opens when an attribute is being edited.
from customtkinter import *
import textwrap
from lib.submitBtn import SubmitButton
from tkinter import messagebox

class GetValueWin(CTkToplevel):
    def __init__(self,attributeName,assigningFunc,assigningFuncArgs=None,listName=None,validationFunc=None,validationFuncArgs=None,\
                 fontName="Bahnschrift",maxChars=None,customTitle=None,accent="dodgerblue2",flagFunc=None):
        """Takes in an input and changes the value of an attribute.

        Pass in the assigning function (assigningFunc) that will be run once the input has been taken in.
        Any arguments for the assigningFunc or the validationFunc should be put into a dictionary with the correct keyword names.

        You can also include f-strings into the custom title and they will be formatted.
        Just make sure that they take into account what the actual variable name will be (e.g. attributeName -> self.attributeName)"""
        
        super().__init__()
        
        self.geometry("400x150")
        self.iconbitmap("logo//tickd.ico")

        if listName != None:
            self.listName = listName

        # Defines class attributes based on entered arguments.
        self.attributeName = attributeName
        self.fontName = fontName
        self.maxChars = maxChars
        self.customTitle = customTitle
        self.accent = accent
        self.assigningFunc = assigningFunc
        self.flagFunc = flagFunc

        if validationFunc != None:
            # Allows for validation to be run once input has been received.
            self.validationFunc = validationFunc
        else:
            # Otherwise, input will be passed straight into the assigningFunc (function which is run to use input)
            self.validationFunc = None
        
        self.validationFuncArgs = validationFuncArgs
        self.assigningFuncArgs = assigningFuncArgs
        

        if customTitle == None:
            self.title(f"Change the {self.attributeName} - Tickd")
        else:
            self.title(f"{customTitle} - Tickd")

        # Sets custom function for when window is closed.
        self.protocol("WM_DELETE_WINDOW",lambda:self.close_window())

        self.widgets()
        self.placeWidgets()

        # Lifts new window to the top.
        self.grab_set()
        self.lift()
        self.after(1000,self.grab_release)

        

        # Limits the amount of characters that can be entered.
        validateCharsCmd = (self.register(self.checkChars),"%P")
        self.entryAttribute.configure(validate="key",validatecommand=validateCharsCmd)

        self.bind("<Return>",lambda event: self.submit())

        """self.entryAttribute.bind("<FocusIn>",lambda event: self.enter())
                self.entryAttribute.bind("<FocusOut>",lambda event: self.leave())"""
        
    
    def bringToTop(self):
        self.grab_set()
        self.lift()
        self.after(1000,self.grab_release)
        self.focus()
        
    def close_window(self):
        if self.flagFunc != None:
            self.flagFunc()
        self.destroy()

    def widgets(self):
        globalFontName = self.fontName
        if self.customTitle == None:
            self.titleText = textwrap.fill(f"Change the {self.attributeName}",50)
        else:
            self.titleText = textwrap.fill(f"{self.customTitle}",50)
        print(self.titleText)
        self.lblTitle = CTkLabel(self,text=self.titleText,font=(globalFontName,20),anchor=W)

        if self.maxChars != None:
            self.entrywidth = self.maxChars * 15
        else:
            self.entrywidth=280
        self.entryAttribute = CTkEntry(self,font=(globalFontName,22),placeholder_text=f"{self.attributeName}",width=self.entrywidth)

        self.btnSubmit = SubmitButton(self,command=self.submit,colour=self.accent,buttonSize=(28,28))

    def placeWidgets(self):
        self.lblTitle.place(x=15,y=25)
        
        if len(self.titleText) > 50:
            entryAttrY = 60
        else:
            entryAttrY = 30

        self.entryAttribute.place(in_=self.lblTitle,y=entryAttrY)
        self.btnSubmit.place(in_=self.entryAttribute,x=5+self.entrywidth,y=-2)

    
    
    def checkChars(self,entryTxt):
        if self.maxChars == None:
            return True
        else:
            if len(entryTxt) > self.maxChars:
                return False
            else:
                return True

    def enter(self):
        self.entryAttribute.bind("<Key>",lambda event: self.limitChars())
    def leave(self):
        self.entryAttribute.unbind("<Key>")
    

    def submit(self):
        # Assuming that each validation function returns two values: a correct value and a message.

        # If validation function assigned.
        if self.validationFunc != None:
            if self.validationFuncArgs != None:
                # Unpackages any arguments for the validation function using ** operator
                # validationFuncArgs and assigningFuncArgs are both dictionaries with format {parameter_name:value}
                # However, the user input is always passed in as the first argument.
                value,message = self.validationFunc(self.entryAttribute.get(),**self.validationFuncArgs)
            else:
                value,message = self.validationFunc(self.entryAttribute.get())

            if value == False:
                # Error occurred.
                messagebox.showerror(f"Can't change {self.attributeName}",message)

                # Runs function to lift window and focus it.
                self.bringToTop()
            else:
                # Validation successful, now running function to use argument.
                if self.assigningFuncArgs != None:
                    self.assigningFunc(value,**self.assigningFuncArgs)
                else:
                    self.assigningFunc(value)

                # Closes window once function has finished running.
                self.destroy()
                
        # Validation function not assigned.
        else:
            if self.assigningFuncArgs != None:
                self.assigningFunc(self.entryAttribute.get(),**self.assigningFuncArgs)
            else:
                self.assigningFunc(self.entryAttribute.get())

            self.destroy()



"""root = CTk()
myWin = EditingWin("date","print",maxChars=8)
myWin.grab_set()
root.after(1000,lambda: myWin.grab_release())
root.mainloop()"""

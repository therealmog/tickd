# Details panel for tasks
from customtkinter import *
from lib.checkbox_customTk import Checkbox
from PIL import Image
from lib.uploadTask import uploadTask
from lib.getValueWindow import GetValueWin
from lib.checkDate import checkDate
from lib.checkTime import checkTime
from tkinter import messagebox
from lib.getTaskDict import getTaskDict

class DetailsPanel(CTkFrame):
    def __init__(self,master,origin,mainWindow,taskObj,userPath,taskAttributes,taskButtonCommand,commandArgs,\
                 fontName="Bahnschrift",accent="dodgerblue2"):
        super().__init__(master,width=800,height=500,border_width=3,border_color="grey5")

        self.taskAttributes = taskAttributes
        self.taskName = taskAttributes["title"]
        self.taskDate = taskAttributes["date"]
        self.taskTime = taskAttributes["time"]
        self.taskPriority = taskAttributes["priority"]
        self.taskID = taskAttributes["taskID"]
        self.fontName = fontName
        self.accent = accent
        self.userPath = userPath
        self.origin = origin
        self.taskObj = taskObj   
        self.mainWindow = mainWindow   

        
        

        self.taskButtonCommand = taskButtonCommand
        self.commandArgs = commandArgs

        try:
            self.taskDescription = taskAttributes["description"]
        except:
            self.taskDescription = ""
        
        

        self.widgets()
        self.placeWidgets()
        self.bindEventListeners()

        


    def widgets(self):
        globalFontName = self.fontName
        self.lblTaskName = CTkLabel(self,text=self.taskName,font=(globalFontName,35),cursor="hand2")

        # Checks length of title to see if font size needs to be reduced.
        self.checkTitleLength()

        # Declares rest of interface elements.
        self.imgClose = CTkImage(Image.open("icons//cancel.png"),size=(20,20))
        self.btnClose = CTkButton(self,image=self.imgClose,text="",width=20,fg_color="grey12",hover_color="red",\
                                  border_color="grey5",border_width=2,command=self.place_forget)
        self.taskButton = self.getTaskButton()
        self.lblDate = CTkLabel(self,text=self.taskDate,font=(globalFontName,20),cursor="hand2")
        self.lblTime = CTkLabel(self,text=self.taskTime,font=(globalFontName,20),cursor="hand2")
        self.lblDescription = CTkLabel(self,text="description:",font=(globalFontName,22))
        self.entryDescription = CTkTextbox(self,width=750,height=250,font=(globalFontName,22),wrap=WORD,\
                                           activate_scrollbars=True,fg_color=("#f0fafe","gray13"))
        self.entryDescription.insert("1.0",self.taskDescription)
        self.entryDescription.bind("<Button-1>",lambda event: self.descriptionBoxEnter())

        # Checks to see if date and time are defined, to replace the label with (no date) or (no time) if needed.
        self.checkAttributes()

        # Used for binding event listeners in the bindEventListeners procedure.
        self.hoverWidgets = {"lblTaskName":self.lblTaskName,
                        "lblDate":self.lblDate,
                        "lblTime":self.lblTime,
                        }
        self.hoverWidgetFonts = {}

        # Declares save and cancel button for editing description.
        self.imgSave = CTkImage(Image.open("icons//save.png"),size=(25,25))
        self.btnSaveDescription = CTkButton(self,text="save",font=(globalFontName,25),fg_color=self.accent,\
                                            command=lambda:self.saveDescription(),width=70,image=self.imgSave)
        self.tickImg = CTkImage(Image.open("logo//tick.png"),size=(35,35))
        self.lblSave = CTkLabel(self,text="Saved description.",text_color="limegreen",font=(globalFontName,25),\
                                image=self.tickImg,compound="left")
        self.imgCancel = CTkImage(Image.open("icons//cancel.png"),size=(25,25))
        self.btnCancel = CTkButton(self,text="cancel",fg_color="red",image=self.imgCancel,font=(globalFontName,25),\
                                   width=80,command=self.btnCancelClicked,hover_color="#c92d2a")

        # Declares set reminder button and icon.
        self.imgAlarm = CTkImage(Image.open("icons//alarm.png"),size=(23,23))
        self.btnSetReminder = CTkButton(self,text="Set reminder",font=(globalFontName,22),fg_color=self.accent,width=70,\
                                        image=self.imgAlarm)
        
        self.flagAttributeEditing = False

        self.changeDateArgs = {"attributeName":"date",
                          "assigningFunc":self.updateTaskInfo,
                          "assigningFuncArgs":{"attributeName":"date"},
                          "validationFunc":checkDate,
                          "maxChars":8,
                          "accent":self.accent,
                          "flagFunc":self.flagFuncAttrEditing}
        
        self.changeTimeArgs = {"attributeName":"time",
                          "assigningFunc":self.updateTaskInfo,
                          "assigningFuncArgs":{"attributeName":"time"},
                          "validationFunc":checkTime,
                          "maxChars":5,
                          "accent":self.accent,
                          "flagFunc":self.flagFuncAttrEditing}
        
        self.changeNameArgs = {"attributeName":"name",
                          "assigningFunc":self.updateTaskInfo,
                          "assigningFuncArgs":{"attributeName":"name"},
                          "validationFunc":self.checkNewTitle,
                          "accent":self.accent,
                          "previousVal":self.taskName,
                          "flagFunc":self.flagFuncAttrEditing}
        
        self.bindAttributeWins()
        
        

    def bindAttributeWins(self):
        changeDateText = f"Change the date for '{self.taskName}'"
        changeTimeText = f"Change the time for '{self.taskName}'"
        changeNameText = f"Change the name of '{self.taskName}'"

        self.lblTaskName.unbind("<Button-1>")
        self.lblDate.unbind("<Button-1>")
        self.lblTime.unbind("<Button-1>")

        self.lblDate.bind("<Button-1>",lambda event,customTitle=changeDateText,
                          kwargs=self.changeDateArgs:self.checkAttributeEditing(customTitle,kwargs))
        self.lblTime.bind("<Button-1>",lambda event,customTitle=changeTimeText,
                          kwargs=self.changeTimeArgs:self.checkAttributeEditing(customTitle,kwargs))
        self.lblTaskName.bind("<Button-1>",lambda event,customTitle=changeNameText,
                              kwargs=self.changeNameArgs:self.checkAttributeEditing(customTitle,kwargs))

    def checkAttributeEditing(self,customTitle,kwargs):
        # Checks to see if a previous editing window exists.

        if self.flagAttributeEditing:
            # Previous window already open
            messagebox.showinfo("Window already active",
                                "Another attribute is currently being edited.\nPlease close the previous window to open another one.")
        else:
            # Sets flag to True so that another window cannot be opened.
            self.flagAttributeEditing = True
            # Calls new GetValueWin instance
            GetValueWin(customTitle=customTitle,fontName=self.fontName,**kwargs)
                


    def placeWidgets(self):
        self.btnClose.place(x=740,y=20)
        self.lblTaskName.place(x=80,y=20)
        self.lblDate.place(in_=self.lblTaskName,y=45)
        self.lblTime.place(in_=self.lblDate,x=12*(len(self.lblDate.cget("text"))))
        self.btnSetReminder.place(in_=self.lblTime,x=100)
        self.lblDescription.place(x=25,y=110)
        self.entryDescription.place(in_=self.lblDescription,y=30)
        self.taskButton.placeWidget()
        #self.btnSaveDescription.place(in_=self.entryDescription,x=220,y=190)

    def updateTaskInfo(self,newData,attributeName):
        if attributeName == "date":
            self.taskDate = newData
            self.lblDate.configure(text=newData)
            self.taskAttributes["date"] = newData
            self.mainWindow.checkOverdueAll()
            
        elif attributeName == "time":
            self.taskTime = newData
            self.lblTime.configure(text=newData)
            self.taskAttributes["time"] = newData
        elif attributeName == "priority":
            self.taskPriority = newData
        else:
            self.taskName = newData
            self.lblTaskName.configure(text=newData)
            self.taskAttributes["title"] = newData
            self.changeNameArgs["previousVal"] = newData
        

        uploadTask(self.userPath,self.taskAttributes,listName=self.taskAttributes["listName"])
        self.taskObj.refreshData()
        self.mainWindow.updateTasks()
        self.mainWindow.checkNewTasksAll()
        self.bindAttributeWins()
        self.flagFuncAttrEditing()

    def refreshTaskDetails(self):
        # Gets latest task details.
        taskDict = getTaskDict(self.taskID,self.userPath,self.taskAttributes["listName"])

        # Rewrites attributes with their latest versions.
        self.lblTaskName.configure(text=taskDict["title"])
        self.lblDate.configure(text=taskDict["date"])
        self.lblTime.configure(text=taskDict["time"])

        # Checks if date and/or time are blank, and replaces them with "no date/time".
        self.checkAttributes()

        self.lblTime.place(in_=self.lblDate,x=len(self.lblDate._text)*10+15)
        
        # Deletes old description and replaces it with latest version.
        self.entryDescription.delete(1.0,END)
        self.entryDescription.insert(1.0,taskDict["description"])

    def flagFuncAttrEditing(self):
        self.flagAttributeEditing = not self.flagAttributeEditing


    def getTaskButton(self):
        taskButton = Checkbox(self,x=20,y=20,size=(50,50),command=self.taskButtonCommand,\
                              commandArgs=self.commandArgs)
        return taskButton

    def checkAttributes(self):
        if self.taskDate == "":
            self.lblDate.configure(text="no date")
        
        if self.taskTime == "":
            self.lblTime.configure(text="no time")
    
    def checkNewTitle(self,newTitle):
        if newTitle.strip() == "":
            message = "Invalid name entered."
            return False,message
        else:
            return newTitle,None
    
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
            self.lblTaskName.configure(font=(self.fontName,self.titleFontSize))
    
    def bindEventListeners(self):
        for each in self.hoverWidgets:
            # Binding occurring directly with widget.
            self.hoverWidgets[each].bind("<Enter>",lambda event,widgetName=each:self.onhover(widgetName))
            self.hoverWidgets[each].bind("<Leave>",lambda event,widgetName=each:self.onhoverexit(widgetName))

    def onhover(self,widgetName):
        widget = self.hoverWidgets[widgetName]
        try:
            # Gets the original widget font
            widgetFont = self.hoverWidgetFonts[widgetName]
        except:
            widgetFont = widget._font
            self.hoverWidgetFonts[widgetName] = widgetFont
        
        newFont = (widgetFont[0],widgetFont[1],"underline")
        widget.configure(font=newFont,text_color=self.accent)
    
    def onhoverexit(self,widgetName):
        widget = self.hoverWidgets[widgetName]
        widget.configure(font=self.hoverWidgetFonts[widgetName],text_color=("black","white"))
    
    def btnCancelClicked(self):
        self.entryDescription.delete(1.0,"end")
        self.entryDescription.insert(1.0,self.taskDescription)
        self.btnCancel.place_forget()
        self.btnSaveDescription.place_forget()
        self.lblDescription.focus()

    def descriptionBoxEnter(self):
        self.btnSaveDescription.place(in_=self.entryDescription,x=650,y=260)
        self.btnCancel.place(in_=self.btnSaveDescription,x=-125)

        self.origin.unbind("<Return>")
        

    def saveDescription(self):
        # Cursor removed from description box.
        self.lblDescription.focus()

        # Retrieving the changed description from the box.
        newDescription = self.entryDescription.get(1.0,END).strip()

        # Replacing the value in the attributes list and the class attribute.
        self.taskAttributes["description"] = newDescription
        self.taskDescription = newDescription

        # Uploading the changes to the JSON file.
        listName = self.taskAttributes["listName"]
        uploadTask(self.userPath,self.taskAttributes,listName)
        print(newDescription)
        self.lblSave.place(in_=self.entryDescription,y=255)

        # Update task details and details panel displayed on other screens.
        self.mainWindow.updateTasks()

        # Removing both save and cancel buttons
        self.origin.bindEnterKey()
        self.btnCancel.place_forget()
        self.btnSaveDescription.place_forget()

        # Removing the save label after 1 second.
        self.after(1000,self.lblSave.place_forget)




        
    
"""root = CTk()
root.geometry("1920x1080")

myPanel = DetailsPanel(root,{"title":"Revise","date":"16/10/2024","description":"You have to finish all of your homework first","time":"","priority":"","taskID":"2ks90a"},"hello")
myPanel.pack()

root.mainloop()"""
        



# Details panel for tasks
from customtkinter import *
from lib.checkbox_customTk import Checkbox
from PIL import Image
from lib.uploadTask import uploadTask


class DetailsPanel(CTkFrame):
    def __init__(self,master,origin,userPath,taskAttributes,taskButtonCommand,commandArgs,\
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
        self.imgAlarm = CTkImage(Image.open("icons//alarm.png"),size=(25,25))
        self.btnSetReminder = CTkButton(self,text="Set reminder",font=(globalFontName,25),fg_color=self.accent,width=70,\
                                        image=self.imgAlarm)

    def placeWidgets(self):
        self.btnClose.place(x=740,y=20)
        self.lblTaskName.place(x=80,y=20)
        self.btnSetReminder.place(in_=self.lblTaskName,x=400,y=5)
        self.lblDate.place(in_=self.lblTaskName,y=45)
        self.lblTime.place(in_=self.lblDate,x=12*(len(self.lblDate.cget("text"))))
        self.lblDescription.place(x=25,y=110)
        self.entryDescription.place(in_=self.lblDescription,y=30)
        self.taskButton.placeWidget()
        #self.btnSaveDescription.place(in_=self.entryDescription,x=220,y=190)
    
    def getTaskButton(self):
        taskButton = Checkbox(self,x=20,y=20,size=(50,50),command=self.taskButtonCommand,\
                              commandArgs=self.commandArgs)
        return taskButton

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
            self.lblTaskName.configure(font=(self.fontName,self.titleFontSize))
    
    def bindEventListeners(self):
        for each in self.hoverWidgets:
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
        



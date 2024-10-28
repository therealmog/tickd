# Details panel for tasks
from customtkinter import *
from lib.checkbox_customTk import Checkbox
from PIL import Image
from lib.uploadTask import uploadTask


class DetailsPanel(CTkFrame):
    def __init__(self,master,userPath,taskAttributes,taskButtonCommand,commandArgs,fontName="Bahnschrift",accent="dodgerblue2"):
        super().__init__(master,width=600,height=380,border_width=3,border_color="white")

        self.taskAttributes = taskAttributes
        self.taskName = taskAttributes["title"]
        self.taskDate = taskAttributes["date"]
        self.taskTime = taskAttributes["time"]
        self.taskPriority = taskAttributes["priority"]
        self.taskID = taskAttributes["taskID"]
        self.fontName = fontName
        self.accent = accent
        self.userPath = userPath

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
        self.lblTaskName = CTkLabel(self,text=self.taskName,font=(globalFontName,30),cursor="hand2")
        
        self.checkTitleLength()
        
        self.taskButton = self.getTaskButton()
        self.lblDate = CTkLabel(self,text=self.taskDate,font=(globalFontName,20),cursor="hand2")
        self.lblTime = CTkLabel(self,text=self.taskTime,font=(globalFontName,20),cursor="hand2")
        self.lblDescription = CTkLabel(self,text="description:",font=(globalFontName,20))
        self.entryDescription = CTkTextbox(self,width=550,height=180,font=(globalFontName,20),wrap=WORD,activate_scrollbars=True)
        self.entryDescription.insert("1.0",self.taskDescription)
        self.entryDescription.bind("<Button-1>",lambda event: self.descriptionBoxEnter())

        self.checkAttributes()

        self.hoverWidgets = {"lblTaskName":self.lblTaskName,
                        "lblDate":self.lblDate,
                        "lblTime":self.lblTime,
                        }
        self.hoverWidgetFonts = {}

        self.imgSave = CTkImage(Image.open("save.png"),size=(25,25))
        self.btnSaveDescription = CTkButton(self,text="save",font=(globalFontName,25),fg_color=self.accent,command=lambda:self.saveDescription(),width=70,image=self.imgSave)
        self.lblSave = CTkLabel(self,text="Saved description.",text_color="limegreen",font=(globalFontName,25))
        self.imgCancel = CTkImage(Image.open("cancel.png"),size=(25,25))
        self.btnCancel = CTkButton(self,text="cancel",fg_color="red",image=self.imgCancel,font=(globalFontName,25),width=80)

    def placeWidgets(self):
        self.lblTaskName.place(x=75,y=20)
        self.lblDate.place(in_=self.lblTaskName,y=35)
        self.lblTime.place(in_=self.lblDate,x=12*(len(self.lblDate.cget("text"))))
        self.lblDescription.place(x=25,y=100)
        self.entryDescription.place(in_=self.lblDescription,y=30)
        self.taskButton.placeWidget()
        #self.btnSaveDescription.place(in_=self.entryDescription,x=220,y=190)
    
    def getTaskButton(self):
        taskButton = Checkbox(self,x=20,y=20,size=(50,50),command=self.taskButtonCommand,commandArgs=self.commandArgs)
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
            self.lblTaskName.configure(font=(self.fontName,self.titleFontSize,"underline"))
    
    def bindEventListeners(self):
        for each in self.hoverWidgets:
            print(each)
            self.hoverWidgets[each].bind("<Enter>",lambda event,widgetName=each:self.onhover(widgetName))
            self.hoverWidgets[each].bind("<Leave>",lambda event,widgetName=each:self.onhoverexit(widgetName))

    def onhover(self,widgetName):
        widget = self.hoverWidgets[widgetName]
        try:
            widgetFont = self.hoverWidgetFonts[widgetName]
        except:
            widgetFont = widget._font
            self.hoverWidgetFonts[widgetName] = widgetFont
        
        newFont = (widgetFont[0],widgetFont[1],"underline")
        widget.configure(font=newFont,text_color=self.accent)
    
    def onhoverexit(self,widgetName):
        widget = self.hoverWidgets[widgetName]
        widget.configure(font=self.hoverWidgetFonts[widgetName],text_color="white")
    
    def btnCancelClicked(self):
        pass

    def descriptionBoxEnter(self):
        self.btnSaveDescription.place(in_=self.entryDescription,x=450,y=190)
        self.btnCancel.place(in_=self.btnSaveDescription,x=-125)

    def saveDescription(self):
        self.lblDescription.focus()
        newDescription = self.entryDescription.get(1.0,END).strip()
        self.taskAttributes["description"] = newDescription

        listName = self.taskAttributes["listName"]
        uploadTask(self.userPath,self.taskAttributes,listName)
        print(newDescription)
        self.lblSave.place(in_=self.btnSaveDescription,x=-60)
        self.after(1000,self.lblSave.place_forget)


        
    
"""root = CTk()
root.geometry("1920x1080")

myPanel = DetailsPanel(root,{"title":"Revise","date":"16/10/2024","description":"You have to finish all of your homework first","time":"","priority":"","taskID":"2ks90a"},"hello")
myPanel.pack()

root.mainloop()"""
        



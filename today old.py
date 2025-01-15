from customtkinter import *
from PIL import Image
from datetime import date,timedelta
from lib.getDetails import getAllDetails,getDetailsIndividual,writeToAuthDetails
from lib.submitBtn import SubmitButton
from lib.createTaskDict import createTaskDict
from lib.checkDate import checkDate
from lib.checkTime import checkTime
from lib.task import Task
from lib.loadTaskList import loadTaskList
from lib.getTasks import getTasks
from lib.uploadTask import uploadTask
from lib.updateTaskListData import updateTaskListData
from lib.detailsPanel import DetailsPanel
from tkinter import messagebox
from lib.getOverdue import getOverdue
from lib.getListImgs import getListImgs


class Today(CTkFrame):
    
    globalFontName = "Bahnschrift"
    textgrey="#9e9f9f"
    def __init__(self,mainWindow,email,userPath,todaysDate,userAccent="dodgerblue2",listName="inbox",):
        """The class object used to generate the Today view, which is the landing page of the app once the user has logged in.
    
    It should only be declared once in the main function, and then the declared object can be called multiple times."""
        
        
        super().__init__(mainWindow,width=1400,height=900,fg_color=("white","gray9"),border_color="gray7",border_width=5,corner_radius=20)
        
        self.mainWindow = mainWindow
        self.mainWindow.title("Today - Tickd")

        self.userPath = userPath
        self.listName = listName
        self.email = email


        self.accent = userAccent
        self.userName = getDetailsIndividual(self.email)

        self.elements = {
            
        } 

        # Calculated and passed into this class from app
        if isinstance(todaysDate,str):
            self.todaysDate = todaysDate
        else:
            self.todaysDate = todaysDate.strftime("%A, %d %B %Y")

        self.widgets()
        self.placeWidgets()


        self.entriesDict = {
            "entryTask":self.entryTask,
            "entryDate":self.entryDate,
            "entryTime":self.entryTime,
            "dropdownPriority":self.dropdownPriority
        }

        

        self.entryTask.bind("<Return>",lambda event:self.taskSubmitted())
        self.bindTaskEntry()

        self.loadTasks()

        #self.bind("<Configure>",lambda event:self.resizeFrame())

    #------------------------# Widgets and placing #-------------------------#    
    def widgets(self):
        globalFontName = self.globalFontName
        
        print("Bonjour.")
        self.lblListName = CTkLabel(self,text=self.listName.title(),font=(globalFontName,40))
    
        self.lblDate = CTkLabel(self,text=self.todaysDate,font=(globalFontName,20)) 
        self.imgLogo = CTkImage(light_image=Image.open("logo//whiteBGLogo.png"),dark_image=Image.open("logo//blackBGLogo.png"),size=(155,49))
        self.logoPanel = CTkLabel(self,text="",image=self.imgLogo)
        self.entryTask = CTkEntry(self,placeholder_text="Enter a task...",font=(globalFontName,30),width=650,corner_radius=20)
        

        self.entryDate = CTkEntry(self,placeholder_text="date",font=(globalFontName,22),corner_radius=20,border_width=0)
        self.entryTime = CTkEntry(self,placeholder_text="time",font=(globalFontName,22),corner_radius=20,border_width=0)
        self.dropdownPriority = CTkOptionMenu(self,values=["priority","P1","P2","P3"],font=(globalFontName,22),dropdown_font=(globalFontName,20),corner_radius=20,fg_color=("#f9f9fa","#353639"),button_color=("#f9f9fa","#353639"),text_color=self.textgrey,command=self.priorityCallback)
        self.btnTaskSubmit = SubmitButton(self,colour=self.accent,buttonSize=(35,35),command=self.taskSubmitted,radius=60)
        
        self.lblNoTasks = CTkLabel(self,text="You have no tasks.",font=(globalFontName,40))

        """self.sampleDetailsPanel = DetailsPanel(self,{"title": "Welcome!", "date": "16/10/2024", "taskID": "TjAiDX", "completed": "False", "time": "", "priority": "", "description": ""},
                                               self.taskCompleted,{"taskID":"TjAiDX"})"""
        self.entries = [self.entryDate,self.dropdownPriority,self.entryTime]

        self.taskFrame = CTkScrollableFrame(self,width=410,height=720,fg_color=("white","#191616"))
        self.overdueFrame = CTkScrollableFrame(self,width=410,height=200,fg_color=("white","#191616"))
        self.lblOverdue = CTkLabel(self,text="OVERDUE",font=(globalFontName,30))

        listImgs = getListImgs()
        try:
            image = listImgs[self.listName.capitalize()]
            self.lblOtherTasks = CTkLabel(self,text=f" {self.listName.capitalize()} - ",font=(globalFontName,30),image=image,compound="left")
        except KeyError:
            print(f"Image does not exist for {self.listName}")
            self.lblOtherTasks = CTkLabel(self,text=f"{self.listName.capitalize()} - ",font=(globalFontName,30))

        

    def placeWidgets(self):
        #self.place(relx=0.5,rely=0.5,anchor="center")
        #self.panelImgBG.place(x=0,y=0)
        
        self.lblListName.place(x=125,y=50)
        self.lblDate.place(in_=self.lblListName,x=0,y=-25)
        self.logoPanel.place(relx=0.98,y=40,anchor=E)
        self.entryTask.place(in_=self.lblListName,x=350,y=-20)

        #self.sampleDetailsPanel.place(in_=self.entryTask,x=50,y=100)

        self.currentAttribute = ""

        

    def frameDimensions(self):
        print(f"Width: {self.winfo_screenwidth()}, Height: {self.winfo_screenheight()}")
        frameX = 0.68 * self.winfo_screenwidth()
        frameY = 0.68 * self.winfo_screenheight()

        return frameX, frameY
        
    def resizeFrame(self):
        
        #print(self.winfo_width(),"by",self.winfo_height())
        frameX = 0.95 * self.winfo_width()
        frameY = 0.95 * self.winfo_height()

        self.configure(width=frameX,height=frameY)
        #self.panelImgBG._image
        
        
        if self.winfo_width() < 1505:
            self.entryTask.place_forget()

        if self.winfo_width() > 1505:
            self.entryTask.place(in_=self.logoPanel,x=-650,y=10)

    def loadTasks(self): # Should only be run at the start of the program
        
        self.taskList = getTasks(self.taskFrame,self.userPath,"inbox",self.accent,command=self.taskCompleted,fontName=self.globalFontName)
        
        """# Getting a list with the same tasks, but the master for these tasks is overdueFrame. 
        self.overdueList = getTasks(self.overdueFrame,self.userPath,"inbox",self.accent,command=self.taskCompleted,fontName=self.globalFontName)"""
        

        self.detailPanels = {} # taskID:detailPanelObj
        self.currentDisplayed = "" # stores taskID of task with details panel displayed.

        self.overdueList = []
        
        if self.taskList != False:
            # Gathering overdue tasks
            self.overdueDict = getOverdue(self.taskList) # Returns a dictionary

            #print(self.overdueDict)
            print(list(self.overdueDict.keys()))
            for each in self.taskList.copy():
                if each.attributes["taskID"] in list(self.overdueDict.keys()):
                    self.taskList.remove(each)
                    #print(f"Removing {each.attributes["taskID"]}")
                    overdueTask = Task(self.overdueFrame,each.attributes,accent=self.accent,font=self.globalFontName,command=self.taskCompleted)
                    self.overdueList.append(overdueTask)
                    self.setDetailsPanel(overdueTask,each.attributes["taskID"])


            self.lblNoTasks.place_forget()
           
            newOtherTasksText = f" {self.listName.capitalize()} - {len(self.taskList)}"
            self.lblOtherTasks.configure(text=newOtherTasksText)

            newOverdueTasksText = f"OVERDUE - {len(self.overdueList)}"
            self.lblOverdue.configure(text=newOverdueTasksText)

            # Placing tasks in taskList
            if len(self.taskList)>=1:
                self.taskList[0].grid(row=0,column=0,pady=(5,10))
                
                taskID = self.taskList[0].attributes["taskID"]
                self.setDetailsPanel(self.taskList[0],taskID)
                i = 1 # Indicates column for taskFrame grid

                for each in range(1,len(self.taskList)): # Starts with second item
                    task = self.taskList[each]
                    task.grid(row=i,column=0,pady=10)
                    i+=1
                    
                    taskID = task.attributes["taskID"]
                    self.setDetailsPanel(task,taskID)

            
            if len(self.overdueList) != 0:
                self.overdueList[0].grid(row=1,column=0,pady=(20,10))

                i = 2
                for each in range(1,len(self.overdueList)):
                    widget = self.overdueList[each]
                    
                    widget.grid(row=i,column=0,pady=10)
                    i+=1
            
                self.lblOverdue.place(in_=self.lblListName,x=-5,y=100)
                self.overdueFrame.place(in_=self.lblOverdue,y=30)

                if len(self.taskList) >=1:
                    self.lblOtherTasks.place(in_=self.lblOverdue,y=280)
                    self.taskFrame.place(in_=self.lblOtherTasks,y=30)
                    #self.taskFrame.configure(height=500)
            else:
                if len(self.taskList) >=1:
                    self.lblOtherTasks.place(in_=self.lblListName,x=-5,y=100)
                    self.taskFrame.place(in_=self.lblOtherTasks,y=35)
                else:
                    self.lblNoTasks.place(x=25,y=150)
            
            

        else:
            self.lblNoTasks.place(x=25,y=150)
    
    def renameMainWin(self):
        self.mainWindow.title("Today - Tickd")
        

    #--------------------# Task entry and button functions #------------------#
    def taskEntryEnter(self):
        self.placeAttributeEntries()   
        #self.entryTask.unbind("<Key>")
      
    
    def attributeEntered(self):
        """This ensures that the attribute entries are always displayed if they are clicked on, especially since
        when you click out of another attribute entry, it removes the entries, so this places them back."""
        self.placeAttributeEntries()
        

    def attributeLeave(self):
        """Checks if any of the attribute entries are filled. If they are, then none of the entries will be removed.
        If none of them are filled then all are removed. This is called whenever the entry is left"""
        filled = False
        for each in self.entries:
            if each.get() != "" and each.get() !="priority":
                filled = True

        if filled == False:
            self.removeAttributeEntries()

    
    def taskSubmitted(self):
        # Input received from entry box.
        title = self.entryTask.get()

        # The task's attributes dictionary
        attributes = {}

        if title == "":
            messagebox.showinfo("Cannot create task","Please enter a task title before submitting.")
        else: # Start to interpret attributes
            dateInput = self.entryDate.get()
            dateInput = dateInput.strip()
            if dateInput == "":
                # No date has been entered.
                date = "" 
            else:
                date,message = checkDate(userInput=dateInput)

            if date == False: # Date is set as False by checkDate function
                # Displays error message
                messagebox.showerror("Invalid date",message)
                #self.messageVar.set(message)
            else:
                # Adding date to the task attributes dict.
                attributes["date"] = date

                # Getting the input from the time entry box.
                timeInput = self.entryTime.get()
                if timeInput == "":
                    time = ""
                else:
                    # Validates time input.
                    time,message = checkTime(userInput=timeInput)

                if time == False:
                    # Displays error message for time.
                    #self.messageVar.set(message)
                    messagebox.showerror("Invalid time",message)
                else:
                    # Adds time to the attributes dict.
                    attributes["time"] = time                
                
                    
                    if self.dropdownPriority.get() != "priority":
                        # Since priority comes from option menu, it can be added straight
                        # to the attributes dict.
                        attributes["priority"] = self.dropdownPriority.get()
                    else:
                        attributes["priority"] = ""
                    

                    # Adds extra attributes to be altered later if desired.
                    attributes["description"] = ""
                    attributes["listName"] = "inbox"
                    
                    # All the attributes are brought together to create a task dictionary
                    # to be written to the task list JSON file.
                    taskDict = createTaskDict(title,date,attributes)
                    self.resetEntry(["entryTask","entryDate","entryTime","dropdownPriority"])

                    # Task is written to the specified list.
                    uploadTask(self.userPath,taskDict,listName="inbox")


                    
                    # Task is placed onto the screen.
                    self.placeNewTask(taskDict)


                    print([x.attributes["title"] for x in self.taskList])

    def placeNewTask(self,taskDict):
        newTask = Task(self.taskFrame,taskDict,self.accent,command=self.taskCompleted,font=self.globalFontName)
        
        if bool(self.taskList) == False:
            self.lblNoTasks.place_forget()
            self.taskList = []

            if self.overdueFrame.winfo_ismapped():
                self.lblOtherTasks.place(in_=self.lblOverdue,y=300)
                self.taskFrame.place(in_=self.lblOtherTasks,y=30)
            else:
                self.lblOtherTasks.place(in_=self.lblListName,x=-5,y=100)
                self.taskFrame.place(in_=self.lblOtherTasks,y=30)
            newTask.grid(row=0,column=0,pady=10)
        else:
            newTask.grid(row=len(self.taskList),column=0,pady=10)

        taskID = newTask.attributes["taskID"]
        self.setDetailsPanel(newTask,taskID)
        self.taskList.append(newTask)

        self.lblOtherTasks.configure(text=f" {self.listName.capitalize()} - {len(self.taskList)}")
    
    def setDetailsPanel(self,task,taskID):
        self.detailPanels[taskID] = DetailsPanel(self,self,self.userPath,task.attributes,self.taskCompleted,{"taskID":taskID},self.globalFontName,self.accent)
        task.bind("<Button-1>",lambda event,taskID=taskID:self.showDetailsPanel(taskID))
        task.lblTitle.bind("<Button-1>",lambda event,taskID=taskID:self.showDetailsPanel(taskID))
        task.lblDate.bind("<Button-1>",lambda event,taskID=taskID:self.showDetailsPanel(taskID))

    def showDetailsPanel(self,taskID):
        if self.winfo_width() < 1505:
            messagebox.showinfo("Can't display details panel.","Increase your window width to\ndisplay the details panel for this task.")
        else:
            if self.currentDisplayed != "":
                self.detailPanels[self.currentDisplayed].place_forget() # Removes current display panel.
            print("you clicked me")
            taskDetailsPanel = self.detailPanels[taskID]
            self.currentDisplayed = taskID

            taskDetailsPanel.place(in_=self.entryTask,y=150)


    def taskCompleted(self,taskID):
        taskListData = loadTaskList(self.userPath,"inbox")

        allTasksDict = taskListData["tasks"]
        try:
            completedTasksDict = taskListData["completed"]
        except:
            taskListData["completed"] = {}
            completedTasksDict = taskListData["completed"]
        
                
        taskDict = ""
        for each in allTasksDict.copy():
            if each == taskID: # Dictionary key for each task in allTasksDict is the taskID
                taskDict = allTasksDict[each]
                allTasksDict.pop(each)

        taskDict["completed"] = "True"

        completedTasksDict[taskID] = taskDict

        taskListData["tasks"] = allTasksDict
        taskListData["completed"] = completedTasksDict

        updateTaskListData(taskListData,self.userPath,"inbox")
        
        if taskID in self.overdueDict:
            for each in self.overdueList.copy():
                if each.attributes["taskID"] == taskID:
                    each.attributes["completed"] = "True"
        else:
            for each in self.taskList:
                if each.attributes["taskID"] == taskID:
                    each.attributes["completed"] = "True"
        
        self.detailPanels[taskID].place_forget()
        self.detailPanels.pop(taskID)
        self.currentDisplayed = ""
        self.removeIfCompleted()

        #print(self.taskList)
        

    def removeIfCompleted(self):
        for each in self.taskList:
            if each.attributes["completed"] == "True":
                print(f"Removing {each.attributes["title"]}")
                self.placeTasks(self.taskList.index(each),overdue=False)
        
        for each in self.overdueList:
            if each.attributes["completed"] == "True":
                print(f"Removing {each.attributes["title"]}")
                self.placeTasks(self.overdueList.index(each),overdue=True)
        
        self.lblOtherTasks.configure(text=f" {self.listName.capitalize()} - {len(self.taskList)}")
        
        if len(self.taskList) == 0 and len(self.overdueList) == 0:
            self.taskFrame.place_forget()
            self.lblOtherTasks.place_forget()
            self.overdueFrame.place_forget()
            self.lblOverdue.place_forget()
            self.lblNoTasks.place(x=25,y=150)


    def placeTasks(self,removedIndex,overdue:bool):
        print("hello")
        # Removes completed task by index
        # Then places all tasks again after the one which has been removed.

        if overdue:
            list = self.overdueList
        else:
            list = self.taskList
        
        for each in range(removedIndex,len(list)):
            list[each].grid_forget()

        if not overdue:
            self.taskList.pop(removedIndex)
        else:
            self.overdueList.pop(removedIndex)
        

        for each in range(removedIndex,len(list)): # Starts with index which was removed
            task = list[each]
            task.grid(row=each,column=0,pady=10)
     

    def priorityCallback(self,event):
        if self.dropdownPriority.get() == "priority":
            self.dropdownPriority.configure(text_color="#9e9f9f")
        else:
            self.dropdownPriority.configure(text_color=("black","white"))

    def bindEnterKey(self):
        self.bind("<Return>",lambda event: self.taskSubmitted)
        #print("enter is back")

    def placeAttributeEntries(self):
        self.btnTaskSubmit.place(in_=self.entryTask,x=650)
        self.bindEnterKey()

        entries = [self.entryDate,self.entryTime,self.dropdownPriority]
        entries[0].place(in_=self.entryTask,y=50)
        for each in range(1,len(entries)):
            entries[each].place(in_=entries[each-1],x=150)
    
    def removeAttributeEntries(self):
        self.btnTaskSubmit.place_forget()
        self.btnTaskSubmit.unbind("<Return>")

        entries = [self.entryDate,self.entryTime,self.dropdownPriority,self.btnTaskSubmit]
        for each in range(0,len(entries)):
            entries[each].place_forget()
            
    def resetEntry(self,entries:list):
        entriesDict = self.entriesDict
        for each in entries:
            if "dropdown" in each:
                valuesList = entriesDict[each]._values 
                entriesDict[each].set(valuesList[0])
                entriesDict[each].configure(text_color=self.textgrey)
            else:
                entriesDict[each].delete(0,"end")


    def bindTaskEntry(self):
        self.entryTask.bind("<FocusIn>",lambda event:self.taskEntryEnter())
        self.entryTask.bind("<FocusOut>",lambda event:self.attributeLeave())
        
        for each in self.entries:
            each.bind("<FocusIn>",lambda event:self.attributeEntered())
            each.bind("<FocusOut>",lambda event:self.attributeLeave())


#today = Today(mainWindow=None,email="omar@gmail.com",userPath="users//omar@gmail.com",theme="dark",listName="inbox")

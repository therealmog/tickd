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
from lib.getValueWindow import GetValueWin
import os
import json
from lib.checkListName import checkListName



class List(CTkFrame):
    
    globalFontName = "Bahnschrift"
    textgrey="#9e9f9f"
    def __init__(self,mainWindow,email,userPath,todaysDate,userAccent="dodgerblue2",listName="inbox",):
        """The class for generating frames for individual lists."""
        
        
        super().__init__(mainWindow,width=1400,height=900,fg_color=("white","gray9"),border_color="gray7",border_width=5)
        
        self.mainWindow = mainWindow

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


        # Indicates whether list is renameable, shareable, or deleteable.
        # Keeping these as 3 separate variables allows them to be toggled separately.
        # e.g. a list could be renameable and deleteable, but not shareable.
        # However, at the moment I have not made any lists like that so they are all toggled at the same time.
        if self.listName.lower() == "inbox" or self.listName.lower() == "starred":
            # If these are toggled, the respective buttons are made for these.
            self.renameable = False
            self.shareable = False
            self.deleteable = False
        else:
            self.renameable = True
            self.shareable = True
            self.deleteable = True

        self.widgets()
        self.placeWidgets()

        # Dictionary to allow task entries to be referenced.
        self.entriesDict = {
            "entryTask":self.entryTask,
            "entryDate":self.entryDate,
            "entryTime":self.entryTime,
            "dropdownPriority":self.dropdownPriority
        }

        
        # Allows the user to press the Enter key to submit the task.
        self.entryTask.bind("<Return>",lambda event:self.taskSubmitted())
        # Makes the date, time and priority entries appear when the user enters the task entry.
        self.bindTaskEntry()

        # Loads the tasks from the JSON file.
        self.loadTasks()
        self.btnTaskSubmit.bind("<Return>",lambda event:self.taskSubmitted())

        # Flag for when renaming the list
        self.flagRenaming = False

    #------------------------# Widgets and placing #-------------------------#    
    def widgets(self):
        globalFontName = self.globalFontName
        
        print("Bonjour.")
        self.lblListName = CTkLabel(self,text=self.listName.capitalize(),font=(globalFontName,40),cursor="pencil")

        self.lblListName.bind("<Button-1>",lambda event:self.checkRenameList())

        
        smallerListImgs = getListImgs((20,20))
        if self.renameable:
            self.btnRename = CTkButton(self,text="Rename list",font=(self.globalFontName,20),width=130,image=smallerListImgs["Rename"],compound="left",command=self.checkRenameList,
                                       fg_color=self.accent)
        
        if self.shareable:
            self.btnShare = CTkButton(self,text="Share list",font=(self.globalFontName,20),width=130,image=smallerListImgs["Share"],compound="left",
                                      fg_color=self.accent)

        if self.deleteable:
            self.btnDelete = CTkButton(self,text="Delete list",font=(self.globalFontName,20),width=130,image=smallerListImgs["Delete"],compound="left",command=self.deleteList,
                                       fg_color=self.accent)

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

        #self.balloonRename = Balloon(self,balloonmsg="Click to rename the list.")
        

    def placeWidgets(self):
        #self.place(relx=0.5,rely=0.5,anchor="center")
        #self.panelImgBG.place(x=0,y=0)
        
        self.lblListName.place(x=125,y=50)
        self.lblDate.place(in_=self.lblListName,x=0,y=-25)
        self.logoPanel.place(relx=0.98,y=40,anchor=E)
        self.entryTask.place(in_=self.logoPanel,x=-250)

        #self.sampleDetailsPanel.place(in_=self.entryTask,x=50,y=100)

        self.currentAttribute = ""

        if self.renameable and self.deleteable and self.shareable:
            self.btnRename.place(in_=self.lblListName,y=55)
            self.btnDelete.place(in_=self.btnRename,x=160)
            self.btnShare.place(in_=self.btnDelete,x=145)
        

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

    def renameList(self,newName):
        # Gets previous name and path.
        oldName = self.listName
        oldPath = f"{self.userPath}//{self.listName}.json"

        # Creates new path
        newPath = f"{self.userPath}//{newName}.json"

        # Renames class attribute and labels.
        self.listName = newName
        self.lblListName.configure(text=self.listName.capitalize()) # Top list label

        if self.taskList != False:
            # Label above task frame
            self.lblOtherTasks.configure(text=f"{self.listName} - {len(self.taskList)}")


        # Uses os module to rename JSON file.
        os.rename(oldPath,newPath)
        self.mainWindow.title(f"{newName.capitalize()} - Tickd")

        # Changes value of button in MyLists frame
        # Iterates through list of buttons in MyLists frame.
        for each in self.mainWindow.frameMyLists.customListsBtnsArray:
            if each._text == oldName:
                each.configure(text=newName)
        
        # Change listName attribute of each task
        with open(newPath,"r") as f:
            listData = json.load(f)
        
        try:
            completedData = listData["completed"]
            for each in completedData:
                completedData[each]["listName"] = newName
        except: pass

        currentTasksData = listData["tasks"]

        for each in currentTasksData:
            currentTasksData[each]["listName"] = newName
        
        with open(newPath,"w") as f:
            json.dump(listData,f,indent=4)
        
        
        
        



    def checkRenameList(self):
        notAllowedValues = ["inbox","today","starred"]
        allowedToRename = True

        # Checks if list is a Tickd default quickly by checking name. 
        for each in notAllowedValues:
            if self.listName.lower() == each:
                allowedToRename = False
        
        if not allowedToRename:
            messagebox.showerror("Cannot rename this list","This list cannot be renamed since it is a Tickd default.")
        else:
            if self.flagRenaming:
                messagebox.showerror("Window already active",
                                     "Rename window already active. Please close it before opening another one.")
            else:
                self.flagRenaming = True
                winTitle = f"Rename '{self.listName}'"
                # Calls a GetValueWin object
                GetValueWin(attributeName="list name",assigningFunc=self.renameList,validationFunc=checkListName,
                            validationFuncArgs={"userPath":self.userPath},accent=self.accent,
                            flagFunc=self.changeFlagRenaming,customTitle=winTitle)
    
    def changeFlagRenaming(self):
       self.flagRenaming = not self.flagRenaming

    def loadTasks(self): # Should only be run once at the start of the program

        # Gets a list of Task objects.
        self.taskList = getTasks(self.taskFrame,self.userPath,self.listName,self.accent,command=self.taskCompleted,fontName=self.globalFontName,displayListName=False)
               
        # Creates the list for details panels
        self.detailPanels = {} # taskID:detailPanelObj
        self.currentDisplayed = "" # stores taskID of task with details panel displayed.

        # Creates a list for overdue task objects
        self.overdueList = []
        self.overdueDict = {}
        
        # self.taskList = False indicates that there are no tasks.
        # If there are no tasks at all, there will be no overdue tasks either.
        if self.taskList != False:
            # Gathering overdue tasks
            self.overdueDict = getOverdue(self.taskList) # Returns a dictionary

            if len(self.overdueDict) > 0:
                for each in self.taskList.copy():
                    if each.attributes["taskID"] in list(self.overdueDict.keys()):
                        self.taskList.remove(each)

                        # Creates a new Task object with the same details as the removed object.
                        overdueTask = Task(self.overdueFrame,each.attributes,userPath=self.userPath,accent=self.accent,font=self.globalFontName,command=self.taskCompleted,displayListName=False)

                        # New object added to overdue list and details panel binded.
                        self.overdueList.append(overdueTask)
                        self.setDetailsPanel(overdueTask,each.attributes["taskID"])

            # Creates labels for the regular lists
            newOtherTasksText = f" {self.listName.capitalize()} - {len(self.taskList)}"
            self.lblOtherTasks.configure(text=newOtherTasksText)

            newOverdueTasksText = f"OVERDUE - {len(self.overdueList)}"
            self.lblOverdue.configure(text=newOverdueTasksText)

            # Placing tasks in taskList
            # First, tasks are ordered.
            self.orderList(self.taskList)

            # grid method used to display tasks in scrollable frame
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

            # Overdue tasks displayed in overdueFrame
            if len(self.overdueList) != 0:
                self.overdueList[0].grid(row=1,column=0,pady=(20,10))

                i = 2
                for each in range(1,len(self.overdueList)):
                    widget = self.overdueList[each]
                    
                    widget.grid(row=i,column=0,pady=10)
                    i+=1
            
                # Overdue tasks always placed at the top to grab user's attention.
                self.lblOverdue.place(in_=self.lblListName,x=-5,y=115)
                self.overdueFrame.place(in_=self.lblOverdue,y=30)

                # If other tasks are also there which aren't overdue.
                if len(self.taskList)>0:
                    self.lblOtherTasks.place(in_=self.lblOverdue,y=295)
                    self.taskFrame.place(in_=self.lblOtherTasks,y=30)
                    
            else:
                # No overdue tasks
                # Places task frame and label at the top.
                self.lblOtherTasks.place(in_=self.lblListName,x=-5,y=100)
                self.taskFrame.place(in_=self.lblOtherTasks,y=35)
                
            
            

        else:
            # Since there are no tasks, label is placed.
            self.lblNoTasks.place(x=25,y=150)
    
    def renameMainWin(self):
        self.mainWindow.title(f"{self.listName.capitalize()} - Tickd")
        

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
                    attributes["listName"] = self.listName
                    attributes["starred"] = "False"
                    
                    # All the attributes are brought together to create a task dictionary
                    # to be written to the task list JSON file.
                    taskDict = createTaskDict(title,date,attributes)
                    self.resetEntry(["entryTask","entryDate","entryTime","dropdownPriority"])

                    # Task is written to the specified list.
                    uploadTask(self.userPath,taskDict,listName=self.listName)


                    
                    # Task is placed onto the screen.
                    self.placeNewTask(taskDict)

                    # Checks all screens for any new tasks added.
                    self.mainWindow.checkNewTasksAll()
                    
                    
    
    def deleteListFromFolder(self):
        path = f"{self.userPath}//{self.listName}.json"

        os.remove(path)


    def deleteList(self):
        check1 = messagebox.askyesnocancel("Are you sure?",f"Are you sure you would like to delete the list '{self.listName}'?")
        
        if check1:
            check2 = messagebox.askyesnocancel("Confirm list deletion",
                                               "Your list will be permanently deleted.\nAre you sure you would like to continue and delete this list?")
            if check2:
                self.deleteListFromFolder()

                # Remove from buttons in "My lists"
                for each in self.mainWindow.frameMyLists.customListsBtnsArray:
                    if each._text == self.listName:
                        each.place_forget()
                        self.mainWindow.frameMyLists.customListsBtnsArray.remove(each)
                        self.mainWindow.frameMyLists.placeCustomLists()
                        break
                self.mainWindow.loadFrame("myLists")
                

            else:
                messagebox.showinfo("List not deleted.","Your list has not been deleted.")

    def orderList(self,listToSort):
        """Orders list in terms of priority."""
        
        # These variables are necessary to know where to place the lower priority tasks.
        # e.g. P2 tasks will be placed after P1, indicated by the noOfP1 index.
        noOfP1 = 0
        noOfP2 = 0
        noOfP3 = 0

        for each in listToSort:
            if each.attributes["priority"] == "P1":
                noOfP1 +=1
            elif each.attributes["priority"] == "P2":
                noOfP2 +=1
            elif each.attributes["priority"] == "P3":
                noOfP3 +=1
            else:
                pass

        for each in listToSort.copy():
            listToSort.remove(each)
            if each.attributes["priority"] == "P1":
                listToSort.insert(0,each)
            elif each.attributes["priority"] == "P2":
                listToSort.insert(noOfP1+1,each)
            elif each.attributes["priority"] == "P3":
                listToSort.insert(noOfP2+noOfP3+1,each)
            else:
                listToSort.insert(len(listToSort)-1,each)


    def placeNewTask(self,taskDict):
        newTask = Task(self.taskFrame,taskDict,self.userPath,self.accent,command=self.taskCompleted,font=self.globalFontName)
        
        if bool(self.taskList) == False:
            self.lblNoTasks.place_forget()
            self.taskList = []

            if self.overdueFrame.winfo_ismapped():
                self.lblOtherTasks.place(in_=self.lblOverdue,y=315)
                self.taskFrame.place(in_=self.lblOtherTasks,y=30)
            else:
                self.lblOtherTasks.place(in_=self.lblListName,x=-5,y=115)
                self.taskFrame.place(in_=self.lblOtherTasks,y=30)
            newTask.grid(row=0,column=0,pady=10)
        else:
            newTask.grid(row=len(self.taskList),column=0,pady=10)

        taskID = newTask.attributes["taskID"]
        self.setDetailsPanel(newTask,taskID)
        self.taskList.append(newTask)

        self.lblOtherTasks.configure(text=f" {self.listName.capitalize()} - {len(self.taskList)}")
    
    def setDetailsPanel(self,task,taskID):
        self.detailPanels[taskID] = DetailsPanel(self,self,self.mainWindow,task,self.userPath,task.attributes,self.taskCompleted,{"taskID":taskID},self.globalFontName,self.accent)
        task.bind("<Button-1>",lambda event,taskID=taskID:self.showDetailsPanel(taskID))
        task.lblTitle.bind("<Button-1>",lambda event,taskID=taskID:self.showDetailsPanel(taskID),
                           )
        task.lblDate.bind("<Button-1>",lambda event,taskID=taskID:self.showDetailsPanel(taskID))

        """# Also sets lblTitle to show accent colour
        task.bind("<Button-1>",lambda event:task.setTitleColour())
        task.bind("<Button-1>",lambda event:task.setTitleColour())"""


    def showDetailsPanel(self,taskID):
        # Window is too small to show details panel.
        if self.winfo_width() < 1505:
            messagebox.showinfo("Can't display details panel.","Increase your window width to\ndisplay the details panel for this task.")
        else:
            # If another details panel is currently being displayed, it is removed from the screen.
            if self.currentDisplayed != "":
                self.detailPanels[self.currentDisplayed].place_forget() # Removes current display panel.

            # Retrieves details panel to be displayed by its taskID
            taskDetailsPanel = self.detailPanels[taskID]
            self.currentDisplayed = taskID

            taskDetailsPanel.place(in_=self.entryTask,y=150)


    def taskCompleted(self,taskID):
        # Retrieving all of the data for the list.
        taskListData = loadTaskList(self.userPath,self.listName)


        # Selecting the tasks part (tasks is a sub-dictionary)
        # (in each list there are two parts, shared and tasks)
        allTasksDict = taskListData["tasks"]


        # Trying to select the completed tasks part
        # (completed is a sub-dictionary of the tasks dict)
        try:
            completedTasksDict = taskListData["completed"]
        except:
            taskListData["completed"] = {}
            completedTasksDict = taskListData["completed"]

        
        # Attempting to find the individual task dictionary for the completed
        # task, searching by its taskID.
        taskDict = ""
        for each in allTasksDict.copy():
            if each == taskID:
            # Dictionary key for each task in allTasksDict is the taskID
                taskDict = allTasksDict[each]
                allTasksDict.pop(each)

        taskDict["completed"] = "True"
        

        # Rewriting the task to the completed section.
        completedTasksDict[taskID] = taskDict


        # Rewriting each of the full list JSON with the amended details.
        # taskListData is the dictionary of the entire list from before.
        taskListData["tasks"] = allTasksDict
        taskListData["completed"] = completedTasksDict


        # Saving the changes by writing them to the JSON file.
        updateTaskListData(taskListData,self.userPath,self.listName)


        # Checking if task is in the overdue section.
        # Then marking it as complete.
        if len(self.overdueDict) != 0:
            if taskID in self.overdueDict:
                for each in self.overdueList.copy():
                    if each.attributes["taskID"] == taskID:
                        each.attributes["completed"] = "True"
            else:
                # Otherwise, marking the task in the regular taskList as complete.
                for each in self.taskList:
                    if each.attributes["taskID"] == taskID:
                        each.attributes["completed"] = "True"

        # Removing the details panel for the completed task.
        self.detailPanels[taskID].place_forget()
        self.detailPanels.pop(taskID)
        self.currentDisplayed = ""

        # Removes the task from the screen and edits text for list title.
        self.removeIfCompleted()

        # Checks other lists to remove completed tasks
        self.mainWindow.updateTasks()

        
    
    def removeIfCompleted(self):
        # First checks if task in regular task list
        for each in self.taskList:
            if each.attributes["completed"] == "True":
                #print(f"Removing {each.attributes["title"]}")

                # Runs placeTasks procedure, passing in index of item and if it is overdue or not.
                self.placeTasks(self.taskList.index(each),overdue=False)

                # Edits list title
                self.lblOtherTasks.configure(text=f" {self.listName.capitalize()} - {len(self.taskList)}")

        # Then checks if it is in overdue list.
        for each in self.overdueList:
            if each.attributes["completed"] == "True":
                #print(f"Removing {each.attributes["title"]}")

                # Same as above except for overdue lists
                self.placeTasks(self.overdueList.index(each),overdue=True)
                self.lblOverdue.configure(text=f"OVERDUE - {len(self.overdueList)}")

        # Removes overdue list frame if there are no more overdue lists.
        if len(self.overdueList) == 0:
            self.lblOverdue.place_forget()
            self.lblOtherTasks.place(in_=self.lblListName,x=-5,y=100)


        # Removes both the regular task frame and the overdue task frame if there are no tasks remaining.
        # Also displays the "You have no tasks" label.
        if len(self.taskList) == 0 and len(self.overdueList) == 0:
            self.taskFrame.place_forget()
            self.lblOtherTasks.place_forget()
            self.overdueFrame.place_forget()
            self.lblOverdue.place_forget()
            self.lblNoTasks.place(x=25,y=150)


    def placeTasks(self,removedIndex,overdue:bool):
        # Removes completed task by index
        # Then places all tasks again after the one which has been removed.


        # Sets which task is being edited.
        if overdue:
            list = self.overdueList
        else:
            list = self.taskList

        # Removes tasks from the completed task to the end of the list.
        for each in range(removedIndex,len(list)):
            list[each].grid_forget()

        # Removes the completed task from the list.
        list.pop(removedIndex)
       

        # Replaces the other previously removed tasks.
        for each in range(removedIndex,len(list)): # Starts with index which was removed
            task = list[each]
            task.grid(row=each,column=0,pady=10)

        if overdue:
            self.lblOverdue.configure(text=f"OVERDUE - {len(self.overdueList)}")
            if len(self.overdueList) == 0:
                self.lblOverdue.place_forget()
                self.lblOtherTasks.place(in_=self.lblListName,x=-5,y=100)
        else:
            self.lblOtherTasks.configure(text=f"{self.listName.capitalize()} - {len(self.taskList)}")
            if len(self.taskList) == 0 and len(self.overdueList)==0:
                self.lblOtherTasks.place_forget()
                self.lblNoTasks.place(x=25,y=150)
            
        
        
    
    def checkNotOverdue(self):
        # Looks through tasks in overdueList to check if they are still overdue.
        todayObj = date.today()

        for each in self.overdueList.copy():
            try:
                taskDateSplit = each.attributes["date"].split("/")
                taskDateObj = date(int(taskDateSplit[-1]),int(taskDateSplit[1]),int(taskDateSplit[0]))
                
                if taskDateObj >= todayObj:
                    # Not overdue, moves to taskFrame
                    self.placeNewTask(each.attributes)
                    self.overdueDict.pop(each.attributes["taskID"])
                    removedIndex = self.overdueList.index(each)
                    self.placeTasks(removedIndex,True)
                    

            except:
                print("Date doesn't exist")

     

    def priorityCallback(self,event):
        if self.dropdownPriority.get() == "priority":
            self.dropdownPriority.configure(text_color="#9e9f9f")
        else:
            self.dropdownPriority.configure(text_color=("black","white"))

    def bindEnterKey(self):
        self.bind("<Return>",lambda event: self.taskSubmitted())
        #print("enter is back")

    def placeAttributeEntries(self):
        # Places submit button
        self.btnTaskSubmit.place(in_=self.entryTask,x=650)

        # Ensures that enter key can be used to submit task
        self.bindEnterKey()

        # Places each entry by using the entries dictionary.
        entries = [self.entryDate,self.entryTime,self.dropdownPriority]
        entries[0].place(in_=self.entryTask,y=50)
        entries[0].bind("<Return>",lambda event:self.taskSubmitted())
        for each in range(1,len(entries)):
            # Each entry is placed to the right of the previous, indicated by each-1
            entries[each].place(in_=entries[each-1],x=150)
            entries[each].bind("<Return>",lambda event:self.taskSubmitted())
    
    def checkTasks(self):
        # Refresh data of tasks.
        # Check if any tasks have been completed and remove if they have

        # Checks for completed tasks in regular list
        if self.taskList != False:
            for each in self.taskList:
                each.refreshData()
                if each.attributes["completed"] == "True":
                    removedIndex = self.taskList.index(each)
                    self.placeTasks(removedIndex,False)

        # Checks for completed tasks in overdue list.
        if self.overdueList != False: 
            for each in self.overdueList:
                each.refreshData()
                if each.attributes["completed"] == "True":
                    self.overdueDict.pop(each.attributes["taskID"])
                    removedIndex = self.overdueList.index(each)
                    self.placeTasks(removedIndex,True)

    def checkNewTasksAdded(self):
        # Checks to see if any new tasks have been added in a different screen.
        # Checks for any new tasks to be added.
        updatedList = getTasks(self.taskFrame,self.userPath,self.listName,
                               self.accent,command=self.taskCompleted,
                               fontName=self.globalFontName,displayListName=False)
        if updatedList != False:
            updatedListTaskIDs = [each.attributes["taskID"] for each in updatedList]
            
            if self.taskList != False:
                for each in self.taskList:
                    if each.attributes["taskID"] in updatedListTaskIDs:
                        updatedListTaskIDs.remove(each.attributes["taskID"])

            if self.overdueList != False:
                for each in self.overdueList:
                    if each.attributes["taskID"] in updatedListTaskIDs:
                        updatedListTaskIDs.remove(each.attributes["taskID"])
            
            for taskID in updatedListTaskIDs:
                # Adds new tasks.
                # The index i matches with the index of the item in updatedList.
                # These items are the ones which are going to be added.
                # Saves the time taken to add all of the tasks again.

                for each in updatedList:
                    if each.attributes["taskID"] == taskID:
                        newTaskDict = each.attributes
                        print(newTaskDict)
                        self.placeNewTask(newTaskDict)
                        break
        
        

    def removeAttributeEntries(self):
        self.btnTaskSubmit.place_forget()
        self.btnTaskSubmit.unbind("<Return>")

        entries = [self.entryDate,self.entryTime,self.dropdownPriority,self.btnTaskSubmit]
        for each in range(0,len(entries)):
            entries[each].place_forget()
            entries[each].unbind("<Return>")
            
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

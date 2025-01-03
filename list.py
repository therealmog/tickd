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


class List(CTkFrame):
    
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
        self.btnTaskSubmit.bind("<Return>",lambda event:self.taskSubmitted())
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
        self.entryTask.place(in_=self.logoPanel,x=-250)

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
        
        self.taskList = getTasks(self.taskFrame,self.userPath,self.listName,self.accent,command=self.taskCompleted,fontName=self.globalFontName)
        
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

            self.orderList(self.taskList)

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

                if len(self.taskList)>0:
                    self.lblOtherTasks.place(in_=self.lblOverdue,y=280)
                    #self.taskFrame.configure(height=500)
                    self.taskFrame.place(in_=self.lblOtherTasks,y=30)
                    
            else:
                if len(self.taskList) >=1:
                    self.lblOtherTasks.place(in_=self.lblListName,x=-5,y=100)
                    self.taskFrame.place(in_=self.lblOtherTasks,y=35)
                else:
                    self.lblNoTasks.place(x=25,y=150)
            
            

        else:
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
        print("yes")
        
        

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
                    
                    # All the attributes are brought together to create a task dictionary
                    # to be written to the task list JSON file.
                    taskDict = createTaskDict(title,date,attributes)
                    self.resetEntry(["entryTask","entryDate","entryTime","dropdownPriority"])

                    # Task is written to the specified list.
                    uploadTask(self.userPath,taskDict,listName=self.listName)


                    
                    # Task is placed onto the screen.
                    self.placeNewTask(taskDict)


                    print([x.attributes["title"] for x in self.taskList])

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

        #print(self.taskList)
        

    """def removeIfCompleted(self):
        for each in self.taskList:
            if each.attributes["completed"] == "True":
                print(f"Removing {each.attributes["title"]}")
                self.placeTasks(self.taskList.index(each))
        
        self.lblOtherTasks.configure(text=f" {self.listName.capitalize()} - {len(self.taskList)}")
        
        if len(self.taskList) == 0 and len(self.overdueList) == 0:
            self.taskFrame.place_forget()
            self.lblOtherTasks.place_forget()
            self.overdueFrame.place_forget()
            self.lblOverdue.place_forget()
            self.lblNoTasks.place(x=25,y=150)


    def placeTasks(self,removedIndex):
        print("hello")
        # Removes completed task by index
        # Then places all tasks again after the one which has been removed.

        
        for each in range(removedIndex,len(self.taskList)):
            self.taskList[each].grid_forget()

        self.taskList.pop(removedIndex)
        

        for each in range(removedIndex,len(self.taskList)): # Starts with index which was removed
            task = self.taskList[each]
            task.grid(row=each,column=0,pady=10)"""
    
    def removeIfCompleted(self):
        # First checks if task in regular task list
        for each in self.taskList:
            if each.attributes["completed"] == "True":
                print(f"Removing {each.attributes["title"]}")

                # Runs placeTasks procedure, passing in index of item and if it is overdue or not.
                self.placeTasks(self.taskList.index(each),overdue=False)

                # Edits list title
                self.lblOtherTasks.configure(text=f" {self.listName.capitalize()} - {len(self.taskList)}")

        # Then checks if it is in overdue list.
        for each in self.overdueList:
            if each.attributes["completed"] == "True":
                print(f"Removing {each.attributes["title"]}")

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

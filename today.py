from customtkinter import *
from datetime import date,timedelta
from lib.getDetails import getAllDetails,getDetailsIndividual,writeToAuthDetails
from lib.submitBtn import SubmitButton
import lib.getWallpaper as getWallpaper
from lib.createTaskDict import createTaskDict
from lib.checkDate import checkDate
from lib.checkTime import checkTime
from lib.task import Task
from lib.loadTaskList import loadTaskList
from lib.getTasks import getTasks
from lib.uploadTask import uploadTask
from lib.updateTaskListData import updateTaskListData
from copy import copy
from lib.detailsPanel import DetailsPanel


from PIL import Image

class Today(CTk):
    
    globalFontName = "Bahnschrift"
    textgrey="#9e9f9f"
    def __init__(self,email,imgBGPath,userPath,theme,listName="inbox"):
        """The class object used to generate the Today view, which is the landing page of the app once the user has logged in.
    
    It should only be declared once in the main function, and then the declared object can be called multiple times."""
        
        
        super().__init__()
        
        self.geometry(f"{self.winfo_screenwidth()}x{self.winfo_screenheight()}")
        self.minsize(750,800)
        
        print(self.winfo_screenwidth(),"by",self.winfo_screenheight())

        self.maxdims = [1920,1080]
        self.maxsize(self.maxdims[0],self.maxdims[1])
        self.title("Today - Tickd")

        self.darkImgBGPath = imgBGPath[0]
        self.lightImgBGPath = imgBGPath[1]
        self.userPath = userPath
        self.theme = theme
        self.listName = listName
        
        self.userDetails,self.userIndex = getDetailsIndividual(email)
        try:
            self.userName = self.userDetails[2]
        except TypeError:
            print("Invalid email entered. Have you registered?")

        self.today = date.today()
        self.todaysDate = self.today.strftime("%A, %d %B %Y")
        print(self.todaysDate)

        if theme == "dark":
            set_appearance_mode("Dark")
        else:
            set_appearance_mode("Light")
        self.accent = "dodgerblue2"
        #self.bind("<Configure>",lambda event:self.mode())
        

        #deactivate_automatic_dpi_awareness()

        self.elements = {
            
        } 

        self.widgets()
        self.placeWidgets()

        self.entriesDict = {
            "entryTask":self.entryTask,
            "entryDate":self.entryDate,
            "entryTime":self.entryTime,
            "dropdownPriority":self.dropdownPriority
        }



        self.bind("<Return>",lambda event:self.checkEnteredUsername())
        self.checkUserName()

        self.loadTasks()

        self.bind("<Configure>",lambda event:self.resizeFrame())
        self.mainloop()

    #------------------------# Widgets and placing #-------------------------#    
    def widgets(self):
        globalFontName = self.globalFontName

        self.darkImgBG = getWallpaper.getFromPath(self.darkImgBGPath,(self.maxdims[0],self.maxdims[1]))
        self.lightImgBG = getWallpaper.getFromPath(self.lightImgBGPath,(self.maxdims[0],self.maxdims[1]))
        if self.theme == "dark":
            self.panelImgBG = CTkLabel(self,text="",image=self.darkImgBG)
        else:
            self.panelImgBG = CTkLabel(self,text="",image=self.lightImgBG)
        
        frameX,frameY = self.frameDimensions()
        self.frameToday = CTkFrame(self,width=frameX,height=frameY,fg_color=("white","gray9"),border_color="gray7",border_width=5,corner_radius=20)

        self.lblDate = CTkLabel(self.frameToday,text=self.todaysDate,font=(globalFontName,30))
        
        self.textVar = StringVar()
        self.textVar.set(f"Welcome, {self.userName}!")
        self.lblWelcome = CTkLabel(self.frameToday,textvariable=self.textVar,font=(globalFontName,18))
        self.imgLogo = CTkImage(light_image=Image.open("logo//whiteBGLogo.png"),dark_image=Image.open("logo//blackBGLogo.png"),size=(155,49)) 
        self.logoPanel = CTkLabel(self.frameToday,text="",image=self.imgLogo)
        self.entryTask = CTkEntry(self.frameToday,placeholder_text="Enter a task...",font=(globalFontName,30),width=550,corner_radius=20)
        
        
        self.messageVar = StringVar()
        self.lblMessage = CTkLabel(self.frameToday,textvariable=self.messageVar,font=(globalFontName,25))

        self.lblEnterUsername = CTkLabel(self.frameToday,text="Please enter your new username:",font=(globalFontName,22))
        self.entryUserName = CTkEntry(self.frameToday,placeholder_text="",font=(globalFontName,22),width=330)
        self.btnSubmitUsername = SubmitButton(parent=self.frameToday,command=self.checkEnteredUsername,colour=self.accent,buttonSize=(30,30),radius=70)

        self.entryDate = CTkEntry(self.frameToday,placeholder_text="date",font=(globalFontName,22),corner_radius=20,border_width=0)
        self.entryTime = CTkEntry(self.frameToday,placeholder_text="time",font=(globalFontName,22),corner_radius=20,border_width=0)
        self.dropdownPriority = CTkOptionMenu(self.frameToday,values=["priority","P1","P2","P3"],font=(globalFontName,22),dropdown_font=(globalFontName,20),corner_radius=20,fg_color=("#f9f9fa","#353639"),button_color=("#f9f9fa","#353639"),text_color=self.textgrey,command=self.priorityCallback)
        self.btnTaskSubmit = SubmitButton(self.frameToday,colour=self.accent,buttonSize=(35,35),command=self.taskSubmitted,radius=60)
        
        self.lblNoTasks = CTkLabel(self.frameToday,text="You have no tasks.",font=(globalFontName,40))

        """self.sampleDetailsPanel = DetailsPanel(self.frameToday,{"title": "Welcome!", "date": "16/10/2024", "taskID": "TjAiDX", "completed": "False", "time": "", "priority": "", "description": ""},
                                               self.taskCompleted,{"taskID":"TjAiDX"})"""
        self.entries = [self.entryDate,self.dropdownPriority,self.entryTime]

    def placeWidgets(self):
        self.frameToday.place(relx=0.5,rely=0.5,anchor="center")
        self.panelImgBG.place(x=0,y=0)
        
        self.lblDate.place(x=25,y=50)
        self.lblWelcome.place(in_=self.lblDate,x=0,y=-30)
        self.logoPanel.place(relx=0.98,y=40,anchor=E)
        self.entryTask.place(in_=self.lblDate,x=450,y=-20)

        #self.sampleDetailsPanel.place(in_=self.entryTask,x=50,y=100)

        self.currentAttribute = ""

    def frameDimensions(self):
        frameX = 0.68 * self.winfo_screenwidth()
        frameY = 0.68 * self.winfo_screenheight()

        return frameX, frameY
        
    def resizeFrame(self):
        #print(self.winfo_width(),"by",self.winfo_height())
        frameX = 0.78 * self.winfo_width()
        frameY = 0.78 * self.winfo_height()

        self.frameToday.configure(width=frameX,height=frameY)
        #self.panelImgBG._image

        if self.winfo_width() < 1505:
            self.entryTask.place_forget()
        
        if self.winfo_width() > 1505:
            self.entryTask.place(in_=self.logoPanel,x=-650,y=10)

    def loadTasks(self): # Should only be run at the start of the program
        """try:
            for each in self.taskList:
                each.place_forget()
        except:
            pass"""
        
        self.taskList = getTasks(self.frameToday,self.userPath,"inbox",self.accent,command=self.taskCompleted,fontName=self.globalFontName)
        
        self.detailPanels = {} # taskID:detailPanelObj
        self.currentDisplayed = "" # stores taskID of task with details panel displayed.


        if self.taskList != False:
            self.lblNoTasks.place_forget()
            self.taskList[0].place(x=25,y=200)
            
            taskID = self.taskList[0].attributes["taskID"]
            self.setDetailsPanel(self.taskList[0],taskID)

            for each in range(1,len(self.taskList)): # Starts with second item
                task = self.taskList[each]
                task.place(in_=self.taskList[each-1],y=75)
                
                taskID = task.attributes["taskID"]
                self.setDetailsPanel(task,taskID)

        else:
            self.lblNoTasks.place(x=25,y=150)
    
            
        

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
        title = self.entryTask.get()
        attributes = {}

        if title == "":
            self.lblMessage.place(in_=self.entryTask,x=5,y=85)
            self.messageVar.set("Please enter a task title before submitting.")
        else: # Start to interpret attributes
            dateInput = self.entryDate.get()
            if dateInput == "":
                date = ""
            else:
                date,message = checkDate(userInput=dateInput)

            if date == False:
                self.messageVar.set(message)
            else:
                attributes["date"] = date

                timeInput = self.entryTime.get()
                if timeInput == "":
                    time = ""
                else:
                    time,message = checkTime(userInput=timeInput)

                if time == False:
                    self.messageVar.set(message)
                else:
                    attributes["time"] = time                
                
                    if self.dropdownPriority.get() != "priority":
                        attributes["priority"] = self.dropdownPriority.get()
                    else:
                        attributes["priority"] = ""
                    
                    attributes["description"] = ""
                    attributes["listName"] = self.listName
                    
                    taskDict = createTaskDict(title,date,attributes)
                    self.resetEntry(["entryTask","entryDate","entryTime","dropdownPriority"])

                    
                    uploadTask(self.userPath,taskDict,listName="inbox")
                    self.placeNewTask(taskDict)

                    print([x.attributes["title"] for x in self.taskList])

    def placeNewTask(self,taskDict):
        newTask = Task(self.frameToday,taskDict,self.accent,command=self.taskCompleted,font=self.globalFontName)
        
        if bool(self.taskList) == False:
            self.lblNoTasks.place_forget()
            self.taskList = []
            newTask.place(x=25,y=200)
        else:
            newTask.place(in_=self.taskList[-1],y=75)

        taskID = newTask.attributes["taskID"]
        self.setDetailsPanel(newTask,taskID)
        self.taskList.append(newTask)
    
    def setDetailsPanel(self,task,taskID):
        self.detailPanels[taskID] = DetailsPanel(self.frameToday,self.userPath,task.attributes,self.taskCompleted,{"taskID":taskID},self.globalFontName,self.accent)
        task.bind("<Button-1>",lambda event,taskID=taskID:self.showDetailsPanel(taskID))

    def showDetailsPanel(self,taskID):
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
        
                
    
        for each in allTasksDict.copy():
            if each == taskID: # Dictionary key for each task in allTasksDict is the taskID
                taskDict = allTasksDict[each]
                allTasksDict.pop(each)

        taskDict["completed"] = "True"

        completedTasksDict[taskID] = taskDict

        taskListData["tasks"] = allTasksDict
        taskListData["completed"] = completedTasksDict

        updateTaskListData(taskListData,self.userPath,"inbox")


        

        #uploadTask(self.userPath,taskDict,listName="inbox")
        
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
            each.place_forget()
            if each.attributes["completed"] == "True":
                self.taskList.remove(each)
        
        if len(self.taskList) == 0:
            self.lblNoTasks.place(in_=self.lblDate,y=150)
        else:
            print(self.taskList)
            self.placeTasks()

    def placeTasks(self):
        print("hello")
        self.taskList[0].place_forget()
        self.taskList[0].place(x=25,y=200)
        if len(self.taskList)>1:
            for i in range(1,len(self.taskList)):
                self.taskList[i].place(in_=self.taskList[i-1],y=75)

        """try:
            for each in self.taskList:
                each.place_forget()
            
            
        except IndexError:
            print("list is empty!")"""
        
        


    def taskEntryClickedWhileDisabled(self,reason):
        self.messageVar.set(reason)
        self.lblMessage.place(in_=self.entryTask,x=5,y=85)
        self.frameToday.after(3000,self.lblMessage.place_forget)


    def priorityCallback(self,event):
        if self.dropdownPriority.get() == "priority":
            self.dropdownPriority.configure(text_color="#9e9f9f")
        else:
            self.dropdownPriority.configure(text_color=("black","white"))


    def placeAttributeEntries(self):
        self.btnTaskSubmit.place(in_=self.entryTask,x=555)
        self.btnTaskSubmit.bind("<Return>",self.taskSubmitted)

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
        self.messageVar.set("")
            
    def resetEntry(self,entries:list):
        entriesDict = self.entriesDict
        for each in entries:
            if "dropdown" in each:
                valuesList = entriesDict[each]._values 
                entriesDict[each].set(valuesList[0])
                entriesDict[each].configure(text_color=self.textgrey)
            else:
                entriesDict[each].delete(0,"end")

         


    def clickablesOnOff(self):
        clickables = []
        elements = self.elements
        for each in elements:
            if "entry" in each or "btn" in each:
                clickables.append(elements[each])
        
        for clickable in clickables:
            if clickable.cget("state") == "normal":
                clickable.configure(state="disabled")
            else:
                clickable.configure(state="normal")

    def bindTaskEntry(self):
        self.entryTask.bind("<FocusIn>",lambda event:self.taskEntryEnter())
        self.entryTask.bind("<FocusOut>",lambda event:self.attributeLeave())
        
        for each in self.entries:
            each.bind("<FocusIn>",lambda event:self.attributeEntered())
            each.bind("<FocusOut>",lambda event:self.attributeLeave())


    #-----------------------------# Username stuff #--------------------------------#    
    def checkEnteredUsername(self):
        print("hello")
        userInput = self.entryUserName.get()
        self.lblMessage.place(in_=self.entryTask,x=5,y=85)
        if userInput.strip()=="":
            self.messageVar.set("Please enter a username.")
        elif len(userInput) > 20 or len(userInput) < 3:
            self.messageVar.set("Please ensure that username is 3-20 characters long.")
        elif " " in userInput.strip():
            self.messageVar.set("Please ensure that there are no spaces in your username.")
        else:
            self.userDetails[2] = userInput
            details,rememberMeIndex = getAllDetails()
            details[self.userIndex] = self.userDetails
            authDetails = {"details":details,"rememberMe":rememberMeIndex}

            writeToAuthDetails(authDetails)
            self.textVar.set(f"Welcome, {self.userDetails[2]}!")
            self.messageVar.set("Success!")


            self.entryTask.configure(state="normal")
            self.btnTaskSubmit.configure(state="normal")
            self.entryTask.unbind("<Button-1>")
            self.bind("<Return>",lambda event:self.taskSubmitted())
            
            self.lblEnterUsername.place_forget()
            self.entryUserName.place_forget()
            self.btnSubmitUsername.place_forget()

            # Adding 'welcome' task

            welcomeTaskDict = {"title":"Welcome to Tickd!",
                               "date":f"{date.today().strftime('%d/%m/%Y')}",
                               "description":"Welcome to a simpler life with Tickd.\nSimply add tasks with the 'Add a task' box at the top, and use keywords such as 'today' and 'tomorrow' in the date, or for other dates simply add the date using the DD/MM/YY format.\ne.g. for the 31st December 2025, you would put 31/12/25.",
                               "completed":"False",
                               "taskID":"welcome"}
            uploadTask(self.userPath,welcomeTaskDict,"inbox")
            self.loadTasks()

    def checkUserName(self):
        if self.userName == "":
            print("You haven't got a username!")
            self.entryTask.bind("<Button-1>",lambda event,reason="Please enter your username before entering in a task.":self.taskEntryClickedWhileDisabled(reason))
            self.entryTask.configure(state="disabled")
            self.btnTaskSubmit.configure(state="disabled")
            self.lblEnterUsername.place(in_=self.lblWelcome,y=60)
            self.entryUserName.place(in_=self.lblEnterUsername,x=0,y=35)
            self.btnSubmitUsername.place(in_=self.entryUserName,x=340,y=-3)
            self.bindTaskEntry()
        else:
            self.unbind("<Return>")
            self.bind("<Return>",lambda event:self.taskSubmitted())
            self.bindTaskEntry()
    
    
    
     


today = Today(email="omar@gmail.com",imgBGPath=["wallpapers//dark1.png","wallpapers//light1.png"],userPath="users//omar@gmail.com",theme="dark",listName="inbox")

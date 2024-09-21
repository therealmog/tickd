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


from PIL import Image

class Today(CTk):
    
    globalFontName = "Bahnschrift"
    textgrey="#9e9f9f"
    def __init__(self,email,imgBGPath,userPath):
        """The class object used to generate the Today view, which is the landing page of the app once the user has logged in.
    
    It should only be declared once in the main function, and then the declared object can be called multiple times."""
        
        
        super().__init__()
        
        self.geometry("1600x900")
        #self.minsize(1600,900)
        

        self.maxdims = [1920,1080]
        self.maxsize(self.maxdims[0],self.maxdims[1])
        self.title("Today - Tickd")

        self.imgBGPath = imgBGPath
        self.userPath = userPath
        
        self.userDetails,self.userIndex = getDetailsIndividual(email)
        try:
            self.userName = self.userDetails[2]
        except TypeError:
            print("Invalid email entered. Have you registered?")

        self.today = date.today()
        self.todaysDate = self.today.strftime("%A, %d %B %Y")
        print(self.todaysDate)

        set_appearance_mode("Dark")
        self.accent = "dodgerblue2"
        #self.bind("<Configure>",lambda event:self.mode())
        

        deactivate_automatic_dpi_awareness()

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
        self.mainloop()

    #------------------------# Widgets and placing #-------------------------#    
    def widgets(self):
        globalFontName = self.globalFontName

        self.imgBG = getWallpaper.getFromPath(self.imgBGPath,(self.maxdims[0],self.maxdims[1]))
        self.panelImgBG = CTkLabel(self,text="",image=self.imgBG)
        self.frameToday = CTkFrame(self,width=1400,height=800,fg_color=("white","gray9"),border_color="gray7",border_width=5,corner_radius=20)

        self.lblDate = CTkLabel(self.frameToday,text=self.todaysDate,font=(globalFontName,30))
        
        self.textVar = StringVar()
        self.textVar.set(f"Welcome, {self.userName}!")
        self.lblWelcome = CTkLabel(self.frameToday,textvariable=self.textVar,font=(globalFontName,20))
        self.imgLogo = CTkImage(light_image=Image.open("logo//whiteBGLogo.png"),dark_image=Image.open("logo//blackBGLogo.png"),size=(165,53)) 
        self.logoPanel = CTkLabel(self.frameToday,text="",image=self.imgLogo)
        self.entryTask = CTkEntry(self.frameToday,placeholder_text="Enter a task...",font=(globalFontName,30),width=650,corner_radius=20)
        
        
        self.messageVar = StringVar()
        self.lblMessage = CTkLabel(self.frameToday,textvariable=self.messageVar,font=(globalFontName,25))

        self.lblEnterUsername = CTkLabel(self.frameToday,text="Please enter your new username:",font=(globalFontName,22))
        self.entryUserName = CTkEntry(self.frameToday,placeholder_text="",font=(globalFontName,22),width=330)
        self.btnSubmitUsername = SubmitButton(parent=self.frameToday,command=self.checkEnteredUsername,colour=self.accent,buttonSize=(30,30),radius=70)

        self.entryDate = CTkEntry(self.frameToday,placeholder_text="date",font=(globalFontName,22),corner_radius=20,border_width=0)
        self.entryTime = CTkEntry(self.frameToday,placeholder_text="time",font=(globalFontName,22),corner_radius=20,border_width=0)
        self.dropdownPriority = CTkOptionMenu(self.frameToday,values=["priority","P1","P2","P3"],font=(globalFontName,22),dropdown_font=(globalFontName,20),corner_radius=20,fg_color="#353639",button_color="#353639",text_color=self.textgrey,command=self.priorityCallback)
        self.btnTaskSubmit = SubmitButton(self.frameToday,colour=self.accent,buttonSize=(35,35),command=self.taskSubmitted,radius=60)
        
        self.lblNoTasks = CTkLabel(self.frameToday,text="You have no tasks.",font=(globalFontName,40))

        self.entries = [self.entryDate,self.dropdownPriority,self.entryTime]

    def placeWidgets(self):
        self.frameToday.place(relx=0.5,rely=0.5,anchor="center")
        self.panelImgBG.place(x=0,y=0)
        
        self.lblDate.place(x=25,y=25)
        self.lblWelcome.place(in_=self.lblDate,x=0,y=40)
        self.logoPanel.place(relx=0.87,y=20)
        self.entryTask.place(in_=self.lblDate,x=450,y=10)

        self.currentAttribute = ""

    def removeIfCompleted(self):
        for each in self.taskList:
            each.place_forget()
            if each.attributes["completed"] == "True":
                self.taskList.remove(each)
        
        if len(self.taskList) != 0:
            self.taskList[0].place(in_=self.lblWelcome,y=150)
            for each in range(1,len(self.taskList)): # Starts with second item
                self.taskList[each].place(in_=self.taskList[each-1],y=75)
        else:
            self.lblNoTasks.place(in_=self.lblWelcome,y=150)
        

    def loadTasks(self):
        self.taskList = getTasks(self.frameToday,self.userPath,"inbox",self.accent,command=self.taskCompleted)
        
        if self.taskList != False:
            self.lblNoTasks.place_forget()
            self.taskList[0].place(in_=self.lblWelcome,y=150)
            for each in range(1,len(self.taskList)): # Starts with second item
                self.taskList[each].place(in_=self.taskList[each-1],y=75)
        else:
            self.lblNoTasks.place(in_=self.lblWelcome,y=150)
    
            
        

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
                    

                    taskDict = createTaskDict(title,date,attributes)
                    self.resetEntry(["entryTask","entryDate","entryTime","dropdownPriority"])

                    uploadTask(self.userPath,taskDict,listName="inbox")
                    
                    self.loadTasks()

    def taskCompleted(self,taskID):
        taskList = loadTaskList(self.userPath,"inbox")
        allTasksDict = taskList["tasks"]
        
    
        for each in allTasksDict:
            if each == taskID: # Dictionary key for each task in allTasksDict is the taskID
                taskDict = allTasksDict[each]

        taskDict["completed"] = "True"
        

        for each in self.taskList:
            if each.attributes["taskID"] == taskID:
                each.attributes["completed"] = "True"

        uploadTask(self.userPath,taskDict,listName="inbox")
        self.removeIfCompleted()




    def taskEntryClickedWhileDisabled(self,reason):
        self.messageVar.set(reason)
        self.lblMessage.place(in_=self.entryTask,x=5,y=85)
        self.frameToday.after(3000,self.lblMessage.place_forget)


    def priorityCallback(self,event):
        if self.dropdownPriority.get() == "priority":
            self.dropdownPriority.configure(text_color="#9e9f9f")
        else:
            self.dropdownPriority.configure(text_color="white")


    def placeAttributeEntries(self):
        self.btnTaskSubmit.place(in_=self.entryTask,x=655)
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
    
    
    
     


today = Today(email="amoghg75@yahoo.com",imgBGPath="wallpapers//wallpaper1.png",userPath="users//amoghg75@yahoo.com")

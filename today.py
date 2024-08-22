from customtkinter import *
from datetime import date,timedelta
from lib.getDetails import getAllDetails,getDetailsIndividual,writeToAuthDetails
from lib.submitBtn import SubmitButton
import lib.getWallpaper as getWallpaper
from lib.createTaskDict import createTaskDict
from task import Task


from PIL import Image

class Today(CTk):
    
    globalFontName = "Bahnschrift"
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


        self.checkUserName()
        self.bind("<Return>",lambda event:self.checkEnteredUsername())
        self.mainloop()

    #------------------------# Widgets and placing #-------------------------#    
    def widgets(self):
        globalFontName = self.globalFontName

        self.imgBG = getWallpaper.getFromPath(self.imgBGPath,(self.maxdims[0],self.maxdims[1]))
        self.panelImgBG = CTkLabel(self,text="",image=self.imgBG)
        self.frameToday = CTkFrame(self,width=1400,height=800,border_color="gray7",border_width=5,corner_radius=20)

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

        self.entryDate = CTkEntry(self.frameToday,placeholder_text="date",font=(globalFontName,20),corner_radius=20)
        self.entryTime = CTkEntry(self.frameToday,placeholder_text="time",font=(globalFontName,20),corner_radius=20)
        self.entryPriority = CTkEntry(self.frameToday,placeholder_text="priority",font=(globalFontName,20),corner_radius=20)
        self.btnTaskSubmit = SubmitButton(self.frameToday,colour=self.accent,buttonSize=(35,35),command=self.taskSubmitted,radius=60)

        self.myTask = Task(self.frameToday,{"title":""},size=30)
        self.entries = [self.entryDate,self.entryPriority,self.entryTime]

    def placeWidgets(self):
        self.frameToday.place(relx=0.5,rely=0.5,anchor="center")
        self.panelImgBG.place(x=0,y=0)
        
        self.lblDate.place(x=25,y=25)
        self.lblWelcome.place(in_=self.lblDate,x=0,y=40)
        self.logoPanel.place(relx=0.87,y=20)
        self.entryTask.place(in_=self.lblDate,x=400,y=10)

        self.myTask.place(in_=self.lblWelcome,y=150)

        self.currentAttribute = ""

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
            if each.get() != "":
                filled = True
        if filled == False:
            self.removeAttributeEntries()

    
    def taskSubmitted(self):
        title = self.entryTask.get()
        
        if title == "":
            self.lblMessage.place(in_=self.entryTask,x=5,y=85)
            self.messageVar.set("Please enter a task title before submitting.")
        else:
            self.messageVar.set("")
            taskDict = createTaskDict(self.entryTask.get())
            print(taskDict)
        
    
        self.checkDate()

    def checkDate(self):
        userInput = self.entryDate.get().lower()

        if userInput == "today":
            date = self.today.strftime("%d/%m/%Y")
            return date
        elif userInput == "tomorrow":
            tomorrow = self.today + timedelta(days=1)
            date = tomorrow.strftime("%d/%m/%Y")
        else:
            try:
                dateSections = userInput.split("/")
            except:
                self.messageVar.set("Invalid date entered")
                return False
            
            day = dateSections[0]
            month = dateSections[1]
            year = dateSections[2]

            # Checking year #
            if len(year)<=2:
                if steyear<24:
                    self.messageVar("Your date cannot be in the past.")
                    return False
                else:
                    year = "20"+year
            elif len(year)==3:
                self.messageVar.set("Invalid year.")
                return False
            else:
                if year <2024:
                    self.messageVar.set("Your date cannot be in the past.")
                    return False
            
            # Checking day #
            if day>31:
                self.messageVar.set("Invalid date")
                return False
            elif day>28 and month != "2":
                self.messageVar.set("Invalid date")
                return False
            else:




    def taskEntryClickedWhileDisabled(self,reason):
        self.messageVar.set(reason)
        self.lblMessage.place(in_=self.entryTask,x=5,y=85)
        self.frameToday.after(3000,self.lblMessage.place_forget)
    
    def checkEntry(self):
        print("checking")
        if len(self.entryTask.get()) >0:
            self.placeAttributeEntries()
        else:
            self.removeAttributeEntries()

    def placeAttributeEntries(self):
        print("placing")
        self.btnTaskSubmit.place(in_=self.entryTask,x=655)
        self.btnTaskSubmit.bind("<Return>",self.taskSubmitted)

        entries = [self.entryDate,self.entryTime,self.entryPriority]
        entries[0].place(in_=self.entryTask,y=50)
        for each in range(1,len(entries)):
            entries[each].place(in_=entries[each-1],x=150)
    
    def removeAttributeEntries(self):
        print("removing")
        self.btnTaskSubmit.place_forget()
        self.btnTaskSubmit.unbind("<Return>")

        entries = [self.entryDate,self.entryTime,self.entryPriority,self.btnTaskSubmit]
        for each in range(0,len(entries)):
            entries[each].place_forget()
            
        
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
            self.bind("<Return>",lambda event:self.taskSubmitted())
            self.bindTaskEntry()
    
    
    
     


today = Today(email="amoghg75@yahoo.com",imgBGPath="wallpapers//wallpaper1.png",userPath="users//amoghg75@yahoo.com")

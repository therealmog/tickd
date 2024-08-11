from customtkinter import *
from datetime import date
from getDetails import getAllDetails,getDetailsIndividual,writeToAuthDetails
from lib.submitBtn import SubmitButton
import lib.getWallpaper as getWallpaper


from PIL import Image

class Today(CTk):
    globalFontName = "Bahnschrift"
    def __init__(self,email,imgBGPath):
        super().__init__()
        
        self.geometry("1600x900")
        self.minsize(1600,900)

        self.maxdims = [1920,1080]
        self.maxsize(self.maxdims[0],self.maxdims[1])
        self.title("Today - Tickd")

        self.imgBGPath = imgBGPath
        
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
        self.mainloop()


    def mode(self):
        print(f"{self.winfo_width()},{self.winfo_height()}")
    
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
        self.btnSubmitUsername = SubmitButton(parent=self.frameToday,command=self.checkEnteredUsername,colour=self.accent,buttonSize=(30,30))
        #self.btnSubmitUsername.bind("<Button-1>",lambda event:self.checkEnteredUsername())

    def placeWidgets(self):
        self.frameToday.place(relx=0.5,rely=0.5,anchor="center")
        self.panelImgBG.place(x=0,y=0)
        
        self.lblDate.place(x=25,y=25)
        self.lblWelcome.place(in_=self.lblDate,x=0,y=40)
        self.logoPanel.place(relx=0.87,y=20)
        self.entryTask.place(in_=self.lblDate,x=400,y=10)
        
    def taskEntryClickedWhileDisabled(self,reason):
        self.messageVar.set(reason)
        self.lblMessage.place(in_=self.entryTask,x=5,y=85)
        self.frameToday.after(3000,self.lblMessage.place_forget)
    
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

            
            self.lblEnterUsername.place_forget()
            self.entryUserName.place_forget()
            self.btnSubmitUsername.place_forget()

    def checkUserName(self):
        if self.userName == "":
            print("You haven't got a username!")
            self.entryTask.bind("<Button-1>",lambda event,reason="Please enter your username before entering in a task.":self.taskEntryClickedWhileDisabled(reason))
            self.entryTask.configure(state="disabled")
            self.lblEnterUsername.place(in_=self.lblWelcome,y=60)
            self.entryUserName.place(in_=self.lblEnterUsername,x=0,y=35)
            self.btnSubmitUsername.place(in_=self.entryUserName,x=340,y=-3)
    
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


#today = Today(email="omar@gmail.com")

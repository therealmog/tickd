from customtkinter import *
from datetime import date,timedelta
from lib.getDetails import getAllDetails,getDetailsIndividual,writeToAuthDetails
from lib.submitBtn import SubmitButton
from lib.detailsPanel import DetailsPanel
from lib.getListImgs import getListImgs


from PIL import Image

class MyLists(CTkFrame):
    
    globalFontName = "Bahnschrift"
    textgrey="#9e9f9f"
    def __init__(self,mainWindow,email,userPath,todaysDate,userAccent="dodgerblue2"):
        """The 'My lists' frame class."""
        
        
        super().__init__(mainWindow,width=1400,height=900,fg_color=("white","gray9"),border_color="gray7",border_width=5,corner_radius=20)
        
        self.mainWindow = mainWindow
        self.mainWindow.title("My lists - Tickd")

        self.userPath = userPath
        self.listName = "My lists"
        self.email = email

        """self.today = date.today()
        self.todaysDate = self.today.strftime("%A, %d %B %Y")
        print(self.todaysDate)"""


        self.accent = userAccent
        self.userName = getDetailsIndividual(self.email)

        self.elements = {
            
        } 

        

        self.widgets()
        self.placeWidgets()
        self.topButtonCallback("ownedByMe")


        #self.bind("<Configure>",lambda event:self.resizeFrame())

    #------------------------# Widgets and placing #-------------------------#    
    def widgets(self):
        globalFontName = self.globalFontName
       
        print("Bonjour.")
        self.lblListName = CTkLabel(self,text="My lists",font=(globalFontName,50))
        
        self.textVar = StringVar()
        self.textVar.set(f"Welcome, {self.userName}!")
        self.imgLogo = CTkImage(light_image=Image.open("logo//whiteBGLogo.png"),dark_image=Image.open("logo//blackBGLogo.png"),size=(155,49)) 
        self.logoPanel = CTkLabel(self,text="",image=self.imgLogo)
        
        
        self.btnOwnedByMe = CTkButton(self,text="Owned by me",font=(globalFontName,35),command=lambda btn="ownedByMe":self.topButtonCallback(btn),fg_color="grey",hover=False,border_width=5,border_color="grey5",corner_radius=60)
        self.btnSharedWithMe = CTkButton(self,text="Shared with me",font=(globalFontName,35),command=lambda btn="sharedWithMe":self.topButtonCallback(btn),fg_color="grey",hover=False,border_width=5,border_color="grey5",corner_radius=60)

        #---------# System lists #---------#
        self.imgLogoDefaultLists = CTkImage(light_image=Image.open("logo//whiteBGLogo.png"),dark_image=Image.open("logo//blackBGLogo.png"),size=(114,36))
        self.lblDefaultLists = CTkLabel(self,text="default lists",font=(globalFontName,30),image=self.imgLogoDefaultLists,compound="left")

        self.listImgs = getListImgs((36,36))
        self.btnInbox = CTkButton(self,text="Inbox",font=(globalFontName,40),width=280,fg_color="grey28",hover_color="grey24",border_width=5,border_color="grey5",corner_radius=60,image=self.listImgs["Inbox"],compound="left",cursor="hand2")
        self.btnToday = CTkButton(self,text="Today",font=(globalFontName,40),width=280,fg_color="grey28",hover_color="grey24",border_width=5,border_color="grey5",corner_radius=60,image=self.listImgs["Today"],compound="left",cursor="hand2")
        self.btnStarred = CTkButton(self,text="Starred",font=(globalFontName,40),width=280,fg_color="grey28",hover_color="grey24",border_width=5,border_color="grey5",corner_radius=60,image=self.listImgs["Starred"],compound="left",cursor="hand2")

        self.tickdDefaults = [self.btnToday,self.btnInbox,self.btnStarred]

        self.lblYourCustomLists = CTkLabel(self,text="Your custom lists",font=(globalFontName,30))
        self.lblYourSharedLists = CTkLabel(self,text="Your shared lists",font=(globalFontName,30))

    def placeWidgets(self):
        #self.place(relx=0.5,rely=0.5,anchor="center")
        #self.panelImgBG.place(x=0,y=0)
        
        self.lblListName.place(x=125,y=30)
        #self.lblDate.place(in_=self.lblListName,x=0,y=-25)
        self.logoPanel.place(relx=0.98,y=40,anchor=E)

        self.btnOwnedByMe.place(in_=self.lblListName,x=300)
        self.btnSharedWithMe.place(in_=self.btnOwnedByMe,x=260)

        #self.sampleDetailsPanel.place(in_=self.entryTask,x=50,y=100)

        self.lblDefaultLists.place(in_=self.lblListName,y=150)
        self.lblYourCustomLists.place(in_=self.lblDefaultLists,x=450)
        self.lblYourSharedLists.place(in_=self.lblYourCustomLists,x=450)
        
        self.tickdDefaults[0].place(in_=self.lblDefaultLists,y=50)
        for each in range(1,len(self.tickdDefaults)):
            self.tickdDefaults[each].place(in_=self.tickdDefaults[each-1],y=70)

        

        self.currentAttribute = ""

    def frameDimensions(self):
        print(f"Width: {self.winfo_screenwidth()}, Height: {self.winfo_screenheight()}")
        frameX = 0.68 * self.winfo_screenwidth()
        frameY = 0.68 * self.winfo_screenheight()

        return frameX, frameY
    
    def topButtonCallback(self,btn):
        if btn == "ownedByMe":
            self.btnOwnedByMe.configure(fg_color=self.accent)
            self.btnSharedWithMe.configure(fg_color="grey")
        else:
            self.btnSharedWithMe.configure(fg_color=self.accent)
            self.btnOwnedByMe.configure(fg_color="grey")

    """def resizeFrame(self):
        screenWidth = self.winfo_screenwidth()
        screenHeight = self.winfo_screenheight()
        
        #print(self.winfo_width(),"by",self.winfo_height())
        frameX = 0.95 * self.winfo_width()
        frameY = 0.95 * self.winfo_height()

        self.configure(width=frameX,height=frameY)
        #self.panelImgBG._image
        
        
        if self.winfo_width() < 1505:
            self.entryTask.place_forget()

        if self.winfo_width() > 1505:
            self.entryTask.place(in_=self.logoPanel,x=-650,y=10)"""
          
    def renameMainWin(self):
        self.mainWindow.title("My lists - Tickd")

    #--------------------# Task entry and button functions #------------------#
    def taskEntryEnter(self):
        self.placeAttributeEntries()   
        #self.entryTask.unbind("<Key>")

    def bindEnterKey(self):
        self.bind("<Return>",lambda event: self.taskSubmitted)
        print("enter is back")
    
    
     

#today = Today(mainWindow=None,email="omar@gmail.com",userPath="users//omar@gmail.com",theme="dark",listName="inbox")
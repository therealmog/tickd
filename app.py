from customtkinter import *
from datetime import date,timedelta
from lib.getDetails import getAllDetails,getDetailsIndividual,writeToAuthDetails
from lib.uploadTask import uploadTask
from lib.menuAndButton import MenuAndButton
from today import Today
from myLists import MyLists
from lib.accentsConfig import getAccent
from lib.menu import Menu


from PIL import Image

class App(CTk):
    
    globalFontName = "Bahnschrift"
    textgrey="#9e9f9f"
    def __init__(self,email,userPath):
        """Main app container for Tickd."""

        super().__init__()
        
        
        #self.attributes("-topmost",True)
        
        self.geometry(f"{self.winfo_screenwidth()}x{self.winfo_screenheight()}")
        self.minsize(750,800)
        
        set_appearance_mode("dark")
        print(self.winfo_screenwidth(),"by",self.winfo_screenheight())

        self.maxdims = [2000,1100]
        self.maxsize(self.maxdims[0],self.maxdims[1])
        self.title("Tickd")
        
        self.iconbitmap("logo//tickd.ico")

        self.today = date.today()
        self.todaysDate = self.today.strftime("%A, %d %B %Y")
        print(self.todaysDate)

        self.userEmail = email
        self.userPath = userPath
        
        self.userDetails,self.userIndex = getDetailsIndividual(email)
        try:
            self.userName = self.userDetails[2]
        except TypeError:
            print("Invalid email entered. Have you registered?")

        self.accent = getAccent(email)

        if self.accent == False:
            print("User not found in preferences file. Setting colour to default.")
            self.accent = "dodgerblue2"
        
       
        """self.attributes("-fullscreen",True)
        self.after(500,lambda option="-fullscreen",val=False:self.attributes(option,val))"""

        self.widgets()
        self.placeWidgets()

        # Add in frames for different app functions here.
        self.menu = MenuAndButton(self.currentFrame,{"Inbox":lambda msg="hello there":print(msg),
                                          "Today":lambda:self.loadFrame("today"),
                                          "My lists":lambda:self.loadFrame("myLists"),
                                          "Starred":"asdasdasd",
                                          "Leaderboard":"asdasd"},origin=self,userName=self.userName)
        self.menu.place(x=20,y=30)

        
        self.loadFrame("today")
        #self.bindTaskEntry()

        self.bind("<Configure>",lambda event:self.resizeFrame())

        
        
        
        self.mainloop()

    #------------------------# Widgets and placing #-------------------------#    
    def widgets(self):
        globalFontName = self.globalFontName
        
        frameX,frameY = self.frameDimensions()
        self.dummyFrame = CTkFrame(self,width=frameX,height=frameY,fg_color=("white","gray9"),border_color="gray7",border_width=5,corner_radius=20)
        self.currentFrame = self.dummyFrame

        self.imgLogo = CTkImage(light_image=Image.open("logo//whiteBGLogo.png"),dark_image=Image.open("logo//blackBGLogo.png"),size=(155,49))
        self.logoPanel = CTkLabel(self.currentFrame,text="",image=self.imgLogo,cursor="hand2")
        
        self.lblNoTasks = CTkLabel(self.currentFrame,text="Load a content frame.",font=(globalFontName,40))

        """self.sampleDetailsPanel = DetailsPanel(self.currentFrame,{"title": "Welcome!", "date": "16/10/2024", "taskID": "TjAiDX", "completed": "False", "time": "", "priority": "", "description": ""},
                                               self.taskCompleted,{"taskID":"TjAiDX"})"""
        #6self.entries = [self.entryDate,self.dropdownPriority,self.entryTime]

        self.taskFrame = CTkScrollableFrame(self.currentFrame,width=410,height=600,fg_color="#191616")

        #-----------------# Regular app frames #------------------#
        self.frameToday = Today(self,email=self.userEmail,userPath=self.userPath,todaysDate=self.todaysDate,userAccent=self.accent,listName="inbox")
        self.frameMyLists = MyLists(self,email=self.userEmail,userPath=self.userPath,todaysDate=self.todaysDate,userAccent=self.accent)

        self.frames = {"today":self.frameToday,
                       "myLists":self.frameMyLists,
                       "starred":self.dummyFrame,
                       "leaderboard":self.dummyFrame,
                       "inbox":self.dummyFrame}
        
        self.preferencesMenuDict = {"Theme":lambda:self.mode(),
                                    "Accent colour":lambda msg="hello":print(msg)}
        self.preferencesMenu = Menu(self,self.preferencesMenuDict,self.accent,topLabel="",bottomLabel="Your preferences.")
        
        self.logoMenuIsOpen = False

            
        
        
        

    def placeWidgets(self):
        self.currentFrame.place(relx=0.5,rely=0.5,anchor="center")
        #self.panelImgBG.place(x=0,y=0)
        
        self.logoPanel.place(relx=0.98,y=40,anchor=E)
        self.lblNoTasks.place(relx=0.4,rely=0.4)

        #self.sampleDetailsPanel.place(in_=self.entryTask,x=50,y=100)

        self.currentAttribute = ""

    def mode(self):
        if get_appearance_mode().lower() == "light":
            set_appearance_mode("dark")
        else:
            set_appearance_mode("light")

    def frameDimensions(self):
        print(f"Width: {self.winfo_screenwidth()}, Height: {self.winfo_screenheight()}")
        frameX = 0.68 * self.winfo_screenwidth()
        frameY = 0.68 * self.winfo_screenheight()

        return frameX, frameY
    
    def logoClicked(self):
        if not self.logoMenuIsOpen:
            self.preferencesMenu.place(in_=self.logoPanel,x=-80,y=60)
            self.logoMenuIsOpen = True
        else:
            self.preferencesMenu.place_forget()
            self.logoMenuIsOpen = False


    def resizeFrame(self):
        try:
            screenWidth = self.winfo_screenwidth()
            screenHeight = self.winfo_screenheight()

            """if not self.winfo_ismapped():
                pass"""
            
            #print(self.winfo_width(),"by",self.winfo_height())
            """if self.winfo_width > 1560:"""
            frameX = 0.95 * self.winfo_width()
            frameY = 0.95 * self.winfo_height()
            """else:
                frameX = 0.80 * self.winfo_width()
                frameY = 0.5 * self.winfo_height()"""

            self.currentFrame.configure(width=frameX,height=frameY)
            #self.panelImgBG._image
            
            
            if self.winfo_width() < 1505:
                if self.currentFrame == self.frames["today"]:
                    self.currentFrame.entryTask.place_forget()
                    self.currentFrame.taskFrame.configure(height=self.winfo_height()*0.7)

            if self.winfo_width() > 1505:
                if self.currentFrame == self.frames["today"]:
                    self.currentFrame.entryTask.place(in_=self.currentFrame.logoPanel,x=-750,y=10)
                    self.currentFrame.taskFrame.configure(height=self.winfo_height()*0.7)
        except:
            pass
        
    
    def loadFrame(self,frameName):
        self.currentFrame.place_forget()
        self.currentFrame = self.frames[frameName]

        self.currentFrame.place(relx=0.5,rely=0.5,anchor="center")

        """if self.currentFrame == self.frames["today"]:
            self.resizeFrame = self.currentFrame.resizeFrame"""
        try:
            self.menu = MenuAndButton(self.currentFrame,{"Inbox":lambda:self.loadFrame("inbox"),
                                          "Today":lambda:self.loadFrame("today"),
                                          "My lists":lambda:self.loadFrame("myLists"),
                                          "Starred":lambda:self.loadFrame("starred"),
                                          "Leaderboard":lambda:self.loadFrame("leaderboard")},origin=self,userName=self.userName,accent=self.accent)
            
            self.logoPanel = CTkLabel(self.currentFrame,text="",image=self.imgLogo,cursor="hand2")

            self.preferencesMenu = self.preferencesMenu
            self.logoPanel.bind("<Button-1>",lambda event:self.logoClicked())
                        
            self.menu.place(x=20,y=30)
            self.logoPanel.place(relx=0.98,y=40,anchor=E)
            
        except:
            pass

        try:
            self.currentFrame.renameMainWin()
        except:
            pass
        #self.bind("<Configure>",lambda event: self.currentFrame.resizeFrame())


    
    
    
    
     


app = App(email="omar@gmail.com",userPath="users//omar@gmail.com")

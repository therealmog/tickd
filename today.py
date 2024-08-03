from customtkinter import *
from datetime import date
from getDetails import getDetails,getDetailsIndividual

from PIL import Image

class Today(CTk):
    globalFontName = "Bahnschrift"
    def __init__(self,email):
        super().__init__()
        
        self.geometry("1600x900")
        self.minsize(1600,900)
        self.maxsize(1920,1080)
        self.title("Today - Tickd")

        self.userDetails = getDetailsIndividual(email)

        self.userName = self.userDetails[2]

        self.today = date.today()
        self.todaysDate = self.today.strftime("%A, %d %B %Y")
        print(self.todaysDate)

        set_appearance_mode("Dark")
        #self.bind("<Configure>",lambda event:self.mode())
        

        deactivate_automatic_dpi_awareness()

        self.widgets()
        self.placeWidgets()

        self.checkUserName()
        self.mainloop()


    def mode(self):
        print(f"{self.winfo_width()},{self.winfo_height()}")
    
    def widgets(self):
        globalFontName = self.globalFontName

        
        self.imgBG = CTkImage(Image.open("wavy.jpg"),size=(1920,1080))
        self.panelImgBG = CTkLabel(self,text="",image=self.imgBG)
        self.frameToday = CTkFrame(self,width=1400,height=800,border_color="gray7",border_width=5,corner_radius=20)

        self.lblDate = CTkLabel(self.frameToday,text=self.todaysDate,font=(globalFontName,30))
        
        self.textVar = f"Welcome, {self.userName}!"
        self.lblWelcome = CTkLabel(self.frameToday,text=self.textVar,font=(globalFontName,20))
        self.logo = CTkImage(light_image=Image.open("logo//whiteBGLogo.png"),dark_image=Image.open("logo//blackBGLogo.png"),size=(165,53)) 
        self.logoPanel = CTkLabel(self.frameToday,text="",image=self.logo)
        self.taskEntry = CTkEntry(self.frameToday,placeholder_text="Enter a task...",font=(globalFontName,30),width=650,corner_radius=20)
        
    
    def placeWidgets(self):
        self.frameToday.place(relx=0.5,rely=0.5,anchor="center")
        self.panelImgBG.place(x=0,y=0)
        
        self.lblDate.place(x=25,y=25)
        self.lblWelcome.place(in_=self.lblDate,x=0,y=40)
        self.logoPanel.place(relx=0.87,y=20)
        self.taskEntry.place(in_=self.lblDate,x=400,y=10)
        
    
    def checkUserName(self):
        if self.userName == "":
            pass


today = Today(email="amoghng")

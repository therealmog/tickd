from customtkinter import *
from PIL import Image
from lib import getWallpaper
import authcustomTk

class Register(CTk):
    def __init__(self,imgBGPath=None):
        super().__init__()
        self.geometry("650x800")
        self.maxdims = [650,800]
        self.imagedims = [1280,1080]
        self.maxsize(self.maxdims[0],self.maxdims[1])
        self.title("Register - Tickd")

        set_appearance_mode("dark")


        self.imgBGPath = imgBGPath

        self.widgets()
        self.placeWidgets()

        
        

        self.mainloop()

    def widgets(self):
        globalFontName = "Bahnschrift"
        emojiFont = ("Segoe UI Emoji",30)

        if self.imgBGPath == None:
            self.imgBG,_ = getWallpaper.getRandom((self.imagedims[0],self.imagedims[1]))
        else:
            self.imgBG = getWallpaper.getFromPath(self.imgBGPath,(self.imagedims[0],self.imagedims[1]))
        self.panelImgBG = CTkLabel(self,text="",image=self.imgBG)

        self.frameRegister = CTkFrame(self,width=550,height=700,fg_color=("white","gray9"),border_color="gray7",border_width=5,corner_radius=20)
        self.logoImg = CTkImage(dark_image=Image.open("logo//blackBGLogo.png"),light_image=Image.open("logo//whiteBGLogo.png"),size=(140,45))
        self.panelLogo = CTkLabel(self.frameRegister,text="",image=self.logoImg)
        self.registerLbl = CTkLabel(self.frameRegister,font=(globalFontName,35),text="register.")

        self.entryEmail = CTkEntry(self.frameRegister,font=(globalFontName,25),width=400,placeholder_text="email",corner_radius=15)
        self.entryPassword = CTkEntry(self.frameRegister,font=(globalFontName,25),width=400,placeholder_text="password",show="*",corner_radius=15)
        self.lblEmail = CTkLabel(self.frameRegister,font=emojiFont,text="✉️")
        self.lblPassword = CTkLabel(self.frameRegister,font=emojiFont,text="🔒")
        self.entryUsername = CTkEntry(self.frameRegister,font=(globalFontName,25),width=400,placeholder_text="username",corner_radius=15)
        self.lblUsername = CTkLabel(self.frameRegister,font=emojiFont,text="🧑")

    def placeWidgets(self):
        self.panelImgBG.place(x=0,y=0)
        self.frameRegister.place(relx=0.5,rely=0.5,anchor="center")
        self.panelLogo.place(relx=0.7,y=20)
        self.registerLbl.place(x=220,y=45)

        self.entryEmail.place(x=100,y=150)
        self.lblEmail.place(in_=self.entryEmail,x=-50,y=-3)
        self.entryPassword.place(in_=self.entryEmail,y=70)
        self.lblPassword.place(in_=self.entryPassword,x=-50,y=-3)
        self.entryUsername.place(in_=self.entryPassword,y=70)
        self.lblUsername.place(in_=self.entryUsername,x=-50,y=-3)
        

register = Register()
        
        

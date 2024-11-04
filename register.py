from customtkinter import *
from PIL import Image
from lib import getWallpaper
from lib.getDetails import getAllDetails
import json
from lib.createUserFolder import createUserFolder
from random import choice
from datetime import date
from lib.uploadTask import uploadTask
from lib.genHash import genHash


class Register(CTkToplevel):
    # This class doesn't have an __init__ function, to allow it to be stored in the Auth window.
    def initialise(self,imgBGPath=None,accent="dodgerblue2",origin=None):
        super().__init__()
        self.geometry("650x600")
        self.maxdims = [650,600]
        self.imagedims = [1280,1080]
        self.minsize(self.maxdims[0],self.maxdims[1])
        self.maxsize(self.maxdims[0],self.maxdims[1])
        self.title("Register - Tickd")
        
        self.origin = origin
        # This is to access the attributes of the Auth window class.

        self.protocol("WM_DELETE_WINDOW",lambda:self.close_window())

        set_appearance_mode("dark")


        self.imgBGPath = imgBGPath
        self.accent = accent

        
        self.widgets()
        self.placeWidgets()

        """
        """
        self.grab_set()
        self.lift()
        self.after(1000,lambda: self.grab_release())

        

        self.elements = {"entryEmail":self.entryEmail,
                         "entryPassword":self.entryPassword,
                         "entryUsername":self.entryUsername}
        

        self.mainloop()

    def close_window(self):
        self.origin.registerWinOpen = False
        self.destroy()

    def widgets(self):
        globalFontName = "Bahnschrift"
        emojiFont = ("Segoe UI Emoji",30)

        if self.imgBGPath == None:
            self.imgBG,_ = getWallpaper.getRandom((self.imagedims[0],self.imagedims[1]))
        else:
            self.imgBG = getWallpaper.getFromPath(self.imgBGPath,(self.imagedims[0],self.imagedims[1]))
        self.panelImgBG = CTkLabel(self,text="",image=self.imgBG)

        self.frameRegister = CTkFrame(self,width=575,height=500,fg_color=("white","gray9"),border_color="gray7",border_width=5,corner_radius=20)
        self.logoImg = CTkImage(dark_image=Image.open("logo//blackBGLogo.png"),light_image=Image.open("logo//whiteBGLogo.png"),size=(140,45))
        self.panelLogo = CTkLabel(self.frameRegister,text="",image=self.logoImg)
        self.registerLbl = CTkLabel(self.frameRegister,font=(globalFontName,35),text="Create your account.")

        self.entryEmail = CTkEntry(self.frameRegister,font=(globalFontName,25),width=400,placeholder_text="email",corner_radius=15)
        self.entryPassword = CTkEntry(self.frameRegister,font=(globalFontName,25),width=400,placeholder_text="password",show="*",corner_radius=15)
        self.lblEmail = CTkLabel(self.frameRegister,font=emojiFont,text="✉️")
        self.lblPassword = CTkLabel(self.frameRegister,font=emojiFont,text="🔒")
        self.entryUsername = CTkEntry(self.frameRegister,font=(globalFontName,25),width=400,placeholder_text="username",corner_radius=15)
        self.lblUsername = CTkLabel(self.frameRegister,font=emojiFont,text="🧑")

        self.imgShowPassword = CTkImage(Image.open("eyeIcon.png"),size=(33,24))
        self.btnShowPassword = CTkButton(self.frameRegister,image=self.imgShowPassword,text="",width=1,command=self.showHide,corner_radius=15,fg_color=self.accent)
        self.imgHidePassword = CTkImage(Image.open("eyeIconOff.png"),size=(33,24))
        self.btnHidePassword = CTkButton(self.frameRegister,image=self.imgHidePassword,text="",width=0,command=self.showHide,corner_radius=15,fg_color=self.accent)

        self.btnRegister = CTkButton(self.frameRegister,text="register",font=(globalFontName,30),corner_radius=15,text_color="white",border_color=("black","gray12"),fg_color=self.accent,border_width=2,command=self.registerClicked)
        self.messageVar = StringVar()
        self.messageVar.set("hello")
        self.lblMessage = CTkLabel(self.frameRegister,textvariable=self.messageVar,font=(globalFontName,25))

        self.btnCancel = CTkButton(self.frameRegister,text="cancel",font=(globalFontName,30),corner_radius=15,hover_color="red",text_color="white",border_color=("black","gray12"),fg_color=self.accent,border_width=2,command=self.close_window)

    def placeWidgets(self):
        self.panelImgBG.place(x=0,y=0)
        self.frameRegister.place(relx=0.5,rely=0.5,anchor="center")
        self.panelLogo.place(relx=0.35,y=20)
        self.registerLbl.place(in_=self.panelLogo,x=-85,y=45)

        self.entryEmail.place(x=95,y=150)
        self.lblEmail.place(in_=self.entryEmail,x=-50,y=-3)
        self.entryPassword.place(in_=self.entryEmail,y=70)
        self.lblPassword.place(in_=self.entryPassword,x=-50,y=-3)
        self.entryUsername.place(in_=self.entryPassword,y=70)
        self.lblUsername.place(in_=self.entryUsername,x=-50,y=-3)

        self.btnShowPassword.place(in_=self.entryPassword,x=405,y=2)
        self.btnRegister.place(in_=self.entryUsername,x=45,y=100)
        self.btnCancel.place(in_=self.btnRegister,x=145)

        self.setMessage("hello!!","limegreen")
        
    def createSampleTask(self):
        welcomeTaskDict = {"title":"Welcome to Tickd!",
                               "date":f"{date.today().strftime('%d/%m/%Y')}",
                               "description":"Welcome to a simpler life with Tickd.\nSimply add tasks with the 'Add a task' box at the top, and use keywords such as 'today' and 'tomorrow' in the date, or for other dates simply add the date using the DD/MM/YY format.\ne.g. for the 31st December 2025, you would put 31/12/25.",
                               "completed":"False",
                               "time":"",
                               "priority":"",
                               "taskID":"welcome"}
        uploadTask(self.userPath,welcomeTaskDict,"inbox")
    
    def showHide(self):
        if self.btnShowPassword.winfo_ismapped():
            self.btnShowPassword.place_forget()
            self.btnHidePassword.place(in_=self.entryPassword,x=405,y=2)
            self.entryPassword.configure(show="")
        else:
            self.btnHidePassword.place_forget()
            self.btnShowPassword.place(in_=self.entryPassword,x=405,y=2)
            self.entryPassword.configure(show="*")
    
    def grabWin(self):
        self.grab_set()
        self.lift()
        self.after(1000,lambda: self.grab_release())

    def registerClicked(self):
        print("Hello")

        email = self.entryEmail.get()
        password = self.entryPassword.get()
        username = self.entryUsername.get()
        
        details,rememberMeIndex = getAllDetails()
        
        emailEmpty, passwordEmpty,usernameEmpty = self.checkEmpty(email, password,username)
        emailValid = self.checkEmail(email)
        found,self.userDetails = self.checkDetailsFound(email,details)
        

        if emailEmpty == False and passwordEmpty == False and usernameEmpty == False:
            if emailValid and found:
                self.setMessage("An account already exists with this email.","red")
                self.resetEntry(["entryEmail"])
            elif not emailValid:
                self.setMessage("Please enter a valid email.","red")
                self.entryEmail.focus_set()
                self.resetEntry(["entryEmail"])
            else:
                passwordToStore = genHash(password)
                newDetails = [email,passwordToStore,username]

                
                details.append(newDetails)
                newAuthDetails = {"details":details,"rememberMe":rememberMeIndex}

                print(newAuthDetails)
                
                with open("authDetails.json","w") as f:
                    json.dump(newAuthDetails,f,indent=4)
                
                self.resetEntry(["entryEmail","entryPassword"])
                self.userPath = f"users//{email}"
                createUserFolder(self.userPath) # Creates new folder for the new user with one "inbox.json" list
                self.createSampleTask()
                self.setMessage("Account successfully created. Please log in.","limegreen")
                self.origin.registerWinOpen = False
                self.after(2000,self.destroy)
        


    #-------# Entry validation funcs #-------#

    def checkDetailsFound(self,email,details):
        found = False
        for each in details:
            if each[0] == email:
                userDetails = each
                found = True
        if found == False:
            print("No details found.")
            userDetails = []

        return found, userDetails
    
    def checkEmpty(self,email,password,username):
        emailEmpty = False
        passwordEmpty = False
        usernameEmpty = False

        email = email.strip()
        username = username.strip()
        
        print(f"{email}, {password},{username}")
        fields = {"email":email,"password":password,"username":username}
        fieldsVars = {"email":emailEmpty,"password":passwordEmpty,"username":usernameEmpty}
        for each in fields:
            print(each)
            if fields[each] == "":
                print("empty")
                fieldsVars[each] = True
                self.setMessage(f"Please fill out all fields.","red")
        emailEmpty = fieldsVars["email"]
        passwordEmpty = fieldsVars["password"]
        usernameEmpty = fieldsVars["username"]
        print(f"{fieldsVars['email']} {passwordEmpty} {usernameEmpty}")
        
        return emailEmpty, passwordEmpty,usernameEmpty

    def checkEmail(self,email):
        if "@" in email:
            splitEmail = email.split("@")
            if "." in splitEmail[1]:
                return True
            else:
                return False
        else:
            self.setMessage("Invalid email entered.","red")
            return False
    
    def setMessage(self,message,colour = "white"):
        length = len(message)
        lblMessage = self.lblMessage
        lblUsername = self.lblUsername

        lblMessage.place(in_=lblUsername,x=25,y=60)
        
        if colour == "black" or colour == "white":
            colour = ("black","white")
        
        lblMessage.configure(text_color=colour)
        self.messageVar.set(message)
    
    def resetEntry(self,entries:list):
        elements = self.elements
        for each in entries:
            element = elements[each]
            element.delete(0,END)
        
        self.lblEmail.focus_set()

    
    

#register = Register()
        
        

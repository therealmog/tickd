from customtkinter import *
from PIL import Image
from lib import getWallpaper
from lib.getDetails import getAllDetails
import json
import smtplib,ssl
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

class ResetPassword(CTkToplevel):
    def __init__(self,imgBGPath=None,accent="dodgerblue2",origin=None):
        super().__init__()
        self.geometry("650x400")
        self.maxdims = [650,400]
        self.imagedims = [1280,1080]
        self.minsize(self.maxdims[0],self.maxdims[1])
        self.maxsize(self.maxdims[0],self.maxdims[1])
        self.title("Reset your password - Tickd")
        
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
                         "entryPassword":self.entryPassword}
        
        
        

        self.mainloop()

    def close_window(self):
        self.origin.registerWinOpen = False
        self.destroy()

    def widgets(self):
        globalFontName = "Bahnschrift"
        emojiFont = ("Segoe UI Emoji",30)

        if self.imgBGPath == None:
            self.darkImgBG,self.lightImgBG,_,_ = getWallpaper.getRandom((self.imagedims[0],self.imagedims[1]))
        else:
            self.imgBG = getWallpaper.getFromPath(self.imgBGPath,(self.imagedims[0],self.imagedims[1]))
        self.panelImgBG = CTkLabel(self,text="",image=self.darkImgBG)

        self.frameRegister = CTkFrame(self,width=575,height=350,fg_color=("white","gray9"),border_color="gray7",border_width=5,corner_radius=20)
        self.logoImg = CTkImage(dark_image=Image.open("logo//blackBGLogo.png"),light_image=Image.open("logo//whiteBGLogo.png"),size=(140,45))
        self.panelLogo = CTkLabel(self.frameRegister,text="",image=self.logoImg)
        self.registerLbl = CTkLabel(self.frameRegister,font=(globalFontName,35),text="Reset your password.")

        self.entryEmail = CTkEntry(self.frameRegister,font=(globalFontName,25),width=375,placeholder_text="email",corner_radius=15)
        self.entryPassword = CTkEntry(self.frameRegister,font=(globalFontName,25),width=400,placeholder_text="password",show="*",corner_radius=15)
        self.lblEmail = CTkLabel(self.frameRegister,font=emojiFont,text="✉️")
        self.lblPassword = CTkLabel(self.frameRegister,font=emojiFont,text="🔒")

        self.btnVerify = CTkButton(self.frameRegister,text="verify",width=60,corner_radius=15,fg_color=self.accent,font=(globalFontName,25),command=self.checkEmailFormat)

        #self.btnRegister = CTkButton(self.frameRegister,text="register",font=(globalFontName,30),corner_radius=15,text_color="white",border_color=("black","gray12"),fg_color=self.accent,border_width=2,command=self.registerClicked)
        self.messageVar = StringVar()
        self.messageVar.set("hello")
        self.lblMessage = CTkLabel(self.frameRegister,textvariable=self.messageVar,font=(globalFontName,25))

        #self.btnCancel = CTkButton(self.frameRegister,text="cancel",font=(globalFontName,30),corner_radius=15,hover_color="red",text_color="white",border_color=("black","gray12"),fg_color=self.accent,border_width=2,command=self.close_window)

    def placeWidgets(self):
        self.panelImgBG.place(x=0,y=0)
        self.frameRegister.place(relx=0.5,rely=0.5,anchor="center")
        self.panelLogo.place(relx=0.35,y=20)
        self.registerLbl.place(in_=self.panelLogo,x=-85,y=45)

        self.entryEmail.place(x=95,y=150)
        self.lblEmail.place(in_=self.entryEmail,x=-50,y=-3)
        """self.entryPassword.place(in_=self.entryEmail,y=70)
        self.lblPassword.place(in_=self.entryPassword,x=-50,y=-3)"""

        self.btnVerify.place(in_=self.entryEmail,x=380)
        #self.btnRegister.place(in_=self.entryEmail,x=45,y=100)
        #self.btnCancel.place(in_=self.btnRegister,x=145)

        self.setMessage("Please enter your email to receive a \n6-digit code.","white")
        
    def sendEmail(self,receiverEmail):
        context = ssl.create_default_context()
        tickdEmail = "tickd.todolist@gmail.com"
        message = MIMEMultipart()
        message["From"] = "Tickd. <tickd.todolist@gmail.com>"
        message["To"] = receiverEmail
        message["Subject"] = "Your Tickd security code."
        msgText = f"<html><body><img src='https://tickd-todo.s3.eu-west-2.amazonaws.com/blackBGLogo.png' width=300><h2>Your security code.</h2><p>Someone or you tried to reset your Tickd password.<br><br>Your security code is</p><h2>{self.code}</h2><br><br><p>Thanks,</p><h3>The Tickd security team.</h3></body></html>"
        msgObj = MIMEText(msgText,"html")
        message.attach(msgObj)

        with smtplib.SMTP_SSL("smtp.gmail.com",465,context=context) as server:
            server.login(tickdEmail,"daxn vysr plkb blnv")
            server.sendmail(tickdEmail,receiverEmail,message.as_string())
            print("Message sent!")
        

    
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
                newDetails = [email,password,username]

                
                details.append(newDetails)
                newAuthDetails = {"details":details,"rememberMe":rememberMeIndex}

                print(newAuthDetails)
                
                with open("authDetails.json","w") as f:
                    f.write(json.dumps(newAuthDetails))
                
                self.resetEntry(["entryEmail","entryPassword"])
                createUserFolder(userPath=f"users//{email}") # Creates new folder for the new user with one "inbox.json" list
                self.setMessage("Account successfully created. Please log in.","limegreen")
        


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

    def checkEmailFormat(self):
        email = self.entryEmail.get()
        if "@" in email:
            splitEmail = email.split("@")
            if "." in splitEmail[1]:
                emailRegistered = self.checkEmailRegistered(email)

                if emailRegistered:
                    self.setMessage("Email registered.","limegreen")
                else:
                    self.setMessage("Email not registered.","red")
            else:
                self.setMessage("Invalid email entered.","red")
        else:
            self.setMessage("Invalid email entered.","red")
            return False
    
    def checkEmailRegistered(self,emailToCheck):
        details,_ = getAllDetails()
        for detailSet in details:
            if detailSet[0] == emailToCheck:
                return True
        return False

    
    def setMessage(self,message,colour = "white"):
        length = len(message)
        lblMessage = self.lblMessage

        lblMessage.place(in_=self.lblEmail,x=40,y=60)
        
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

register = ResetPassword()
        
        

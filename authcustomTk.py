# Amogh NG
# Auth screen with customtkinter

from customtkinter import *
from PIL import ImageTk, Image
import json
from checkbox_customTk import Checkbox
from getDetails import getAllDetails
from getWallpaper import getRandom as getWallpaper



class Auth(CTk):
    globalFontName = "Bahnschrift"
    buttonFont = (globalFontName,25)
    emojiFont = ("Segoe UI Emoji",30)
    globalColour = ("black","white")
    accent = "dodgerblue2"

    def __init__(self):
        super().__init__()

        self.dimensions = [950,670]
        self.maxdimensions = [1280,800]

        maxdims = self.maxdimensions 
        x=self.dimensions[0]
        y=self.dimensions[1]
        self.geometry(f"{x}x{y}")
        self.minsize(x,y)
        self.maxsize(maxdims[0],maxdims[1])
        self.title("Log in - Tickd")

        self.loggedIn = False

        self.widgets()
        self.placeWidgets()
        self.checkRememberMe()

        self.bind("<Return>",lambda event:self.signInClicked())

        print(self.btnRegister.cget("state"))
        
        
        self.mainloop()

        

    def widgets(self):
        globalFontName = self.globalFontName
        emojiFont = self.emojiFont
        buttonFont = self.buttonFont

        self.imgBG,self.imgBGPath = getWallpaper((self.maxdimensions[0],self.maxdimensions[1]))
        self.panelImgBG = CTkLabel(self,text="",image=self.imgBG)
        self.frameLogin = CTkFrame(self,width=850,height=570,corner_radius=20,border_color="gray7",border_width=5,fg_color=None)
        

        self.imgMode = CTkImage(light_image=Image.open("logo//moon.png"),dark_image=Image.open("logo//sun.png"),size=(40,40))
        self.btnMode = CTkButton(self.frameLogin,image=self.imgMode,text="",command=self.changeMode,width=1,fg_color="#252425",hover_color=self.accent,corner_radius=50)
        
        self.logo = CTkImage(light_image=Image.open("logo//whiteBGLogo.png"),dark_image=Image.open("logo//blackBGLogo.png"),size=(330,105)) 
        self.logoPanel = CTkLabel(self.frameLogin,text="",image=self.logo)
        
        
        self.entryEmail = CTkEntry(self.frameLogin,font=(globalFontName,25),width=400,placeholder_text="email",corner_radius=15)
        self.entryPassword = CTkEntry(self.frameLogin,font=(globalFontName,25),width=400,placeholder_text="password",show="*",corner_radius=15)
        self.lblEmail = CTkLabel(self.frameLogin,font=emojiFont,text="✉️")
        self.lblPassword = CTkLabel(self.frameLogin,font=emojiFont,text="🔒")
        
        self.imgShowPassword = CTkImage(Image.open("eyeIcon.png"),size=(30,30))
        self.btnShowPassword = CTkButton(self.frameLogin,image=self.imgShowPassword,text="",width=1,command=self.showHide,corner_radius=15,fg_color=self.accent)
        self.imgHidePassword = CTkImage(Image.open("eyeIconOff.png"),size=(30,30))
        self.btnHidePassword = CTkButton(self.frameLogin,image=self.imgHidePassword,text="",width=1,command=self.showHide,corner_radius=15)
        self.btnRegister = CTkButton(self.frameLogin,text="register",font=buttonFont,corner_radius=15,text_color=self.globalColour,border_color=("black","gray12"),fg_color=self.accent,border_width=2,command=self.registerClicked)
        self.btnSignIn = CTkButton(self.frameLogin,text="sign in",font=buttonFont,corner_radius=15,command=self.signInClicked,text_color=self.globalColour,border_color=("black","gray12"),fg_color=self.accent,border_width=2)
        self.btnConfirm = CTkButton(self.frameLogin,text="confirm",font=buttonFont,corner_radius=15,command=self.signInClicked,text_color=self.globalColour,border_color=("black","gray12"),fg_color=self.accent,border_width=2)
        self.btnDeny = CTkButton(self.frameLogin,text="deny",font=buttonFont,corner_radius=15,command=self.rememberMeDeniedClicked,text_color=self.globalColour,border_color=("black","gray12"),fg_color=self.accent,border_width=2)
        self.checkboxRememberMe = Checkbox(self.frameLogin,x=0,y=50,size=(35,35),relWidget=self.entryPassword)
        self.messageVar = StringVar()
        self.lblMessage = CTkLabel(self.frameLogin,font=(globalFontName,30),textvariable=self.messageVar)
        

        self.lblRememberMe = CTkLabel(self.frameLogin,text="Remember me",font=(globalFontName,25),text_color=self.globalColour,cursor="hand2")
        self.lblRememberMe.bind("<Button-1>",lambda event: self.checkboxRememberMe.boxClicked(event))


        self.elements = {
            "lblEmail":self.lblEmail,
            "lblPassword":self.lblPassword,
            "entryEmail":self.entryEmail,
            "entryPassword":self.entryPassword,
            "btnRegister":self.btnRegister,
            "btnSignIn":self.btnSignIn,
            "btnShowPassword":self.btnShowPassword,
            "btnHidePassword":self.btnHidePassword,
            }
        #self.bindingEventListeners()
        

    def placeWidgets(self):
        self.panelImgBG.place(x=0,y=0)
        self.frameLogin.place(relx=0.5,rely=0.5,anchor="center")
        self.logoPanel.place(relx=0.3,rely=0.1)
        self.btnMode.place(x=770,y=15)
        self.entryEmail.place(in_=self.logoPanel,x=-25,y=150)
        self.entryPassword.place(in_=self.entryEmail,y=50)
        self.lblEmail.place(in_=self.entryEmail,x=-50,y=-5)
        self.lblPassword.place(in_=self.entryPassword,x=-50,y=-5)
        self.btnShowPassword.place(in_=self.entryPassword,x=410)
        self.btnRegister.place(in_=self.entryPassword,x=50,y=100)
        self.btnSignIn.place(in_=self.btnRegister,x=150)
        self.checkboxRememberMe.placeWidget()
        self.lblRememberMe.place(in_=self.entryPassword,x=40,y=52)
        
    def changeMode(self):
        if get_appearance_mode() == "Light":
            set_appearance_mode("Dark")
            self.btnMode.configure(fg_color="#252425")
            self.globalColour = "white"
        else:
            set_appearance_mode("Light")
            self.btnMode.configure(fg_color="#eaeaeb")
            self.globalColour = "black"
    

    def showHide(self):
        if self.btnShowPassword.winfo_ismapped():
            self.btnShowPassword.place_forget()
            self.btnHidePassword.place(in_=self.entryPassword,x=410)
            self.entryPassword.configure(show="")
        else:
            self.btnHidePassword.place_forget()
            self.btnShowPassword.place(in_=self.entryPassword,x=410)
            self.entryPassword.configure(show="*")


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
    
    def checkEmpty(self,email,password):
        emailEmpty = False
        passwordEmpty = False

        email = email.strip()

        if email == "" and password == "":
            emailEmpty = True
            passwordEmpty = True
        elif email == "":
            self.setMessage("Please enter your email.",self.globalColour)
            emailEmpty = True
        elif password == "":
            passwordEmpty = True
        
        return emailEmpty, passwordEmpty

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

    def setMessage(self,message,colour):
        length = len(message)
        lblMessage = self.lblMessage
        btnRegister = self.btnRegister

        print(repr(message))
        
        increment=0 # Used to increase the distance the widget is placed to the right. Used for larger messages.
        if length>=45 and not "\n" in message:
            increment=20
        elif length > 45:
            increment = 150
        elif length>35:
            increment = 50 
        
        fontSize = 30
        x=150+increment-(7*length)
        lblMessage.place(in_=btnRegister,x=x,y=70)
        
        if colour == "black" or colour == "white":
            colour = ("black","white")
        
        lblMessage.configure(font=(self.globalFontName,fontSize),text_color=colour)
        self.messageVar.set(message)

    def resetEntry(self,entries:list):
        elements = self.elements
        for each in entries:
            element = elements[each]
            element.delete(0,END)
        
        self.lblEmail.focus_set()


    def signInClicked(self):
        print("Hello")
        self.btnConfirm.place_forget()

        email = self.entryEmail.get()
        password = self.entryPassword.get()
        
        details,_ = getAllDetails()
        
        emailEmpty, passwordEmpty = self.checkEmpty(email, password)
        emailValid = self.checkEmail(email)
        found,self.userDetails = self.checkDetailsFound(email,details)
        

        if emailEmpty and passwordEmpty:
            self.setMessage("Please enter your details.",self.globalColour)
        elif emailEmpty:
            self.setMessage("Please enter your email.",self.globalColour)
            self.resetEntry(["entryPassword"])
        elif passwordEmpty:
            self.setMessage("Please enter your password.",self.globalColour)
        else:
            if emailValid and not found:
                self.setMessage("Details not found.\nPlease click 'register' to make a new account.","red")
            elif not emailValid:
                self.setMessage("Please enter a valid email.",self.globalColour)
                self.resetEntry(["entryPassword","entryEmail"])
            else:
                correctPassword = self.userDetails[1]
            
                if password == correctPassword:
                    self.resetEntry(["entryEmail","entryPassword"])
                    
                    self.userLoginSequence()
                    self.signIn(self.userDetails)
                    self.after(1500,self.destroy)
                else:
                    self.setMessage("Incorrect password.","red")
                    self.resetEntry(["entryPassword"])

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


    def rememberMeConfirmClicked(self):
        self.loggedInEmail = self.rememberedEmail
        self.setMessage(f"Logging in as {self.loggedInEmail}","limegreen")
        self.loggedIn = True
        self.after(1000,self.destroy)
    
    def rememberMeDeniedClicked(self):
        self.lblMessage.place_forget()
        self.btnConfirm.configure(command=self.btnRegisterConfirmClicked)
        self.btnConfirm.place_forget()
        self.btnDeny.place_forget()

        self.loggedInEmail = ""
        self.clickablesOnOff()

    def signIn(self,userDetails):
        self.rememberedEmail = userDetails[0]
        if not self.loggedIn:
            self.setMessage(f"Would you like to login automatically as\n{self.rememberedEmail}?",self.globalColour)
            self.clickablesOnOff()
            self.btnConfirm.configure(command=self.rememberMeConfirmClicked)
            self.btnConfirm.place(in_=self.btnRegister,y=150)
            self.btnDeny.place(in_=self.btnSignIn,y=150)

        else:
            self.loggedInEmail = self.rememberedEmail
            self.setMessage(f"Logging in as {self.loggedInEmail}","limegreen")

    def registerClicked(self):
        setMessage = self.setMessage

        self.btnConfirm.place_forget()
        newEmail = self.entryEmail.get()
        newPassword = self.entryPassword.get()

        details,_ = getAllDetails()
        found,_ = self.checkDetailsFound(newEmail,details)
        emailEmpty,passwordEmpty = self.checkEmpty(newEmail,newPassword)
        emailValid = self.checkEmail(newEmail)

        if found:
            setMessage("Email already registered with another account","black")
        elif emailEmpty:
            setMessage("Please enter the email you would like to register with.","black")
        elif passwordEmpty:
            setMessage("Please enter a password to use with this account.","black")
        elif not emailValid:
            setMessage("Please enter a valid email.","black")
        else:
            setMessage("Would you like to register a new account with these details?","black")
            self.btnConfirm.place(in_=self.btnRegister,x=75,y=150)

    def btnRegisterConfirmClicked(self):
        self.btnConfirm.place_forget()
        newEmail = self.entryEmail.get()
        newPassword = self.entryPassword.get()

        newDetails = [newEmail,newPassword,""]

        details,rememberMeIndex = getAllDetails()
        details.append(newDetails)
        newAuthDetails = {"details":details,"rememberMe":rememberMeIndex}

        print(newAuthDetails)
        
        with open("authDetails.json","w") as f:
            f.write(json.dumps(newAuthDetails))
        
        self.resetEntry(["entryEmail","entryPassword"])
        self.setMessage("Account successfully created. Please log in.","limegreen")


    def userLoginSequence(self):
        rememberMeVal = self.checkboxRememberMe.value
        details,_ = getAllDetails()

        if rememberMeVal:
            userDetailsIndex = details.index(self.userDetails)
        else:
            userDetailsIndex = "False"

        newAuthDetails = {"details":details,"rememberMe":userDetailsIndex}
        with open("authDetails.json","w") as f:
            f.write(json.dumps(newAuthDetails))
        
        self.loggedIn = True
    
    def checkRememberMe(self):
        print("hello")
        details,rememberMeIndex = getAllDetails()
        if rememberMeIndex != "False":
            userDetails = details[rememberMeIndex]
            self.signIn(userDetails)

    def bindingEventListeners(self):
        elements = self.elements
        for each in elements:
            elements[each].bind("<Enter>",lambda event,element=each:self.elementMouseEnter(element))
            elements[each].bind("<Leave>",lambda event,element=each:self.elementMouseLeave(element))

        """self.entryEmail.bind("<FocusIn>",self.emailFocusIn)
        self.entryEmail.bind("<FocusOut>",self.emailFocusOut)
        self.entryPassword.bind("<FocusIn>",self.passwordFocusIn)
        self.entryPassword.bind("<FocusOut>",self.passwordFocusOut)"""

#auth = Auth()
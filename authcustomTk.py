# Amogh NG
# Auth screen with customtkinter

from customtkinter import *
from PIL import ImageTk, Image
import json
from checkbox_customTk import Checkbox

class Auth(CTk):
    globalFontName = "Bahnschrift"
    buttonFont = (globalFontName,25)
    emojiFont = ("Segoe UI Emoji",30)
    globalColour = "white"

    def __init__(self):
        super().__init__()

        self.geometry("850x570")
        self.minsize(850,570)
        self.maxsize(850,570)
        self.title("Log in - Tickd")

        self.loggedIn = False

        self.widgets()
        self.placeWidgets()
        self.checkRememberMe()
        
        
        self.mainloop()

        

    def widgets(self):
        globalFontName = self.globalFontName
        emojiFont = self.emojiFont
        buttonFont = self.buttonFont

        self.frameLogin = CTkFrame(self,width=850,height=570,corner_radius=20)

        self.imgMode = CTkImage(light_image=Image.open("logo//moon.png"),dark_image=Image.open("logo//sun.png"),size=(40,40))
        self.btnMode = CTkButton(self.frameLogin,image=self.imgMode,text="",command=self.changeMode,width=1,fg_color="#252425",hover_color="royalblue1",corner_radius=50)
        
        self.logo = CTkImage(light_image=Image.open("logo//whiteBGLogo.png"),dark_image=Image.open("logo//blackBGLogo.png"),size=(330,105)) 
        self.logoPanel = CTkLabel(self.frameLogin,text="",image=self.logo)
        
        
        self.entryEmail = CTkEntry(self.frameLogin,font=(globalFontName,25),width=400,placeholder_text="email",corner_radius=15)
        self.entryPassword = CTkEntry(self.frameLogin,font=(globalFontName,25),width=400,placeholder_text="password",show="*",corner_radius=15)
        self.lblEmail = CTkLabel(self.frameLogin,font=emojiFont,text="✉️")
        self.lblPassword = CTkLabel(self.frameLogin,font=emojiFont,text="🔒")
        
        self.imgShowPassword = CTkImage(Image.open("eyeIcon.png"),size=(30,30))
        self.btnShowPassword = CTkButton(self.frameLogin,image=self.imgShowPassword,text="",width=1,command=self.showHide,corner_radius=15)
        self.imgHidePassword = CTkImage(Image.open("eyeIconOff.png"),size=(30,30))
        self.btnHidePassword = CTkButton(self.frameLogin,image=self.imgHidePassword,text="",width=1,command=self.showHide,corner_radius=15)
        self.btnRegister = CTkButton(self.frameLogin,text="register",font=buttonFont,corner_radius=15,text_color="black",border_color="black",fg_color="white",border_width=5)
        self.btnSignIn = CTkButton(self.frameLogin,text="sign in",font=buttonFont,corner_radius=15,command=self.signInClicked,text_color="black",border_color="black",fg_color="white",border_width=5)
        self.btnRegisterConfirm = CTkButton(self.frameLogin,text="confirm",font=buttonFont,corner_radius=15,command=self.signInClicked,text_color="black",border_color="black",fg_color="white",border_width=5)
        self.checkboxRememberMe = Checkbox(self.frameLogin,x=0,y=50,size=(35,35),relWidget=self.entryPassword)
        self.messageVar = StringVar()
        self.lblMessage = CTkLabel(self.frameLogin,font=(globalFontName,30),textvariable=self.messageVar)

        self.elements = {
            "lblEmail":self.lblEmail,
            "lblPassword":self.lblPassword,
            "entryEmail":self.entryEmail,
            "entryPassword":self.entryPassword,
            #"btnRegister":self.btnRegister,
            #"btnSignIn":self.btnSignIn,
            #"btnShowPassword":self.btnShowPassword,
            #"btnHidePassword":self.btnHidePassword,
            #"btnRegisterConfirm":self.btnRegisterConfirm
            }
        #self.bindingEventListeners()
        

    def placeWidgets(self):
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
        
    def changeMode(self):
        if get_appearance_mode() == "Light":
            set_appearance_mode("Dark")
            self.btnMode.configure(fg_color="#252425")
            self.globalColour = "white"
        else:
            set_appearance_mode("Light")
            self.btnMode.configure(fg_color="#eaeaeb")
            self.globalColour = "black"
    
    def elementMouseEnter(self,element):
        if "btn" in element or "entry" in element:
            self.elements[element].configure(relief="solid")
        else:
            self.elements[element].configure(fg_color="black")
    
    def elementMouseLeave(self,element):
        if "btn" in element:
            self.elements[element].configure(relief="raised")
        elif "entry" in element:
            self.elements[element].configure(relief="flat")
        # rewrite
        else:
            self.elements[element].configure(fg_color="gray")

    def showHide(self):
        if self.btnShowPassword.winfo_ismapped():
            self.btnShowPassword.place_forget()
            self.btnHidePassword.place(in_=self.entryPassword,x=410)
            self.entryPassword.configure(show="")
        else:
            self.btnHidePassword.place_forget()
            self.btnShowPassword.place(in_=self.entryPassword,x=410)
            self.entryPassword.configure(show="*")

    def getDetails(self):
        with open("authDetails.json","r") as f:
            detailsDict = json.load(f)
            details = detailsDict["details"]
            rememberMeIndex = detailsDict["rememberMe"]

        return details,rememberMeIndex

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
        
        
        fontSize = 30
        print(length)
        x=150-(7*length)
        print(x)
        lblMessage.place(in_=btnRegister,x=x,y=80)


        """if length<20:
            fontSize = 30
            x=100-(2*length)
            print(x)
            lblMessage.place(in_=btnRegister,x=x,y=80)
        elif length<60 and length>30 and "\n" in message:
            fontSize = 25
            lblMessage.place(in_=btnRegister,x=-50,y=85)
        elif length<47 and length>30:
            fontSize = 25
            lblMessage.place(in_=btnRegister,x=-170,y=85)
        elif length>30:
            fontSize = 20
            lblMessage.place(in_=btnRegister,x=-185,y=85)
        else:
            fontSize = 30
            lblMessage.place(in_=btnRegister,x=-95,y=80)"""
        
        if colour == "black" or colour == "white":
            colour = ("black","white")
        
        lblMessage.configure(font=(self.globalFontName,fontSize),text_color=colour)
        self.messageVar.set(message)

    def resetEntry(self,entries:list):
        elements = self.elements
        for each in entries:
            element = elements[each]
            element.configure(show="")
            element.delete(0,END)
        
        self.lblEmail.focus_set()

    def btnRegisterConfirmClicked(self):
        pass

    def signInClicked(self):
        print("Hello")
        self.btnRegisterConfirm.place_forget()

        email = self.entryEmail.get()
        password = self.entryPassword.get()
        
        details,_ = self.getDetails()
        
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

    def rememberMeConfirmClicked(self):
        self.setMessage(f"Login successful as\n{self.loggedInEmail}","green")
        self.loggedIn = True
        self.after(1000,self.destroy)
    
    def rememberMeDeniedClicked(self):
        self.lblMessage.place_forget()
        self.btnRegisterConfirm.configure(command=self.btnRegisterConfirmClicked)
        self.btnRegisterConfirm.place_forget()

    def signIn(self,userDetails):
        self.loggedInEmail = userDetails[0]
        self.setMessage(f"Would you like to login automatically as\n{self.loggedInEmail}?")
        self.btnRegisterConfirm.configure(command=self.rememberMeConfirmClicked)



    def userLoginSequence(self):
        rememberMeVal = self.rememberMe.value
        details,_ = self.getDetails()

        if rememberMeVal:
            userDetailsIndex = details.index(self.userDetails)
        else:
            userDetailsIndex = "False"

        newAuthDetails = {"details":details,"rememberMe":userDetailsIndex}
        with open("authDetails.json","w") as f:
            f.write(json.dumps(newAuthDetails))
    
    def checkRememberMe(self):
        print("hello")
        details,rememberMeIndex = self.getDetails()
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

auth = Auth()
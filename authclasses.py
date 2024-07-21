# Amogh NG
# Auth with class-based approach

from tkinter import *
import json
from time import sleep
from checkbox import Checkbox

try:
    from import_packages import import_packages
    import_packages(['pillow',])
except:
    pass
from PIL import Image, ImageTk

class Auth(Tk):
    globalFontName = "Bahnschrift"
    buttonFont = (globalFontName,20)
    emojiFont = ("Segoe UI Emoji",20)

    



    def __init__(self):
        super().__init__() # Essentially the same as calling the Tk() function
        self.geometry("800x570")
        self.minsize(800,570)
        self.title("Log in - Tickd")
        #self.iconbitmap("logo//tickd.ico")

        self.loggedIn = False
        

        self.widgets()
                 

    def widgets(self):
        buttonFont = self.buttonFont
        globalFontName = self.globalFontName
        emojiFont = self.emojiFont

        #-----------# Widgets #-----------#
        self.entryEmail = Entry(self,font=buttonFont,width=30,fg="gray",relief="flat")
        self.entryEmail.insert(0,"email")


        self.entryPassword = Entry(self, font=buttonFont,width=30,fg="gray",relief="flat")
        self.entryPassword.insert(0,"password")

        self.lblEmail = Label(self,font=emojiFont,text="✉",fg="gray")
        self.lblPassword = Label(self,font=emojiFont,text="🔒",fg="gray")
        self.lblRememberMe = Label(self,font=(globalFontName,20),text="remember me",fg="black")

        messageVar = StringVar()
        self.lblMessage = Label(self,font=(globalFontName,30),fg="black",textvariable=messageVar)


        self.btnSignIn = Button(self,text="sign in",font=buttonFont)
        self.btnSignIn.bind("<Button-1>",lambda event:self.signInClicked())
        
        self.btnRegister = Button(self,text="register",font=buttonFont,relief="raised")
        self.btnRegister.bind("<Button-1>",lambda event:self.registerClicked())

        self.btnRegisterConfirm = Button(self,text="confirm",font=buttonFont,relief="raised")
        self.btnRegisterConfirm.bind("<Button-1>",lambda event:self.registerConfirmClicked())

        photoLogoBlack = ImageTk.PhotoImage(Image.open("logo//whiteBGLogo.png").resize((280,70)))
        self.panelLogoBlack = Label(self,image=photoLogoBlack)

        self.imgEyeShow = ImageTk.PhotoImage(Image.open("eyeIcon.png").resize((27,30)))

        self.imgEyeHide = ImageTk.PhotoImage(Image.open("eyeIconOff.png").resize((27,30)))

        self.btnShowPassword = Button(self,image=self.imgEyeShow)
        self.btnHidePassword = Button(self,image=self.imgEyeHide)

        self.btnShowPassword.bind("<Button-1>",lambda event,eyeShow=True:self.showPasswordToggle(eyeShow))
        self.btnHidePassword.bind("<Button-1>",lambda event,eyeShow=False:self.showPasswordToggle(eyeShow))
        
        self.rememberMe = Checkbox(self,0,60,self.entryPassword,(30,30))
        self.rememberMe.placeWidget()
        
        self.elements = {
            "lblEmail":self.lblEmail,
            "lblPassword":self.lblPassword,
            "entryEmail":self.entryEmail,
            "entryPassword":self.entryPassword,
            "btnRegister":self.btnRegister,
            "btnSignIn":self.btnSignIn,
            "btnShowPassword":self.btnShowPassword,
            "btnHidePassword":self.btnHidePassword,
            "btnRegisterConfirm":self.btnRegisterConfirm}

        
        self.bindingEventListeners()
        self.placingWidgets()
        self.checkRememberMe()
        self.mainloop()
    
    def placingWidgets(self):
        self.entryEmail.grid(row=1,column=0,padx=180,pady=(150,0),sticky="")
        self.entryPassword.grid(row=2,column=0, sticky="",padx=180,pady=(20,0))
        self.lblEmail.place(in_=self.entryEmail,x=-50,y=-5)
        self.lblPassword.place(in_=self.entryPassword,x=-52,y=-5)
        self.btnShowPassword.place(in_=self.entryPassword,x=460,y=-2)
        self.btnRegister.place(in_=self.lblPassword,x=110,y=120)
        self.btnSignIn.place(in_=self.lblPassword,x=270,y=120)
        self.lblRememberMe.place(in_=self.btnRegister,x=-25,y=-65)
        
        #self.checkbtnRememberUser.place(in_=self.entryPassword,y=50)
        self.lblMessage.place(in_=self.btnRegister,x=-75,y=80)
        self.panelLogoBlack.grid(row=3,column=0)
        self.panelLogoBlack.place(in_=self.entryEmail,x=80,y=-100)
        
        self.messageVar = StringVar()
        self.lblMessage = Label(self,font=(self.globalFontName,30),fg="black",textvariable=self.messageVar)
    
    
    def setMessage(self,message,colour):
        length = len(message)
        lblMessage = self.lblMessage
        btnRegister = self.btnRegister

        print(repr(message))
        
        if length<20:
            fontSize = 30
            lblMessage.place(in_=btnRegister,x=-10,y=80)
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
            lblMessage.place(in_=btnRegister,x=-95,y=80)
        
        
        lblMessage.config(font=(self.globalFontName,fontSize),fg=colour)
        self.messageVar.set(message)

    #-----------------------# Details #----------------------------#
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

        if email == "email" and password == "password":
            emailEmpty = True
            passwordEmpty = True
        elif email == "email" or email == "":
            self.setMessage("Please enter your email.","black")
            emailEmpty = True
        elif password == "password" or password == "":
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

    #------------------# Button functions #--------------------#

    def showPasswordToggle(self,eyeShow):
        elements = self.elements
        entryPassword = self.entryPassword
        if eyeShow:
            print("hi")
            elements["btnShowPassword"].place_forget()
            elements["btnHidePassword"].place(in_=entryPassword,x=460,y=-2)
            entryPassword.config(show="")
        else:
            print("no")
            if entryPassword.get() == "password":
                entryPassword.config(show="")
            else:
                entryPassword.config(show="*")
            
            elements["btnHidePassword"].place_forget()
            elements["btnShowPassword"].place(in_=entryPassword,x=460,y=-2) 

    def bindingEventListeners(self):
        elements = self.elements
        for each in elements:
            elements[each].bind("<Enter>",lambda event,element=each:self.elementMouseEnter(element))
            elements[each].bind("<Leave>",lambda event,element=each:self.elementMouseLeave(element))

        self.entryEmail.bind("<FocusIn>",self.emailFocusIn)
        self.entryEmail.bind("<FocusOut>",self.emailFocusOut)
        self.entryPassword.bind("<FocusIn>",self.passwordFocusIn)
        self.entryPassword.bind("<FocusOut>",self.passwordFocusOut)
        
    def elementMouseEnter(self,element):
        if "btn" in element or "entry" in element:
            self.elements[element].config(relief="solid")
        else:
            self.elements[element].config(fg="black")
    


    def elementMouseLeave(self,element):
        if "btn" in element:
            self.elements[element].config(relief="raised")
        elif "entry" in element:
            self.elements[element].config(relief="flat")
        # rewrite
        else:
            self.elements[element].config(fg="gray")

    def emailFocusIn(self,event):
        if self.entryEmail.get() == "email":
            self.entryEmail.delete(0,"end")
        self.entryEmail.config(fg="black",relief="solid")
        self.lblEmail.config(fg="black")

    

    def emailFocusOut(self,event):
        if self.entryEmail.get() == "":
            self.entryEmail.insert(0,"email")
            self.entryEmail.config(fg="gray")
        self.entryEmail.config(relief="flat")
        self.lblEmail.config(fg="gray")
    

    def passwordFocusIn(self,event):
        if self.entryPassword.get() == "password":
            self.entryPassword.delete(0,"end")
            self.entryPassword.config(show="*")
        self.entryPassword.config(fg="black",relief="solid")
        self.lblPassword.config(fg="black")

        if self.btnHidePassword.winfo_ismapped():
            self.entryPassword.config(show="")
    

    def passwordFocusOut(self,event):
        entryPassword = self.entryPassword
        lblPassword = self.lblPassword

        if entryPassword.get() == "":
            entryPassword.insert(0,"password")
            entryPassword.config(fg="gray",show="")
        entryPassword.config(relief="flat")
        lblPassword.config(fg="gray")

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
            self.setMessage("Please enter your details.","black")
        elif emailEmpty:
            self.setMessage("Please enter your email.","black")
            self.resetEntry(["entryPassword"])
        elif passwordEmpty:
            self.setMessage("Please enter your password.","black")
        else:
            if emailValid and not found:
                self.setMessage("Details not found.\nPlease click 'register' to make a new account.","red")
            elif not emailValid:
                self.setMessage("Please enter a valid email.","black")
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

    def registerClicked(self):
        setMessage = self.setMessage

        self.btnRegisterConfirm.place_forget()
        newEmail = self.entryEmail.get()
        newPassword = self.entryPassword.get()

        details,_ = self.getDetails()
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
            self.btnRegisterConfirm.place(in_=self.btnRegister,x=75,y=150)

    def registerConfirmClicked(self):
        self.btnRegisterConfirm.place_forget()
        newEmail = self.entryEmail.get()
        newPassword = self.entryPassword.get()

        newDetails = [newEmail,newPassword]

        details,rememberMeIndex = self.getDetails()
        details.append(newDetails)
        newAuthDetails = {"details":details,"rememberMe":rememberMeIndex}

        print(newAuthDetails)
        
        with open("authDetails.json","w") as f:
            f.write(json.dumps(newAuthDetails))

        
        self.resetEntry(["entryEmail","entryPassword"])
        self.setMessage("Account successfully created. Please log in.","green")



    def resetEntry(self,entries:list):
        elements = self.elements
        entryEmail = self.entryEmail
        entryPassword = self.entryPassword
        for each in entries:
            element = elements[each]
            element.config(fg="gray",show="")
            element.delete(0,END)
        
        if "entryEmail" in entries:
            entryEmail.insert(0,"email")
        if "entryPassword" in entries:
            entryPassword.insert(0,"password")
        self.lblEmail.focus_set()
    
    def signIn(self,userDetails):
        self.loggedInEmail = userDetails[0]
        self.setMessage(f"Login successful as\n{self.loggedInEmail}","green")
        self.loggedIn = True
        

        self.after(1000,self.destroy)

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


auth = Auth()
print(auth.loggedIn)
print(auth.loggedInEmail)

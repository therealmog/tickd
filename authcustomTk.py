# Amogh NG
# Auth screen with customtkinter

from customtkinter import *
from PIL import Image
import json
from lib.checkbox_customTk import Checkbox
from lib.getDetails import getAllDetails
from register import Register
from lib.checkWithPepper import checkWithPepper
from resetPassword import ResetPassword
from tkinter import messagebox



class Auth(CTk):
    globalFontName = "Bahnschrift"
    buttonFont = (globalFontName,25)
    emojiFont = ("Segoe UI Emoji",30)
    globalColour = ("black","white")
    accent = "crimson"

    def __init__(self):
        super().__init__()

        self.geometry("600x400")
        self.minsize(600,400)
        self.maxsize(600,400)
        self.title("Log in - Tickd")
        self.iconbitmap("logo//tickd.ico")

        self.loggedIn = False

        set_appearance_mode("dark")
        self.checkRememberMe()
        if not self.loggedIn:
            self.widgets()
            self.placeWidgets()
            

            self.bind("<Return>",lambda event:self.signInClicked())

            self.registerWinOpen = False
            self.resetWinOpen = False
            self.theme = "dark"

            self.mainloop()
        
        

    def widgets(self):
        globalFontName = self.globalFontName
        emojiFont = self.emojiFont
        buttonFont = self.buttonFont

        self.frameLogin = CTkFrame(self,width=560,height=370,corner_radius=20,border_color="gray7",border_width=5,fg_color=("white","#171616"))
        

        self.imgMode = CTkImage(light_image=Image.open("logo//moon.png"),dark_image=Image.open("logo//sun.png"),size=(35,35))
        self.btnMode = CTkButton(self.frameLogin,image=self.imgMode,text="",command=self.changeMode,width=1,fg_color="#252425",hover_color=self.accent,corner_radius=50)
        
        self.logo = CTkImage(light_image=Image.open("logo//whiteBGLogo.png"),dark_image=Image.open("logo//blackBGLogo.png"),size=(282,90)) #Ratio 330x105
        self.logoPanel = CTkLabel(self.frameLogin,text="",image=self.logo)
        
        
        self.entryEmail = CTkEntry(self.frameLogin,font=(globalFontName,25),width=400,placeholder_text="email",corner_radius=15)
        self.entryPassword = CTkEntry(self.frameLogin,font=(globalFontName,25),width=400,placeholder_text="password",show="*",corner_radius=15)
        self.lblEmail = CTkLabel(self.frameLogin,font=emojiFont,text="✉️")
        self.lblPassword = CTkLabel(self.frameLogin,font=emojiFont,text="🔒")
        
        self.imgShowPassword = CTkImage(Image.open("icons//eyeIcon.png"),size=(32,24))
        self.btnShowPassword = CTkButton(self.frameLogin,image=self.imgShowPassword,text="",width=1,command=self.showHide,corner_radius=15,fg_color=self.accent)
        self.imgHidePassword = CTkImage(Image.open("icons//eyeIconOff.png"),size=(32,24))
        self.btnHidePassword = CTkButton(self.frameLogin,image=self.imgHidePassword,text="",width=1,command=self.showHide,corner_radius=15)
        self.btnRegister = CTkButton(self.frameLogin,text="register",font=buttonFont,corner_radius=15,text_color=self.globalColour,border_color=("black","gray12"),fg_color=self.accent,border_width=2,command=self.createRegisterWindow)
        

        self.btnSignIn = CTkButton(self.frameLogin,text="sign in",font=buttonFont,corner_radius=15,command=self.signInClicked,text_color=self.globalColour,border_color=("black","gray12"),fg_color=self.accent,border_width=2)
        self.btnConfirm = CTkButton(self.frameLogin,text="confirm",font=buttonFont,corner_radius=15,command=self.signInClicked,text_color=self.globalColour,border_color=("black","gray12"),fg_color=self.accent,border_width=2)
        self.checkboxRememberMe = Checkbox(self.frameLogin,x=0,y=50,size=(35,35),relWidget=self.entryPassword)
        self.messageVar = StringVar()
        self.lblMessage = CTkLabel(self.frameLogin,font=(globalFontName,30),textvariable=self.messageVar,justify="left")
        

        self.lblRememberMe = CTkLabel(self.frameLogin,text="remember me",font=(globalFontName,25),text_color=self.globalColour,cursor="hand2")
        self.lblRememberMe.bind("<Button-1>",lambda event: self.checkboxRememberMe.boxClicked(event))

        self.lblForgotPassword = CTkLabel(self.frameLogin,font=(globalFontName,22),text="forgot your password?",cursor="hand2")
        self.lblForgotPassword.bind("<Enter>",lambda event: self.forgotLblEnter())
        self.lblForgotPassword.bind("<Leave>",lambda event: self.forgotLblLeave())
        self.lblForgotPassword.bind("<Button-1>",lambda event: self.createResetWindow())

        self.imgTick = CTkImage(Image.open("logo//tick.png"),size=(35,35))
        self.lblLoggingIn = CTkLabel(self.frameLogin,font=(globalFontName,22),text=" Logging in.",text_color="limegreen",image=self.imgTick,compound="left")
        
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
        

    def placeWidgets(self):
        #self.panelImgBG.place(x=0,y=0)
        self.frameLogin.place(relx=0.5,rely=0.5,anchor="center")
        self.logoPanel.place(relx=0.25,rely=0.05)
        self.btnMode.place(in_=self.logoPanel,x=330,y=-5)
        self.entryEmail.place(in_=self.logoPanel,x=-60,y=105)
        self.entryPassword.place(in_=self.entryEmail,y=50)
        self.lblEmail.place(in_=self.entryEmail,x=-50,y=-5)
        self.lblPassword.place(in_=self.entryPassword,x=-50,y=-5)
        self.btnShowPassword.place(in_=self.entryPassword,x=405,y=1)
        self.btnRegister.place(in_=self.entryPassword,x=50,y=100)
        self.btnSignIn.place(in_=self.btnRegister,x=150)
        self.checkboxRememberMe.placeWidget()
        self.lblRememberMe.place(in_=self.entryPassword,x=40,y=52)
        self.lblForgotPassword.place(in_=self.btnRegister,x=50,y=50)
        
        
    def changeMode(self):
        if get_appearance_mode() == "Light":
            self.theme = "dark"
            set_appearance_mode("Dark")
            #self.panelImgBG.configure(image=self.darkImgBG)
            #self.imgBGPath = self.darkImgBGPath
            self.btnMode.configure(fg_color="#252425")
            self.globalColour = "white"
        else:
            self.theme = "light"
            set_appearance_mode("Light")
            #self.panelImgBG.configure(image=self.lightImgBG)
            #self.imgBGPath = self.lightImgBGPath
            self.btnMode.configure(fg_color="#eaeaeb")
            self.globalColour = "black"
    
    def forgotLblEnter(self):
        self.hoverOriginalFont = self.lblForgotPassword._font
        newFont = (self.hoverOriginalFont[0],self.hoverOriginalFont[1],"underline")
        self.lblForgotPassword.configure(font=newFont,text_color=self.accent)
    
    def forgotLblLeave(self):
        self.lblForgotPassword.configure(font=self.hoverOriginalFont,text_color=("black","white"))

    def createResetWindow(self):
        if self.resetWinOpen:
            messagebox.showinfo("Window already active","Reset password window already active.")
            #self.setMessage("Reset password window already active.")
        else:
            self.resetWinOpen = True
            # Replace "no" with self.imgBGPath
            self.resetWin = ResetPassword("no",self.accent,origin=self)

    def showHide(self):
        if self.btnShowPassword.winfo_ismapped():
            self.btnShowPassword.place_forget()
            self.btnHidePassword.place(in_=self.entryPassword,x=405,y=1)
            self.entryPassword.configure(show="")
        else:
            self.btnHidePassword.place_forget()
            self.btnShowPassword.place(in_=self.entryPassword,x=405,y=1)
            self.entryPassword.configure(show="*")


    def checkDetailsFound(self,email,details):
        found = False
        for each in details: # Selects each sublist in the large overall list of details.
            if each[0] == email: # Uses format [email,password,username] so each[0] means the email.
                userDetails = each
                found = True
        if found == False:
            print("No details found.")
            userDetails = []    

        return found, userDetails
    
    def checkEmpty(self,email,password):
        emailEmpty = False
        passwordEmpty = False

        email = email.strip() # Removes any unnecessary whitespace in the entry boxes.

        if email == "" and password == "":
            emailEmpty = True
            passwordEmpty = True
        elif email == "":
            messagebox.showerror("Can't sign in to Tickd.","Please enter your email.")
            emailEmpty = True
        elif password == "":
            passwordEmpty = True
        
        return emailEmpty, passwordEmpty

    def checkEmail(self,email):
        if "@" in email:
            splitEmail = email.split("@")
            # Splits the email into two parts, e.g. john@gmail.com -> ["john","gmail.com"]
            if "." in splitEmail[1]:
                return True
            else:
                return False
        else: # The entered email contains no "@" symbol.
            return False 

    def setMessage(self,message,colour="white"):
        lblMessage = self.lblMessage
        btnRegister = self.btnRegister
        fontSize = 20

        if colour == "white" or colour == "black":
            colour = ("black","white")

        if "\n" in message:
            splitMsg = message.split("\n")
            msgRef = min(splitMsg)
        else:
            msgRef = message
        
        increment = 50-len(msgRef)

        x = increment * 6

        
        lblMessage.place(x=x,rely=0.8)


        lblMessage.configure(font=(self.globalFontName,fontSize),text_color=colour)
        self.messageVar.set(message)

    """def setMessage(self,message,colour):
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
        
        fontSize = 25
        x=160+increment-(7*length)
        lblMessage.place(in_=btnRegister,x=x,y=70)
        
        if colour == "black" or colour == "white":
            colour = ("black","white")
        
        lblMessage.configure(font=(self.globalFontName,fontSize),text_color=colour)
        self.messageVar.set(message)"""

    def resetEntry(self,entries:list):
        elements = self.elements
        for each in entries:
            element = elements[each]
            element.delete(0,END)
        
        self.lblEmail.focus_set()


    def signInClicked(self):
        self.btnConfirm.place_forget()

        email = self.entryEmail.get().lower()
        passwordTxt = self.entryPassword.get()
        
        details,_ = getAllDetails()
        
        emailEmpty, passwordEmpty = self.checkEmpty(email, passwordTxt)
        emailValid = self.checkEmail(email)
        found,self.userDetails = self.checkDetailsFound(email,details)
        

        if emailEmpty and passwordEmpty:
            messagebox.showerror("Can't sign in to Tickd.","Please enter your details.")
        elif emailEmpty:
            messagebox.showerror("Can't sign in to Tickd.","Please enter your email.")
            self.resetEntry(["entryPassword"])
        elif passwordEmpty:
            messagebox.showerror("Can't sign in to Tickd.","Please enter your password.")
        else:
            if emailValid and not found:
                messagebox.showerror("Details not found.","These details have not been found.\n\
                                     Please click 'register' if you do not already have an account.")
            elif not emailValid:
                messagebox.showerror("Can't sign in to Tickd.","Please enter a valid email.")
                self.resetEntry(["entryPassword","entryEmail"])
            else:
                correctPasswordTxt = self.userDetails[1]
                correctPWSplit = correctPasswordTxt.split("$")
                passwordWithSalt = correctPWSplit[0]+passwordTxt
                correct = checkWithPepper(passwordWithSalt,correctPWSplit[1])             

                if correct:
                    self.resetEntry(["entryEmail","entryPassword"])
                    
                    self.userLoginSequence()
                    self.signIn(self.userDetails)
                    self.lblForgotPassword.place_forget()
                    self.lblLoggingIn.place(in_=self.btnRegister,x=65,y=50)
                    self.after(1500,self.destroy)
                else:
                    messagebox.showerror("Can't sign in to Tickd.","Incorrect password.")
                    #self.setMessage("Incorrect password.","red")
                    self.resetEntry(["entryPassword"])
                    self.entryPassword.focus()

    def clickablesOnOff(self):
        clickables = []
        elements = self.elements
        for each in elements:
            if "entry" in each or "btn" in each:
                clickables.append(elements[each])
        
        for clickable in clickables:
            try:
                if clickable.cget("state") == "normal":
                    clickable.configure(state="disabled")
                else:
                    clickable.configure(state="normal")
            except:
                pass

    

    def rememberMeConfirmClicked(self):
        self.loggedInEmail = self.rememberedEmail
        self.userPath = f"users//{self.loggedInEmail}"

        self.loggedIn = True
        self.after(1000,self.destroy)
    
    def signIn(self,userDetails):
        self.rememberedEmail = userDetails[0]
        # Uses email that has been verified.
        
        if not self.loggedIn:
            rememberMeInput = messagebox.askyesno("Automatic sign-in",f"Login automatically as\n{self.rememberedEmail}?")
            # Message box returns either True or False if yes or no clicked.
            
            if rememberMeInput:
                self.rememberMeConfirmClicked()

        else:
            self.loggedInEmail = self.rememberedEmail
            self.userPath = f"users//{self.loggedInEmail}"


    def createRegisterWindow(self):
        if self.registerWinOpen:
            messagebox.showinfo("Window already active","Register window already active.")
        else:
            self.registerWinOpen = True
            self.registerWindow = Register()
            self.imgBGPath = None
            self.registerWindow.initialise(self.imgBGPath,self.accent,origin=self)
        
    def userLoginSequence(self):
        rememberMeVal = self.checkboxRememberMe.getValue()
        # Takes value from checkbox using public getter

        details,_ = getAllDetails()
        # Retrieves all auth details from JSON file using pre-written function (from lib)
        # Second underscore is for old remember me index, which is not needed.
        
        if rememberMeVal:
            newRememberMeIndex = details.index(self.userDetails)
        else:
            newRememberMeIndex = "False"

        newAuthDetails = {"details":details,"rememberMe":newRememberMeIndex}
        # Rewrites auth details dictionary using new Remember me index.
        
        with open("authDetails.json","w") as f:
            json.dump(newAuthDetails,f,indent=4)
            # Writes JSON object to file with indenting to make it look readable. 
        
        self.loggedIn = True
        # Allows user to sign into main app.
    
    def checkRememberMe(self):
        print("hello")
        details,rememberMeIndex = getAllDetails()
        if rememberMeIndex != "False":
            userDetails = details[rememberMeIndex]
            self.signIn(userDetails)


#auth = Auth()
